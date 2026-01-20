import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# 1. ADN & VERROUS TECHNIQUES (B22)
# =========================================================
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit (transparent blue glass effect), ultra glossy, white round belly. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; iridescent, tiny scale (5-10% of Melo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera perspective, ray-traced lighting."

# =========================================================
# 2. BIBLIOTHÈQUE DE MATÉRIAUX (D8 / D9)
# =========================================================
MAT_MAP = {
    "🍭 SUCRERIES": {
        "Marshmallow foam": "Marshmallow foam (matte soft), squishy",
        "Translucent jelly candy (glossy)": "Translucent jelly candy (glossy), subsurface scattering",
        "Hard candy (polished)": "Hard candy (polished smooth)",
        "Fondant sugar paste": "Fondant sugar paste (matte)"
    },
    "🧶 TEXTILES": {
        "Felted wool fabric": "Felted wool fabric, soft fibers",
        "Velvet microfabric": "Velvet microfabric, deep sheen",
        "Cotton quilted padding": "Cotton quilted padding, soft seams"
    },
    "🧩 JOUETS": {
        "Lego": "Lego plastic ABS, high gloss",
        "Soft clay (matte)": "Soft clay (matte), hand-molded",
        "Toy wood": "Polished toy wood, rounded edges"
    }
}

# =========================================================
# 3. BASE DE DONNÉES LIEUX & PLANS (EXTRAIT SYNC XLSX)
# =========================================================
DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)", "landmark_en": "Eiffel Tower",
        "decors": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Eiffel Tower clearly recognizable, warm distant streetlamps bokeh. Specific setting: Le Trocadéro."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine banks", "cue": "Eiffel Tower silhouette, river reflections. Specific setting: Les Quais de Seine."},
            3: {"fr": "Au pied de la Tour", "en": "The foot of the Tower", "cue": "Industrial metallic structure, massive iron beams. Specific setting: Au pied de la Tour."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ-de-Mars Lawn", "cue": "Large grass area, distant tower silhouette. Specific setting: Pelouse du Champ-de-Mars."}
        }
    } # Structure prête pour les 19 autres
}

# Séquence de réalisation 1-20
PLANS_SEQ = {
    1: {"Angle": "wide-angle lens", "Light": "Golden Hour", "AM": "Arrival (misty landscape)", "AP": "floats next to Melo"},
    2: {"Angle": "medium framing", "Light": "Golden Hour", "AM": "rubs eyes, looking for color", "AP": "peeks playfully"},
    3: {"Angle": "static close-up", "Light": "Sunset", "AM": "watches Pipo glow", "AP": "glows softly, ready to help"},
    10: {"Angle": "macro lens", "Light": "Blue Hour", "AM": "face in awe, lit by color", "AP": "glows near Melo"},
    20: {"Angle": "wide shot", "Light": "Night", "AM": "Sleep / fade to black", "AP": "dims to near-off"}
}

# =========================================================
# 4. CONFIGURATION UI & SIDEBAR
# =========================================================
st.set_page_config(page_title="Melo Cockpit Total V66", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ ACTIVER MODE MANUEL (E7)", value=False)
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Calculs de synchro
    ville = DB_DECORS[v_id]
    plan = PLANS_SEQ.get(p_id, PLANS_SEQ[1]) # Fallback sur plan 1
    auto_b5_id = ((p_id - 1) % 4) + 1

# =========================================================
# 5. SYSTÈME D'ONGLETS INTÉGRÉS
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR ---
with tab1:
    st.write(f"### ⚙️ Pilotage du Décor — {ville['nom_fr']}")
    c1, c2, c3 = st.columns(3)
    with c1:
        # B5 (Lieu)
        b5_opts = list(ville['decors'].keys())
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", b5_opts, index=b5_opts.index(auto_b5_id), 
                              format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        # B6 (Angle)
        ang_opts = ["wide-angle lens", "medium framing", "macro lens", "static close-up", "ground perspective"]
        b6_idx = ang_opts.index(plan['Angle']) if plan['Angle'] in ang_opts else 0
        b6_val = st.selectbox("ANGLE (B6/I34)", ang_opts, index=b6_idx, disabled=not e7_bool)
    
    with c2:
        # B7 (Lumière)
        light_opts = ["Golden Hour", "Sunset", "Blue Hour", "Night", "Soft Moonlight"]
        b7_idx = light_opts.index(plan['Light']) if plan['Light'] in light_opts else 0
        b7_val = st.selectbox("LUMIÈRE (B7/I35)", light_opts, index=b7_idx, disabled=not e7_bool)
        b8_val = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
    
    with c3:
        cat_d8 = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8_name = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()), disabled=not e7_bool)
        d8_val = MAT_MAP[cat_d8][d8_name]
        d9_val = st.selectbox("MATÉRIEL D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)

    # --- FORMULE XLSX PROMPT 1 ---
    e5_en = ville['decors'][b5_val]['en']
    b12_cue = ville['decors'][b5_val]['cue']
    d9_str = f" and {d9_val}" if d9_val != "none" else ""
    sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {ville['nom_fr']} during the {b7_val}, with a {b8_val} atmosphere. "
        f"The camera uses a {b6_val}. MATERIAL WORLD & SHADING: All surfaces reimagined in {d8_val}{d9_str}. "
        f"Surfaces feature {sugar}. PLATE CUES (STRICT): {b12_cue}. RULES: Pure background plate."
    )
    st.code(prompt_1)

# --- ONGLET 2 : PERSONNAGES ---
with tab2:
    st.write(f"### 🎨 Pilotage Mélo & Pipo — Plan {p_id}")
    ic1, ic2 = st.columns(2)
    with ic1:
        am_val = st.text_input("ACTION MÉLO (A_M)", value=plan['AM'], disabled=not e7_bool)
        expr_val = st.selectbox("EXPRESSION", ["curious", "smiling", "amazed", "sleepy"], disabled=not e7_bool)
    with ic2:
        ap_val = st.text_input("ACTION PIPO (A_P)", value=plan['AP'], disabled=not e7_bool)
        acc_val = st.text_input("ACCESSOIRE", value="none", disabled=not e7_bool)

    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} ACTION: {am_val}. EXPRESSION: {expr_val}. ACCESSORY: {acc_val}. "
        f"{DNA_PIPO} ACTION: {ap_val}. INTEGRATION: Placed in {e5_en}. {TECH_LOCKS}"
    )
    st.code(prompt_2)

# --- ONGLET 3 : VIDÉO ---
with tab3:
    st.write("### 🎞️ Paramètres d'Animation")
    vc1, vc2 = st.columns(2)
    with vc1:
        v_mode = st.selectbox("MODE VIDÉO", ["Perfect loop", "Cinematic non-loop"], disabled=not e7_bool)
    with vc2:
        v_speed = st.selectbox("VITESSE", ["Ultra-slow", "Slow motion", "Real-time"], disabled=not e7_bool)
    
    prompt_3 = f"Cinematic Animation (8s): Melo {am_val}. Pipo {ap_val}. Style: {v_mode}. Speed: {v_speed}."
    st.code(prompt_3)

# =========================================================
# 6. MOTEUR DE RENDU (VERTEX AI)
# =========================================================
def render_melo(prompt):
    creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    with st.spinner("Nanobanana Pro calcule votre image..."):
        imgs = model.generate_images(prompt=prompt, number_of_images=1, aspect_ratio="16:9")
        st.image(imgs[0]._pil_image, use_column_width=True)

st.divider()
if st.button("🚀 LANCER RENDU (DECOR)"):
    render_melo(prompt_1)
