import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE B22 ---
DNA_MELO = "MÉLO: Bunny-shaped high-end designer toy, blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions."
DNA_PIPO = "PIPO: Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera perspective. Soft cinematic bokeh, Ray-traced lighting."

# --- 2. BASE DE DONNÉES DES 80 DÉCORS (TRADUCTION INCLUSE) ---
DECORS_DB = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)",
        "items": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine Banks", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine."},
            3: {"fr": "Au pied de la Tour", "en": "The foot of the Tower", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tower."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ-de-Mars Lawn", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars."}
        }
    },
    "mont_saint_michel": {
        "nom_fr": "Le Mont Saint-Michel (France)",
        "items": {
            1: {"fr": "La Baie", "en": "The Bay", "cue": "Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist."},
            2: {"fr": "La Porte d'Entrée", "en": "The Entrance Gate", "cue": "Ancient stone textures, soft mist. Specific setting: La Porte d'Entrée."},
            3: {"fr": "Le Cloître", "en": "The Cloister", "cue": "Ancient stone textures, soft mist. Specific setting: Le Cloître."},
            4: {"fr": "Les Dunes", "en": "The Dunes", "cue": "Ancient stone textures, soft mist. Specific setting: Les Dunes."}
        }
    },
    # Les autres 18 destinations suivent cette structure...
}

# --- 3. BASE DE DONNÉES DES 20 PLANS (SYNC XLSX) ---
PLANS_DB = {
    1: {"Angle": "Wide / establishing", "Cam_EN": "static wide shot, very slow breathing", "Expr": "curiosité paisible", "Light": "Golden Hour / Sunset", "FX": "none"},
    2: {"Angle": "Medium / approach", "Cam_EN": "very slow push-in, medium framing", "Expr": "curiosité paisible", "Light": "Golden Hour / Sunset", "FX": "none"},
    3: {"Angle": "Close-up / Pipo magic", "Cam_EN": "static close-up, shallow depth of field", "Expr": "curiosité paisible", "Light": "Golden Hour / Sunset", "FX": "soft golden sparkles"},
    # ... on suit la logique 1-5, 6-10, 11-15, 16-20 pour chaque décor
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Studio V57", layout="wide")

# --- 5. LOGIQUE SIDEBAR (PILOTAGE FR) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("ACTIVER CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_key = st.selectbox("DESTINATION (B9)", list(DECORS_DB.keys()), format_func=lambda x: DECORS_DB[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Calculs automatiques
    decor_id = ((p_id - 1) // 5) + 1
    plan_data = PLANS_DB.get(p_id, PLANS_DB[1]) # Fallback sur plan 1 si non rempli
    ville_data = DECORS_DB[v_key]

# --- 6. INTERFACE ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR (LA FORMULE XLSX) ---
with tab1:
    st.write(f"### ⚙️ Paramètres du Décor (Plan {p_id})")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        # E5 (Nom FR pour l'user, EN pour le prompt)
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=decor_id-1, 
                              format_func=lambda x: ville_data['items'][x]['fr'], disabled=not e7_bool)
        # B6 & I34
        b6 = plan_data['Cam_EN']
        i34 = st.selectbox("CAMÉRA MANUELLE (I34)", ["macro lens, shallow depth", "low-angle tracking", "eye-level fixed"], disabled=not e7_bool)
        cam_final = i34 if e7 == "yes" else b6

    with c2:
        # B7 & I35
        b7 = plan_data['Light']
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Deep Night / Starlit", "Blue Hour / Mist", "Golden Hour"], disabled=not e7_bool)
        light_final = i35 if e7 == "yes" else b7
        
        b8 = st.selectbox("AMBIANCE (B8)", ["calm and poetic", "mysterious", "joyful", "nostalgic"], disabled=not e7_bool)
        b11 = st.selectbox("1er PLAN (B11)", ["", "wild flowers", "autumn leaves", "water puddles"], disabled=not e7_bool)

    with c3:
        # D8 & D9
        d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "candy", "lego"], disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust", "sugar coating"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", value="dry and textured", disabled=not e7_bool)

    # --- CONSTRUCTION DU PROMPT 1 (FORMULE XLSX) ---
    e5_en = ville_data['items'][b5_val]['en']
    b9_en = v_key.replace('_', ' ').title()
    b12 = ville_data['items'][b5_val]['cue']
    
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    texture_logic = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
    b12_str = f"PLATE CUES (STRICT): {b12} " if b12 != "" else ""

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {b9_en} during the {light_final}, with a {b8} atmosphere. "
        f"The camera uses a {cam_final} with a low-angle ground perspective. "
        f"{b11_str}"
        f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {texture_logic}. "
        f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant, soft-focus silhouette, suggested only by blurred shapes and glowing light. "
        f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays, bedtime-friendly calm palette. "
        f"GROUND DETAIL: The ground is {b10} with high-tactile micro-textures. "
        f"{b12_str}"
        f"RULES: No characters, no people, no text, no logos, no watermarks. Pure background plate."
    )

    st.divider()
    st.subheader("📝 PROMPT DÉCOR (GENERATED)")
    st.code(prompt_1)

# --- ONGLET 2 : PERSONNAGES ---
with tab2:
    st.write(f"### 🎨 Configuration Mélo & Pipo")
    # Formule simplifiée pour l'exemple mais utilisant les données de PLANS_DB
    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} EXPRESSION: {plan_data['Expr']}. "
        f"{DNA_PIPO} FX: {plan_data['FX']}. "
        f"INTEGRATION: Characters are placed in {e5_en} ({b9_en}). "
        f"Lighting matches {light_final}. {TECH_LOCKS}"
    )
    st.code(prompt_2)

# --- 7. MOTEUR DE RENDU VERTEX ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

st.divider()
c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    if st.button("🚀 LANCER RENDU (IMAGE ACTIVE)"):
        if init_vertex():
            with st.spinner("Nanobanana Pro calcule..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                # On envoie le prompt_1 (Décor) pour cet exemple
                imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)
