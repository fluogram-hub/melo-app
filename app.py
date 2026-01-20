import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# 1. ADN & BIBLE B22 (LOCKS)
# =========================================================
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Melo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera perspective, ray-traced lighting."

# =========================================================
# 2. STRUCTURE DES DONNÉES (COQUE VIDE)
# =========================================================
# Ces dictionnaires sont les réceptacles. On ne les remplit pas ici.
DB_DECORS = {
    "votre_destination": {
        "nom_fr": "Exemple Destination", "landmark_en": "Landmark",
        "decors": {
            1: {"fr": "Lieu 1 FR", "en": "Lieu 1 EN", "cue": "Plate Cue 1"},
            2: {"fr": "Lieu 2 FR", "en": "Lieu 2 EN", "cue": "Plate Cue 2"},
            3: {"fr": "Lieu 3 FR", "en": "Lieu 3 EN", "cue": "Plate Cue 3"},
            4: {"fr": "Lieu 4 FR", "en": "Lieu 4 EN", "cue": "Plate Cue 4"}
        }
    }
}

PLANS_SEQ = {
    1: {"Angle": "wide-angle lens", "Light": "Golden Hour", "AM": "Melo Action", "AP": "Pipo Action", "Mode": "Perfect loop"},
    # La structure attend 20 entrées ici
}

MAT_MAP = {
    "🍭 SUCRERIES": {"Marshmallow foam": "Marshmallow foam", "Jelly candy": "Jelly candy"},
    "🧶 TEXTILES": {"Felted wool": "Felted wool"},
    "🧩 JOUETS": {"Lego": "Lego"}
}

# =========================================================
# 3. CONFIGURATION UI & SIDEBAR
# =========================================================
st.set_page_config(page_title="Melo Cockpit V67", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ ACTIVER MODE MANUEL (E7)", value=False)
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Logique de synchro
    ville = DB_DECORS[v_id]
    plan = PLANS_SEQ.get(p_id, {"Angle": "wide-angle lens", "Light": "Golden Hour", "AM": "...", "AP": "...", "Mode": "..."})
    auto_b5_id = ((p_id - 1) % 4) + 1

# =========================================================
# 4. COCKPIT PAR ONGLET
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR ---
with tab1:
    st.subheader(f"⚙️ Pilotage du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        # B5 (Lieu)
        b5_opts = list(ville['decors'].keys())
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", b5_opts, index=b5_opts.index(auto_b5_id) if auto_b5_id in b5_opts else 0, 
                              format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        # B6 (Angle)
        ang_opts = ["wide-angle lens", "medium framing", "macro lens", "ground perspective"]
        b6_idx = ang_opts.index(plan['Angle']) if plan['Angle'] in ang_opts else 0
        b6_val = st.selectbox("ANGLE (B6/I34)", ang_opts, index=b6_idx, disabled=not e7_bool)
    
    with c2:
        # B7 (Lumière)
        light_opts = ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"]
        b7_idx = light_opts.index(plan['Light']) if plan['Light'] in light_opts else 0
        b7_val = st.selectbox("LUMIÈRE (B7/I35)", light_opts, index=b7_idx, disabled=not e7_bool)
        b8_val = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
        b11_val = st.selectbox("1ER PLAN (B11)", ["none", "flowers", "leaves"], disabled=not e7_bool)
    
    with c3:
        cat_d8 = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8_name = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()), disabled=not e7_bool)
        d8_val = MAT_MAP[cat_d8][d8_name]
        d9_val = st.selectbox("MATÉRIEL D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10_val = st.text_input("SOL (B10)", value="dry and textured", disabled=not e7_bool)

    # --- FORMULE XLSX PROMPT 1 ---
    e5_en = ville['decors'][b5_val]['en']
    b12_cue = ville['decors'][b5_val]['cue']
    d9_str = f" and {d9_val}" if d9_val != "none" else ""
    b11_str = f"In the immediate foreground, a subtle {b11_val} adds volumetric depth; " if b11_val != "none" else ""
    sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {ville['nom_fr']} during the {b7_val}, with a {b8_val} atmosphere. "
        f"The camera uses a {b6_val}. {b11_str}"
        f"MATERIAL WORLD & SHADING: All reimagined in {d8_val}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {sugar}. "
        f"LIGHTING: Soft cinematic bokeh. GROUND: {b10_val}. "
        f"PLATE CUES (STRICT): {b12_cue}. RULES: Pure background plate."
    )
    st.info("📝 PROMPT DÉCOR :")
    st.code(prompt_1)

# --- ONGLET 2 : PERSONNAGES ---
with tab2:
    st.subheader(f"🎨 Pilotage Mélo & Pipo")
    ic1, ic2 = st.columns(2)
    with ic1:
        am_val = st.text_input("ACTION MÉLO (A_M)", value=plan['AM'], disabled=not e7_bool)
        expr_val = st.selectbox("EXPRESSION", ["curious", "smiling", "amazed", "sleepy"], disabled=not e7_bool)
    with ic2:
        ap_val = st.text_input("ACTION PIPO (A_P)", value=plan['AP'], disabled=not e7_bool)
        acc_val = st.text_input("ACCESSOIRE", value="none", disabled=not e7_bool)

    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} ACTION: {am_val}. EXPRESSION: {expr_val}. "
        f"{DNA_PIPO} ACTION: {ap_val}. INTEGRATION: Placed in {e5_en}. {TECH_LOCKS}"
    )
    st.info("📝 PROMPT PERSONNAGES :")
    st.code(prompt_2)

# --- ONGLET 3 : VIDÉO ---
with tab3:
    st.subheader("🎞️ Paramètres d'Animation")
    vc1, vc2 = st.columns(2)
    with vc1:
        v_mode = st.selectbox("MODE VIDÉO", ["Perfect loop", "Cinematic non-loop"], 
                              index=0 if plan['Mode'] == "Perfect loop" else 1, disabled=not e7_bool)
    with vc2:
        v_speed = st.selectbox("VITESSE", ["Ultra-slow", "Slow motion", "Real-time"], disabled=not e7_bool)
    
    prompt_3 = f"Video Animation: Melo {am_val}. Pipo {ap_val}. Mode: {v_mode}. Speed: {v_speed}."
    st.info("📝 PROMPT VIDÉO :")
    st.code(prompt_3)

# =========================================================
# 5. MOTEUR DE RENDU (VERTEX AI)
# =========================================================
def render_melo(prompt):
    try:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        with st.spinner("Calcul Nanobanana Pro..."):
            imgs = model.generate_images(prompt=prompt, number_of_images=1, aspect_ratio="16:9")
            st.image(imgs[0]._pil_image, use_column_width=True)
    except Exception as e:
        st.error(f"Erreur Vertex : {e}")

st.divider()
if st.button("🚀 RENDU UNIQUE (ONGLET ACTIF)"):
    # Envoyer le prompt correspondant à l'onglet sélectionné
    render_melo(prompt_1)
