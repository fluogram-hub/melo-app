import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE B22 (STRICT V31) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Blue glass suit (transparent blue glass effect), ultra-glossy. Rounded child proportions. No internal anatomy."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
MATERIAL_DNA = "Homogeneous transparent blue glass/jelly, high IOR 1.5, caustics, cinematic refraction."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, Ray-traced lighting, 2026 CGI standards."

# --- 2. BASE DE DONNÉES DÉCORS (LES 80 LIEUX) ---
# J'ai intégré les premières destinations, la structure permet de toutes les coller
DECORS_DB = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)",
        "items": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro. Keep framing stable, no characters, no animals, no text."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine riverbanks", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine."},
            3: {"fr": "Au pied de la Tour", "en": "At the foot of the Tower", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tour."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ de Mars lawn", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars."}
        }
    },
    "mont_saint_michel": {
        "nom_fr": "Le Mont Saint-Michel (France)",
        "items": {
            1: {"fr": "La Baie", "en": "The Bay", "cue": "Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Baie."},
            2: {"fr": "La Porte d'Entrée", "en": "Main Gate", "cue": "Ancient stone textures, soft mist. Specific setting: La Porte d'Entrée."},
            3: {"fr": "Le Cloître", "en": "The Cloister", "cue": "Ancient stone textures, soft mist. Specific setting: Le Cloître."},
            4: {"fr": "Les Dunes", "en": "The Dunes", "cue": "Ancient stone textures, soft mist. Specific setting: Les Dunes."}
        }
    }
}

# --- 3. PLANS DE RÉALISATION (SYNC XLSX) ---
PLANS_DB = {
    1: {"Angle": "static wide shot, very slow breathing", "Light": "Golden Hour / Sunset", "Melo_Act": "Arrival (grey/misty landscape)", "Pipo_Act": "Pipo floats next to Melo"},
    2: {"Angle": "very slow push-in, medium framing", "Light": "Golden Hour / Sunset", "Melo_Act": "Melo rubs his eyes, looking for color", "Pipo_Act": "Pipo peeks playfully"},
    3: {"Angle": "static close-up, shallow depth of field", "Light": "Sunset", "Melo_Act": "Pipo glows softly, ready to help", "Pipo_Act": "Melo watches Pipo glow"},
    # ... on suit la même logique pour les 20 plans
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director Studio V59", layout="wide")

# --- 5. LOGIQUE SIDEBAR (FRANÇAIS) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_key = st.selectbox("DESTINATION (B9)", list(DECORS_DB.keys()), format_func=lambda x: DECORS_DB[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Récupération automatique des données du plan
    ville = DECORS_DB[v_key]
    plan = PLANS_DB.get(p_id, PLANS_DB[1])
    auto_b5_id = ((p_id - 1) % 4) + 1

# --- 6. INTERFACE ONGLETS (FRANÇAIS) ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR (FORMULE STRICTE XLSX) ---
with tab1:
    st.write(f"### ⚙️ Configuration du Décor — Plan {p_id}")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # E5 & B9
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_id-1, format_func=lambda x: ville['items'][x]['fr'], disabled=not e7_bool)
        b9_val = ville['nom_fr']
        # Angle (B6 / I34)
        i34 = st.selectbox("CAMÉRA MANUELLE (I34)", ["macro lens", "eye-level", "low-angle"], disabled=not e7_bool)
        b6 = plan['Angle']
        cam_final = i34 if e7 == "yes" else b6
    
    with c2:
        # Lumière (B7 / I35)
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Deep Night / Starlit", "Blue Hour / Mist"], disabled=not e7_bool)
        b7 = plan['Light']
        light_final = i35 if e7 == "yes" else b7
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful", "contemplative"], disabled=not e7_bool)
        b11 = st.selectbox("1ER PLAN (B11)", ["", "wild flowers", "autumn leaves", "mist"], disabled=not e7_bool)

    with c3:
        # Matières (D8 / D9)
        d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "candy", "lego"], disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", value="dry", disabled=not e7_bool)

    # --- FORMULE PROMPT 1 (COPIÉ-COLLÉ XLSX) ---
    e5_en = ville['items'][b5_val]['en']
    b12 = ville['items'][b5_val]['cue']
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
    texture_logic = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"
    b12_str = f"PLATE CUES (STRICT): {b12}. " if b12 != "" else ""

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {b9_val} during the {light_final}, with a {b8} atmosphere. "
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
    st.subheader("📝 PROMPT 1 (DÉCOR)")
    st.code(prompt_1)

# --- ONGLET 2 : PERSONNAGES ---
with tab2:
    st.write(f"### 🎨 Configuration Mélo & Pipo")
    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} ACTION: {plan['Melo_Act']}. "
        f"{DNA_PIPO} ACTION: {plan['Pipo_Act']}. "
        f"INTEGRATION: Characters are perfectly placed in the {e5_en} environment. {TECH_LOCKS}"
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
    if st.button("🚀 RENDU UNIQUE"):
        if init_vertex():
            with st.spinner("Nanobanana Pro calcule..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)
with c_btn2:
    if st.button("🔥 BATCH PRODUCTION (x4)"):
        if init_vertex():
            with st.spinner("Série de 4 décors..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_1, number_of_images=4, aspect_ratio="16:9")
                cols = st.columns(2)
                for i, img in enumerate(batch):
                    with cols[i%2]: st.image(img._pil_image)
