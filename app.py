import streamlit as st

# --- 1. CONFIGURATION DE LA BIBLE B22 & LOCKS ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
REALISM_LOCK = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_LOCK = "Melo's suit is homogeneous transparent blue jelly, no internal anatomy, high gloss, light refraction."

# --- 2. BASE DE DONNÉES ÉTENDUE (Extraite de ton Excel) ---
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
    "petra_jordan": {"name": "Petra - Jordanie", "struct": "A", "plate": "Narrow red rock corridor, sliver of starry sky, deep shadows."},
    "statue_liberty_ny": {"name": "Statue de la Liberté - NY", "struct": "C", "plate": "Dark wooden ferry deck, foggy ocean, distant blurry torch light."},
    "machu_picchu_peru": {"name": "Machu Picchu - Pérou", "struct": "B", "plate": "Green grass slopes, fog, distant blurry peak silhouette."},
    "golden_gate_sf": {"name": "Golden Gate - San Francisco", "struct": "C", "plate": "Thick fog, distant blurry bridge tower, warm light."},
    "lapland_arctic": {"name": "Laponie - Arctique", "struct": "A", "plate": "Snowy landscape, soft aurora glow, pine trees with heavy snow."}
}

# Logique des plans (Extraite de PLAN_DE_REALISATION)
PLANS_LOGIC = {
    1: {"angle": "Wide / Establishing", "A": "Arrival (grey/misty landscape)", "B": "Arrival (Melo looks for Pipo)", "C": "Departure (Melo on transport)"},
    2: {"angle": "Medium shot", "A": "Melo rubs his eyes, looking for color", "B": "Melo searching", "C": "Melo looks ahead, steady"},
    3: {"angle": "Close-up", "A": "Melo watches Pipo glow", "B": "Melo walks on tiptoes, curious", "C": "Landscape drifts slowly behind Melo"},
    5: {"angle": "Medium shot", "A": "Melo smiles, reaching for light", "B": "Melo laughs, trying to catch Pipo", "C": "Melo drags his paw in water"},
    10: {"angle": "Detail / POV", "A": "Melo touches a local object", "B": "Melo investigates a clue", "C": "Melo follows a light trail"},
    18: {"angle": "Close-up", "A": "Melo makes a huge, slow yawn", "B": "Melo makes a huge, slow yawn", "C": "Melo makes a huge, slow yawn"},
    20: {"angle": "Wide / Final", "A": "Sleep, fade to black", "B": "Sleep, fade to black", "C": "Sleep, fade to black"}
}

# --- 3. INTERFACE ---
st.set_page_config(page_title="Mélo Engine Master", layout="wide")
st.title("🎭 Les Voyages de Mélo : Prompt Engine")

with st.sidebar:
    st.header("⚙️ Paramètres")
    lieu_id = st.selectbox("Destination", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    plan_id = st.select_slider("Numéro du Plan", options=list(PLANS_LOGIC.keys()))
    
    st.divider()
    st.write(f"**Structure :** {LIEUX[lieu_id]['struct']}")
    st.write(f"**Type d'Angle :** {PLANS_LOGIC[plan_id]['angle']}")

# Calcul des données
struct = LIEUX[lieu_id]['struct']
action = PLANS_LOGIC[plan_id][struct]
plate = LIEUX[lieu_id]['plate']

# --- 4. AFFICHAGE DES PROMPTS ---
st.header(f"Plan {plan_id} — {LIEUX[lieu_id]['name']}")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("1. Decor (Plate)")
    p1 = f"Ultra-detailed cinematic environment photography of {LIEUX[lieu_id]['name']}. {plate} Minimalist, large negative space, bedtime-friendly. --ar 16:9"
    st.code(p1, language="text")

with c2:
    st.subheader("2. Image (Nanobanana)")
    p2 = f"Character Integration: {MELO_DNA} and {PIPO_DNA}. Pose: {action}. {PLANS_LOGIC[plan_id]['angle']}. [VERROUS]: {REALISM_LOCK} {MATERIAL_LOCK}. Reflective mapping: Glass suit reflects {LIEUX[lieu_id]['name']} colors. --ar 16:9"
    st.code(p2, language="text")

with c3:
    st.subheader("3. Vidéo (Veo 3)")
    p3 = f"Animation (8s): {action} in ultra-slow motion. Inertia on Melo's ribbons. Pipo leaves a soft light trail. Persistent glossy reflections on the blue suit. Perfect loop, cinematic PBR."
    st.code(p3, language="text")

st.info("💡 Conseil : Utilise le Prompt 1 pour fixer ton décor, puis le Prompt 2 en 'Image-to-Image' pour intégrer Mélo.")
