import streamlit as st

# --- 1. LA BIBLE B22 (CONSTANTES INVARIABLES) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
REALISM_LOCK = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_LOCK = "Melo's suit is homogeneous transparent blue jelly, no internal anatomy, high gloss, light refraction."

# --- 2. EXTRACTION DE TA BASE DE DONNÉES (Échantillon de tes fichiers) ---
# J'ai intégré ici les données extraites de tes fichiers BASE_LIEUX et DECORS
LIEUX = {
    "eiffel_paris": {"name": "Paris - Tour Eiffel", "struct": "B", "plate": "Empty stone esplanade, blurry distant Eiffel Tower silhouette, warm streetlamps bokeh."},
    "venice_italy": {"name": "Venise - Canaux", "struct": "C", "plate": "Dark calm water, soft ripples, blurry silhouettes of distant palaces, misty night."},
    "taj_mahal_india": {"name": "Inde - Taj Mahal", "struct": "A", "plate": "Symmetrical white marble, reflecting pool, warm dusk glow, serene silhouette."},
    "lapland_arctic": {"name": "Laponie - Igloo", "struct": "A", "plate": "Snowy landscape, soft aurora glow, pine trees with heavy snow, cozy night."}
}

# Logique simplifiée de ton PLAN_DE_REALISATION (Plans 1, 2, 18, 20)
PLANS = {
    1: {"angle": "Wide / Establishing", "action_A": "Arrival in misty landscape", "action_B": "Melo looks for Pipo", "action_C": "Melo on transport"},
    2: {"angle": "Medium shot", "action_A": "Melo rubs his eyes", "action_B": "Melo searching", "action_C": "Melo looks ahead"},
    18: {"angle": "Close-up", "action_A": "Huge slow yawn", "action_B": "Huge slow yawn", "action_C": "Huge slow yawn"},
    20: {"angle": "Wide shot", "action_A": "Sleep, fade to black", "action_B": "Sleep, fade to black", "action_C": "Sleep, fade to black"}
}

# --- 3. INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Mélo Generator", layout="wide")
st.title("🎭 Les Voyages de Mélo - Générateur de Prompts")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Configuration")
    lieu_key = st.selectbox("Destination", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    plan_id = st.number_input("Numéro du Plan (1-20)", min_value=1, max_value=20, value=1)
    
    # Récupération automatique des données liées
    struct = LIEUX[lieu_key]["struct"]
    action = PLANS.get(plan_id, PLANS[1])[f"action_{struct}"]
    angle = PLANS.get(plan_id, PLANS[1])["angle"]

    st.info(f"**Structure détectée :** {struct}\n\n**Action auto :** {action}")

# --- 4. LE MOTEUR DE GÉNÉRATION (LOGIQUE GENERATOR) ---
with col2:
    st.header("Prompts Générés")

    # PROMPT 1 : DECOR (Master Plate)
    p1 = f"An ultra-detailed cinematic environment photography of {LIEUX[lieu_key]['name']}. {LIEUX[lieu_key]['plate']} Minimalist composition, large negative space, bedtime-friendly. --ar 16:9"
    
    # PROMPT 2 : IMAGE (Nanobanana)
    p2 = f"Character Integration: {MELO_DNA} and {PIPO_DNA}. Pose: {action}. Location: {LIEUX[lieu_key]['name']}. {angle} perspective. [VERROUS]: {REALISM_LOCK} {MATERIAL_LOCK}. Color Spill: Glass suit reflects environment colors. --ar 16:9"

    # PROMPT 3 : VIDEO (Veo 3)
    p3 = f"Animation (8s): {action} in ultra-slow motion. Inertia on Melo's ribbons. Pipo leaves a soft light trail. Consistent glossy reflections on the blue suit. Perfect loop, cinematic PBR."

    st.subheader("1. Decor Plate (Fond)")
    st.code(p1)
    
    st.subheader("2. Image Prompt (Nanobanana)")
    st.code(p2)
    
    st.subheader("3. Vidéo Prompt (Veo 3)")
    st.code(p3)

if st.button("Copier tout pour la prod"):
    st.success("Logique de production validée pour ce plan !")
