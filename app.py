import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE B22 (LOCKS STRICTS V29) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES DÉCORS (LES 80 LIEUX) ---
DECORS_DB = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)",
        "items": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm streetlamps bokeh. Specific setting: Le Trocadéro."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine riverbanks", "cue": "Eiffel Tower clearly recognizable. Specific setting: Les Quais de Seine."},
            3: {"fr": "Au pied de la Tour", "en": "At the foot of the Tower", "cue": "Industrial metallic lattice, looking up. Specific setting: Au pied de la Tour."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ de Mars lawn", "cue": "Large grass area, distant tower silhouette. Specific setting: Pelouse du Champ-de-Mars."}
        }
    },
    # ... Ajoute les autres destinations sur le même modèle
}

# --- 3. PLAN DE RÉALISATION (EXTRAIT XLSX) ---
PLANS_DB = {
    1: {"Angle": "wide-angle lens", "Light": "Golden Hour", "M_Act": "Arrival (grey/misty landscape)", "P_Act": "Pipo floats next to Melo"},
    2: {"Angle": "medium framing", "Light": "Golden Hour", "M_Act": "Melo rubs his eyes", "P_Act": "Pipo peeks playfully"},
    3: {"Angle": "static close-up", "Light": "Sunset", "M_Act": "Melo watches Pipo glow", "P_Act": "Pipo hovers as a guide"},
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Integrated Studio", layout="wide")

# --- 5. LOGIQUE SIDEBAR (GLOBAL) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ ACTIVER MODE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_key = st.selectbox("DESTINATION (B9)", list(DECORS_DB.keys()), format_func=lambda x: DECORS_DB[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DECORS_DB[v_key]
    plan = PLANS_DB.get(p_id, PLANS_DB[1])
    auto_b5_id = ((p_id - 1) % 4) + 1

# --- 6. INTERFACE ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR ---
with tab1:
    st.write(f"### ⚙️ Configuration du Décor — {ville['nom_fr']}")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # E5 (Lieu Précis)
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_id-1, format_func=lambda x: ville['items'][x]['fr'], disabled=not e7_bool)
        # B6 / I34
        angles_list = ["wide-angle lens", "macro lens", "ground perspective", "eye-level"]
        b6_idx = angles_list.index(plan['Angle']) if plan['Angle'] in angles_list else 0
        b6_final = st.selectbox("ANGLE (B6/I34)", angles_list, index=b6_idx, disabled=not e7_bool)
    
    with c2:
        # B7 / I35
        lights_list = ["Golden Hour", "Blue Hour", "Sunset", "Deep Night"]
        b7_idx = lights_list.index(plan['Light']) if plan['Light'] in lights_list else 0
        b7_final = st.selectbox("LUMIÈRE (B7/I35)", lights_list, index=b7_idx, disabled=not e7_bool)
        b8_final = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
        b11_final = st.selectbox("1ER PLAN (B11)", ["none", "flowers", "leaves", "mist"], disabled=not e7_bool)

    with c3:
        d8_final = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "candy"], disabled=not e7_bool)
        d9_final = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10_final = st.text_input("SOL (B10)", value="dry", disabled=not e7_bool)

    # FORMULE PROMPT 1 (XLSX)
    e5_en = ville['items'][b5_val]['en']
    b12_cue = ville['items'][b5_val]['cue']
    d9_str = f" and {d9_final}" if d9_final != "none" else ""
    b11_str = f"In the immediate foreground, a subtle {b11_final} adds volumetric depth; " if b11_final != "none" else ""
    texture_logic = "sugar-coated crystalline textures" if "candy" in d8_final.lower() else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {ville['nom_fr']} during the {b7_final}, with a {b8_final} atmosphere. "
        f"The camera uses a {b6_final} with a low-angle ground perspective. {b11_str}"
        f"MATERIAL WORLD: All architecture reimagined in {d8_final}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {texture_logic}. "
        f"GROUND: {b10_final}. PLATE CUES (STRICT): {b12_cue}. "
        f"RULES: No characters, pure background plate."
    )
    st.divider()
    st.code(prompt_1)

# --- ONGLET 2 : PERSONNAGES ---
with tab2:
    st.write("### 🎨 Configuration Mélo & Pipo")
    ic1, ic2 = st.columns(2)
    with ic1:
        # Actions récupérées du Plan de réalisation
        a_m_final = st.text_input("ACTION MÉLO (A_M)", value=plan['M_Act'], disabled=not e7_bool)
        a_p_final = st.text_input("ACTION PIPO (A_P)", value=plan['P_Act'], disabled=not e7_bool)
    with ic2:
        s_expr = st.selectbox("EXPRESSION", ["curious", "amazed", "smiling", "sleepy"], disabled=not e7_bool)
        s_acc = st.text_input("ACCESSOIRES", value="none", disabled=not e7_bool)

    prompt_2 = (
        f"A high-end cinematic character photography. "
        f"{DNA_MELO} ACTION: {a_m_final}. EXPRESSION: {s_expr}. "
        f"{DNA_PIPO} ACTION: {a_p_final}. "
        f"INTEGRATION: Placed in {e5_en} ({ville['nom_fr']}). {TECH_LOCKS}"
    )
    st.code(prompt_2)

# --- MOTEUR DE RENDU VERTEX ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

st.divider()
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 LANCER RENDU (IMAGE ACTIVE)"):
        if init_vertex():
            with st.spinner("Rendu Nanobanana Pro..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                # Envoie le prompt de l'onglet actif (Simplifié ici pour prompt_1)
                imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)

with col_btn2:
    if st.button("🔥 BATCH PRODUCTION (DÉCOR x4)"):
        if init_vertex():
            with st.spinner("Série de 4 en cours..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_1, number_of_images=4, aspect_ratio="16:9")
                cols = st.columns(2)
                for i, img in enumerate(batch):
                    with cols[i%2]: st.image(img._pil_image)
