import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# ZONE 1 : ADN & VERROUS TECHNIQUES (B22)
# =========================================================
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. No internal anatomy."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent reflections. Dot eyes and small smile. Tiny scale (5-10% of Mélo). Soft constant glow."
MATERIAL_DNA = "Homogeneous transparent blue glass/jelly, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# =========================================================
# ZONE 2 : DICTIONNAIRES (Injection de données à venir)
# =========================================================
# Note: Ces structures resteront fixes, seul leur contenu grandira.
MAT_MAP = {
    "🍭 SUCRERIES": {
        "Marshmallow foam": "Marshmallow foam (matte soft), squishy appearance",
        "Translucent jelly candy (glossy)": "Translucent jelly candy (glossy), subsurface scattering"
    } # Reste des 22 matières ici...
}

DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)", 
        "landmark_en": "Eiffel Tower",
        "decors": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Eiffel Tower clearly recognizable..."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine banks", "cue": "..."}
        }
    } # Reste des 20 destinations ici...
}

PLANS_DB = {
    1: {"Angle": "wide-angle lens", "Light": "Golden Hour", "AM": "Arrival", "AP": "Floating", "Mode": "Perfect loop"},
    2: {"Angle": "medium framing", "Light": "Sunset", "AM": "Searching", "AP": "Peeking", "Mode": "Cinematic"}
}

# =========================================================
# ZONE 3 : LOGIQUE DE L'INTERFACE (MIROIR)
# =========================================================
st.set_page_config(page_title="Melo Studio Master V64", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ MODE MANUEL (E7)", value=False)
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Pré-calculs
    ville = DB_DECORS[v_id]
    plan = PLANS_DB.get(p_id, PLANS_DB[1])
    auto_b5_id = ((p_id - 1) % 4) + 1

# --- Système d'onglets Cockpit ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# =========================================================
# ZONE 4 : ONGLET 1 - DÉCOR (FORMULE XLSX)
# =========================================================
with tab1:
    st.subheader(f"⚙️ Pilotage du Décor")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_id-1, 
                              format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        i34 = st.selectbox("ANGLE MANUEL (I34)", ["macro lens", "eye-level", "low-angle"], disabled=not e7_bool)
        cam_final = i34 if e7_bool else plan['Angle']
    
    with c2:
        i35 = st.selectbox("LUMIÈRE (B7/I35)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"], disabled=not e7_bool)
        light_final = i35 if e7_bool else plan['Light']
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
        b11 = st.selectbox("1ER PLAN (B11)", ["none", "flowers", "leaves"], disabled=not e7_bool)

    with c3:
        cat_d8 = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8_name = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()), disabled=not e7_bool)
        d8_val = MAT_MAP[cat_d8][d8_name]
        d9 = st.selectbox("MATÉRIEL D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", value="dry and textured", disabled=not e7_bool)

    # --- FORMULE MAÎTRESSE PROMPT 1 ---
    e5_en = ville['decors'][b5_val]['en']
    b12_cue = ville['decors'][b5_val]['cue']
    d9_str = f" and {d9}" if d9 != "none" else ""
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "none" else ""
    sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {ville['nom_fr']} during the {light_final}, with a {b8} atmosphere. "
        f"The camera uses a {cam_final} with a low-angle ground perspective. {b11_str}"
        f"MATERIAL WORLD & SHADING: All surfaces reimagined in {d8_val}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {sugar}. "
        f"LIGHTING: Soft cinematic bokeh, gentle god-rays. GROUND: {b10}. "
        f"PLATE CUES (STRICT): {b12_cue}. RULES: Pure background plate."
    )
    st.info("💡 PROMPT DÉCOR :")
    st.code(prompt_1)

# =========================================================
# ZONE 5 : ONGLET 2 - IMAGE (PERSONNAGES)
# =========================================================
with tab2:
    st.subheader("🎨 Mélo & Pipo (Image)")
    ic1, ic2 = st.columns(2)
    with ic1:
        am_final = st.text_input("ACTION MÉLO (A_M)", value=plan['AM'], disabled=not e7_bool)
        ap_final = st.text_input("ACTION PIPO (A_P)", value=plan['AP'], disabled=not e7_bool)
    with ic2:
        expr = st.selectbox("EXPRESSION", ["curious", "amazed", "smiling", "sleepy"], disabled=not e7_bool)
        acc = st.text_input("ACCESSOIRE", value="none", disabled=not e7_bool)

    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} ACTION: {am_final}. EXPRESSION: {expr}. ACCESSORY: {acc}. "
        f"{DNA_PIPO} ACTION: {ap_final}. "
        f"INTEGRATION: Placed in {e5_en} ({ville['nom_fr']}). Light: {light_final}. "
        f"Material: {MATERIAL_DNA}. {TECH_LOCKS}"
    )
    st.info("💡 PROMPT PERSONNAGES :")
    st.code(prompt_2)

# =========================================================
# ZONE 6 : MOTEUR DE RENDU (VERTEX AI)
# =========================================================
def render_melo(target_prompt):
    try:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        with st.spinner("Nanobanana Pro calcule votre plan..."):
            imgs = model.generate_images(prompt=target_prompt, number_of_images=1, aspect_ratio="16:9")
            st.image(imgs[0]._pil_image, use_column_width=True)
    except Exception as e:
        st.error(f"Erreur de rendu : {e}")

st.divider()
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 RENDU UNIQUE (ONGLET ACTIF)"):
        # Logique pour choisir quel prompt envoyer selon l'onglet visible
        render_melo(prompt_1) # Pour test, envoie le décor
