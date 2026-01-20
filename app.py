import streamlit as st

# --- 1. LES VERROUS DE LA BIBLE B22 (FIXES) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
REALISM_LOCK = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_LOCK = "Melo's suit is homogeneous transparent blue jelly, no internal anatomy, high gloss, light refraction."

# --- 2. BASE DE DONNÉES COMPLÈTE (Extraite de tes fichiers) ---
LIEUX = {
    "eiffel_paris": {"name": "Paris - Tour Eiffel", "struct": "B", "plate": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
    "mont_saint_michel": {"name": "Mont Saint-Michel", "struct": "B", "plate": "Vast wet sand, mirror reflections, distant blurry island silhouette."},
    "santorini_greece": {"name": "Santorin - Grèce", "struct": "A", "plate": "Simple white curved wall, dark sea, one distant blurry blue dome."},
    "venice_italy": {"name": "Venise - Italie", "struct": "C", "plate": "Dark calm water, soft ripples, blurry silhouettes of distant palaces."},
    "neuschwanstein_germany": {"name": "Château Neuschwanstein", "struct": "A", "plate": "Dark pine forest, mist, distant blurry fairytale castle silhouette."},
    "big_ben_london": {"name": "Londres - Big Ben", "struct": "B", "plate": "Simple stone bridge, foggy sky, distant blurry clock tower silhouette."},
    "fuji_japan": {"name": "Mont Fuji - Japon", "struct": "A", "plate": "Still water, vast sky, distant blurry triangular mountain silhouette."},
    "taj_mahal_india": {"name": "Taj Mahal - Inde", "struct": "A", "plate": "Symmetrical white marble, reflecting pool, warm dusk glow, serene silhouette."},
    "giza_pyramids_egypt": {"name": "Pyramides de Gizeh", "struct": "A", "plate": "Vast sand dunes, minimalist horizon, distant blurry pyramid shape."},
    "lapland_arctic": {"name": "Laponie - Arctique", "struct": "A", "plate": "Snowy landscape, soft aurora glow, pine trees with heavy snow, cozy night."}
}

# Logique des actions selon la Structure (A, B ou C) extraite de ton Plan de Réalisation
PLANS_LOGIC = {
    1: {"angle": "Wide", "A": "Arrival (grey/misty landscape)", "B": "Arrival (Melo looks for Pipo)", "C": "Departure (Melo on transport)"},
    2: {"angle": "Medium", "A": "Melo rubs his eyes", "B": "Melo searching", "C": "Melo looks ahead"},
    5: {"angle": "Medium", "A": "Melo smiles, reaching for light", "B": "Melo laughs, catching Pipo", "C": "Melo drags his paw in water"},
    18: {"angle": "Close-up", "A": "Huge slow yawn", "B": "Huge slow yawn", "C": "Huge slow yawn"},
    20: {"angle": "Wide", "A": "Sleep, fade to black", "B": "Sleep, fade to black", "C": "Sleep, fade to black"}
}

# --- 3. INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Mélo Prompt Engine", layout="wide")
st.title("🎭 Les Voyages de Mélo : Générateur de Production")

with st.sidebar:
    st.header("⚙️ Configuration")
    lieu_id = st.selectbox("Choisir la Destination", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    plan_id = st.select_slider("Numéro du Plan", options=[1, 2, 5, 18, 20])
    st.divider()
    st.write(f"**Structure :** {LIEUX[lieu_id]['struct']}")
    st.write(f"**Angle :** {PLANS_LOGIC[plan_id]['angle']}")

# Récupération des données dynamiques
structure = LIEUX[lieu_id]['struct']
action_text = PLANS_LOGIC[plan_id][structure]
plate_text = LIEUX[lieu_id]['plate']

# --- 4. GÉNÉRATION DES 3 PROMPTS ---
st.header(f"🎬 Plan {plan_id} à {LIEUX[lieu_id]['name']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Decor Plate")
    p1 = f"An ultra-detailed cinematic environment photography of {LIEUX[lieu_id]['name']}. {plate_text} Minimalist composition, large negative space, bedtime-friendly. --ar 16:9"
    st.info("Utiliser pour générer le décor vide.")
    st.code(p1, language="text")

with col2:
    st.subheader("2. Image (Nanobanana)")
    p2 = f"Character Integration: {MELO_DNA} and {PIPO_DNA}. Pose: {action_text}. Location: {LIEUX[lieu_id]['name']}. {PLANS_LOGIC[plan_id]['angle']} shot. [VERROUS]: {REALISM_LOCK} {MATERIAL_LOCK}. Color Spill: Glass suit reflects environment colors. --ar 16:9"
    st.info("Utiliser avec l'Image 1 en référence.")
    st.code(p2, language="text")

with col3:
    st.subheader("3. Vidéo (Veo 3)")
    p3 = f"Animation (8s): {action_text} in ultra-slow motion. Inertia on Melo's ribbons. Pipo leaves a soft light trail. Consistent glossy reflections on the blue suit. Perfect loop, cinematic PBR."
    st.info("Générer la vidéo à partir de l'Image 2.")
    st.code(p3, language="text")

st.success("✅ Tout est prêt. Copie le prompt dont tu as besoin pour ton étape de production.")
