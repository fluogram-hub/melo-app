import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE B22 (STRICT) ---
DNA_MELO = "MÉLO: Bunny-shaped high-end designer toy, blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. No internal anatomy."
DNA_PIPO = "PIPO: Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera perspective. Soft cinematic bokeh, Ray-traced lighting."

# --- 2. BASE DE DONNÉES : DÉCORS (80 LIEUX) ---
DECORS_DB = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)",
        "items": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine Banks", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, streetlamps bokeh. Specific setting: Les Quais de Seine."},
            3: {"fr": "Au pied de la Tour", "en": "The foot of the Tower", "cue": "Eiffel Tower clearly recognizable. Specific setting: Au pied de la Tour."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ-de-Mars Lawn", "cue": "Eiffel Tower clearly recognizable. Specific setting: Pelouse du Champ-de-Mars."}
        }
    },
    "mont_saint_michel": {
        "nom_fr": "Le Mont Saint-Michel (France)",
        "items": {
            1: {"fr": "La Baie", "en": "The Bay", "cue": "Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Baie."},
            2: {"fr": "La Porte d'Entrée", "en": "The Entrance Gate", "cue": "Ancient stone textures, soft mist. Specific setting: La Porte d'Entrée."},
            3: {"fr": "Le Cloître", "en": "The Cloister", "cue": "Ancient stone textures, soft mist. Specific setting: Le Cloître."},
            4: {"fr": "Les Dunes", "en": "The Dunes", "cue": "Ancient stone textures, soft mist. Specific setting: Les Dunes."}
        }
    },
    "santorini_greece": {
        "nom_fr": "Santorin (Grèce)",
        "items": {
            1: {"fr": "La Vue Haute", "en": "High View", "cue": "Santorini whitewashed architecture, blue domes, Aegean sea horizon. Specific setting: La Vue Haute."},
            2: {"fr": "La Ruelle Blanche", "en": "White Alley", "cue": "Santorini whitewashed architecture. Specific setting: La Ruelle Blanche."},
            3: {"fr": "La Terrasse", "en": "The Terrace", "cue": "Santorini whitewashed architecture. Specific setting: La Terrasse."},
            4: {"fr": "Le Muret", "en": "The Low Wall", "cue": "Santorini whitewashed architecture. Specific setting: Le Muret."}
        }
    },
    "venice_italy": {
        "nom_fr": "Venise (Italie)",
        "items": {
            1: {"fr": "Le Grand Canal", "en": "The Grand Canal", "cue": "Venice canals, calm water reflections, historic facades. Specific setting: Le Grand Canal."},
            2: {"fr": "La Petite Ruelle", "en": "The Small Alley", "cue": "Venice canals, historic facades. Specific setting: La Petite Ruelle."},
            3: {"fr": "La Place Saint-Marc", "en": "St Mark's Square", "cue": "Venice canals, historic facades. Specific setting: La Place Saint-Marc."},
            4: {"fr": "L'Intérieur de la Gondole", "en": "Inside the Gondola", "cue": "Venice canals, historic facades. Specific setting: L'Intérieur de la Gondole."}
        }
    }
    # J'ai la structure prête pour les 20 autres...
}

# --- 3. BASE DE DONNÉES : PLANS (20 ÉTAPES) ---
PLANS_DB = {
    1: {"Angle": "Wide", "Type": "Establishing", "Light": "Golden Hour", "AM": "Arrival (grey/misty landscape)", "AP": "Pipo floats next to Melo"},
    2: {"Angle": "Medium", "Type": "Approach", "Light": "Golden Hour", "AM": "Melo rubs his eyes, looking for color", "AP": "Pipo peeks playfully"},
    3: {"Angle": "Close-up", "Type": "Pipo magic", "Light": "Sunset", "AM": "Pipo glows softly, ready to help", "AP": "Melo watches Pipo glow"},
    4: {"Angle": "POV/Detail", "Type": "What Melo sees", "Light": "Sunset", "AM": "Melo looks at a small detail", "AP": "Pipo touches the detail (magic)"},
    5: {"Angle": "Medium", "Type": "Melo emotion", "Light": "Sunset", "AM": "Melo smiles, reaching for light", "AP": "Pipo offers a soft glow"},
    6: {"Angle": "Wide", "Type": "Establishing", "Light": "Dusk", "AM": "Melo watches Pipo fly away", "AP": "Pipo flies away with glitter trail"},
    7: {"Angle": "Detail", "Type": "Sky changing", "Light": "Dusk", "AM": "Melo notices the sky changing", "AP": "Pipo paints the sky pastel"},
    10: {"Angle": "Close-up", "Type": "Awe", "Light": "Blue Hour", "AM": "Melo face in awe, lit by color", "AP": "Pipo glows near Melo"},
    12: {"Angle": "Wide", "Type": "Softening", "Light": "Night", "AM": "Melo slows, everything softens", "AP": "Pipo dims to bedtime level"},
    20: {"Angle": "Wide", "Type": "Sleep", "Light": "Night", "AM": "Sleep / fade to black", "AP": "Pipo dims to near-off"}
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Studio V58", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_key = st.selectbox("DESTINATION (B9)", list(DECORS_DB.keys()), format_func=lambda x: DECORS_DB[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DECORS_DB[v_key]
    plan = PLANS_DB.get(p_id, PLANS_DB[1])
    auto_b5_id = ((p_id - 1) % 4) + 1

# --- 5. INTERFACE ET ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR (FORMULE XLSX) ---
with tab1:
    st.subheader(f"⚙️ Paramètres du Décor (Plan {p_id})")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # E5 (Traduit en EN pour le prompt)
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_id-1, format_func=lambda x: ville['items'][x]['fr'], disabled=not e7_bool)
        i34 = st.selectbox("ANGLE MANUEL (I34)", ["macro lens", "eye-level", "low-angle tracking"], disabled=not e7_bool)
        b6 = plan['Angle']
        cam_final = i34 if e7 == "yes" else b6
    
    with c2:
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Soft Moonlight", "Deep Night", "Pastel Dawn"], disabled=not e7_bool)
        b7 = plan['Light']
        light_final = i35 if e7 == "yes" else b7
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful", "contemplative"], disabled=not e7_bool)
        b11 = st.selectbox("1er PLAN (B11)", ["", "flowers", "leaves", "mist"], disabled=not e7_bool)

    with c3:
        d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "candy", "lego"], disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", value="dry", disabled=not e7_bool)

    # --- CALCUL PROMPT 1 (FORMULE XLSX) ---
    e5_en = ville['items'][b5_val]['en']
    b9_fr = ville['nom_fr']
    b12_cue = ville['items'][b5_val]['cue']
    
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
    texture_logic = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {b9_fr} during the {light_final}, with a {b8} atmosphere. "
        f"The camera uses a {cam_final} with a low-angle ground perspective. "
        f"{b11_str}"
        f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {texture_logic}. "
        f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant, soft-focus silhouette, suggested only by blurred shapes and glowing light. "
        f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays, bedtime-friendly calm palette. "
        f"GROUND DETAIL: The ground is {b10} with high-tactile micro-textures. "
        f"PLATE CUES (STRICT): {b12_cue}. "
        f"RULES: No characters, no people, no text, no logos, no watermarks. Pure background plate."
    )
    st.divider()
    st.code(prompt_1)

# --- ONGLET 2 : PERSONNAGES ---
with tab2:
    st.subheader("🎨 Mélo & Pipo (Image)")
    # Formule intégrée avec les données du PLAN_DE_REALISATION
    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} ACTION: {plan['AM']}. "
        f"{DNA_PIPO} ACTION: {plan['AP']}. "
        f"INTEGRATION: Placed within the {e5_en} environment. {TECH_LOCKS}"
    )
    st.code(prompt_2)

# --- ONGLET 3 : VIDÉO ---
with tab3:
    st.subheader("🎞️ Animation Vidéo")
    v_act = st.selectbox("Action Vidéo", ["Boucle parfaite", "Non-boucle cinématique"], disabled=not e7_bool)
    v_speed = st.selectbox("Vitesse", ["Ultra-slow", "Natural"], disabled=not e7_bool)
    prompt_3 = f"Cinematic Video: {plan['AM']}. Trail: {plan['AP']}. Speed: {v_speed}. Mode: {v_act}."
    st.code(prompt_3)

# --- MOTEUR DE RENDU ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 RENDU UNIQUE"):
        if init_vertex():
            with st.spinner("Nanobanana Pro calcule..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                # On génère le décor (Prompt 1) par défaut
                imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)
with c2:
    if st.button("🔥 BATCH PRODUCTION (x4)"):
        if init_vertex():
            with st.spinner("Série Nanobanana..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_1, number_of_images=4, aspect_ratio="16:9")
                cols = st.columns(2)
                for i, img in enumerate(batch):
                    with cols[i%2]: st.image(img._pil_image)
