import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# 1. IDENTITÉ VISUELLE (B22 - LOCK GLOBAL)
# =========================================================
B22_IDENTITY_LOCK = """MÉLO (LOCK — DO NOT CHANGE):
- MÉLO: Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws.
- Same face, proportions, materials
- Wearing a blue glass suit (transparent blue glass effect), ultra glossy.
- Rounded child proportions.
- Keep ears visibility consistent.

PIPO (LOCK — DO NOT CHANGE):
- microscopic snow-potato companion; white with subtle iridescent reflections.
- Dot eyes and small smile; not an animal.
- Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo.
- Soft constant glow; bedtime-friendly, minimal."""

# =========================================================
# 2. STRUCTURE DES DONNÉES (COQUE PRÊTE)
# =========================================================
DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)",
        "decors": {
            1: {"fr": "Les Quais de Seine", "en": "Seine riverbanks", "cue": "Ultra-realistic cinematic PBR environment plate... Specific setting: Les Quais de Seine."},
        }
    }
}

PLANS_SEQ = {
    1: {
        "Angle": "Establishing wide shot", "Time": "morning", "Weather": "heavy rain", "Season": "summer",
        "M_Pose": "Melo sat on ground facing the camera, left arm raised, looking at Pipo",
        "M_Expr": "gentle connection with Pipo",
        "P_Act": "Pipo floats gently in the air and waves hello.",
        "P_Pos": "Pipo very close to Melo",
        "Acc": "flower", "Palette": "Dreamy Pastel", "P_Col": "Warm glow", "Trail": "sparkling dust trail",
        "V_Mode": "Non-loop cinematic", "V_Act": "Simple gesture", "V_M_Mvt": "Slow walk (few steps)",
        "V_P_Mvt": "Slow circular float", "V_Cam": "Slow orbit around subject", "V_Env": "Tiny floating dust particles", "V_Trans": "None"
    }
}

MAT_MAP = {
    "🍭 SUCRERIES": {"Translucent colored jelly candy (glossy)": "Translucent colored jelly candy (glossy)"},
    "✨ ACCENTS": {"Crystal sugar glow": "Crystal sugar glow"}
}

# =========================================================
# 3. INTERFACE & SIDEBAR
# =========================================================
st.set_page_config(page_title="Melo Logic Engine V70", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    mode_manuel = st.toggle("🕹️ ACTIVER CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    st.divider()
    v_id = st.selectbox("DESTINATION (LieuKey)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DB_DECORS[v_id]
    plan = PLANS_SEQ.get(p_id, PLANS_SEQ[1])

# =========================================================
# 4. ONGLETS COCKPIT
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (ENV)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR ---
with tab1:
    st.subheader("⚙️ Paramètres du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_val = st.selectbox("DÉCOR (E5)", list(ville['decors'].keys()), format_func=lambda x: ville['decors'][x]['fr'], disabled=not mode_manuel)
        b6_val = st.selectbox("ANGLE (B6/I34)", ["Establishing wide shot", "Medium shot", "Close-up"], index=0, disabled=not mode_manuel)
        b9_val = st.selectbox("SAISON (B9)", ["summer", "winter", "spring", "autumn"], index=0, disabled=not mode_manuel)
    with c2:
        b7_val = st.selectbox("TIME OF DAY (B7/I35)", ["morning", "sunset", "night"], index=0, disabled=not mode_manuel)
        b8_val = st.selectbox("WEATHER (B8)", ["heavy rain", "clear sky", "soft mist", "snow"], index=0, disabled=not mode_manuel)
        b11_val = st.selectbox("1ER PLAN (B11)", ["none", "wild flowers"], disabled=not mode_manuel)
    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", list(MAT_MAP["🍭 SUCRERIES"].keys()), disabled=not mode_manuel)
        d9_val = st.selectbox("MATÉRIEL D9", ["none", "Crystal sugar glow"], disabled=not mode_manuel)
        b10_val = st.text_input("ÉTAT DU SOL (B10)", value="paved", disabled=not mode_manuel)

    # --- FORMULE PROMPT 1 ---
    e5_en = f"{v_id} – {ville['decors'][b5_val]['en']}"
    b12_cue = ville['decors'][b5_val]['cue']
    d9_str = f" and {d9_val}" if d9_val != "none" else ""
    b11_str = f"In the immediate foreground, a subtle {b11_val} adds volumetric depth; " if b11_val != "none" else ""
    sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {b9_val} during the {b7_val}, with a {b8_val} atmosphere. "
        f"The camera uses a {b6_val} with a low-angle ground perspective. {b11_str}"
        f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8_val}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {sugar}. "
        f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant, soft-focus silhouette. "
        f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays, bedtime-friendly calm palette. "
        f"GROUND DETAIL: The ground is {b10_val} with high-tactile micro-textures. "
        f"PLATE CUES (STRICT): {b12_cue}. RULES: No characters, no people, no text. Pure background plate."
    )
    st.code(prompt_1)

# --- ONGLET 2 : IMAGE ---
with tab2:
    st.subheader("🎨 Intégration Personnages")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        s_pose = st.text_area("Pose Mélo", value=plan['M_Pose'], disabled=not mode_manuel)
        s_expr = st.text_area("Expression", value=plan['M_Expr'], disabled=not mode_manuel)
    with r2:
        s_p_act = st.text_area("Pipo Action", value=plan['P_Act'], disabled=not mode_manuel)
        s_p_pos = st.selectbox("Pipo Position", ["Pipo very close to Melo"], disabled=not mode_manuel)
    with r3:
        s_acc = st.text_input("Accessoire Mélo", value=plan['Acc'], disabled=not mode_manuel)
        s_pal = st.selectbox("Palette", ["Dreamy Pastel", "Vibrant"], disabled=not mode_manuel)
    with r4:
        s_pcol = st.selectbox("Couleur Pipo", ["Warm glow", "White"], disabled=not mode_manuel)
        s_trail = st.selectbox("Energy Trail", ["sparkling dust trail", "none"], disabled=not mode_manuel)

    # --- LOGIQUE MÉTÉO (CORRECTIF 2) ---
    weather_interaction = ""
    rain_keywords = ["rain", "snow", "mist", "frost", "drizzle", "storm", "humid"]
    if any(word in b8_val.lower() for word in rain_keywords):
        weather_interaction = f"Add realistic water droplets or frost streaks on Mélo's glossy glass suit that reflect the {b7_val} light."

    prompt_2 = (
        f"IMAGE COMPOSITING TASK: Using Image 3 as static background, integrate Mélo (Image 1) and Pipo (Image 2).\n\n"
        f"1. IDENTITY LOCK: Reference Specs: {B22_IDENTITY_LOCK}. Mélo accessory: {s_acc}.\n"
        f"2. LIGHTING: AMBIENT MATCHING: Apply the '{s_pal}' palette. Environment light must bounce onto Mélo’s glass suit. "
        f"ENVIRONMENT MATERIAL: {d8_val}. Pipo glow: {s_pcol}. Pipo trail: {s_trail}.\n"
        f"3. PHYSICAL INTERACTION: CONDITION: {b8_val}. OVERLAY: Visible falling {b8_val} in front/behind characters. {weather_interaction}\n"
        f"4. SCENE DIRECTION: Pose: {s_pose}. Expression: {s_expr}. Pipo: {s_p_act} near Mélo's head at {s_p_pos}."
    )
    st.code(prompt_2)

# --- ONGLET 3 : VIDÉO ---
with tab3:
    st.subheader("🎞️ Paramètres Vidéo")
    v1, v2 = st.columns(2)
    with v1:
        vm = st.selectbox("Mode", ["Non-loop cinematic", "Perfect loop"], disabled=not mode_manuel)
        va = st.selectbox("Action", ["Simple gesture", "Still pose"], disabled=not mode_manuel)
    with v2:
        vmm = st.selectbox("Mouvement Mélo", ["Slow walk (few steps)", "Breathing only"], disabled=not mode_manuel)
        vpm = st.selectbox("Mouvement Pipo", ["Slow circular float", "Hovering gently"], disabled=not mode_manuel)

    # --- FORMULE PROMPT 3 (CORRECTIF 3) ---
    prompt_3 = (
        f"VIDEO GENERATION PROMPT (FLOW / VEO3)\nMODE: Animate existing pixels. No reinterpretation.\n"
        f"SCENE LOCK: Angle: {b6_val}. Time: {b7_val}. Pipo trail: {s_trail}.\n"
        f"REALISM LOCK: Environment material: {d8_val}.\n"
        f"VIDEO SETTINGS: Duration: 8s. Mode: {vm}. Action: {va}. Melo: {vmm}. Pipo: {vpm}.\n"
        f"LOOP RULES: If mode = Perfect loop, motion must be continuous and seamless."
    )
    st.code(prompt_3)
