import streamlit as st

# --- 1. CONSTANTES BIBLE B22 ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long smooth blue ribbons."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
REALISM_LOCK = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES LIEUX & DÉCORS (Extraite de BASE_LIEUX) ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "decor": "Le Trocadéro", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, blurry distant Eiffel Tower silhouette."},
    "mont_saint_michel": {"name": "Mont Saint-Michel", "struct": "B", "decor": "La Baie", "obj": "Fishing net", "animal": "Sheep", "plate": "Vast wet sand, mirror reflections, distant blurry island silhouette."},
    "santorini_greece": {"name": "Santorin", "struct": "A", "decor": "Les Murs Blancs", "obj": "Wood flute", "animal": "White cat", "plate": "Simple white curved wall, dark sea, blurry blue dome."},
    "venice_italy": {"name": "Venise", "struct": "C", "decor": "Le Grand Canal", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, soft ripples, blurry distant palaces."},
    "taj_mahal_india": {"name": "Taj Mahal", "struct": "A", "decor": "La Terrasse de Marbre", "obj": "Lotus flower", "animal": "Peacock", "plate": "Symmetrical white marble, reflecting pool, warm dusk glow."}
}

# --- 3. LES 20 PLANS (Extraits de PLAN_DE_REALISATION) ---
PLANS_DATA = {
    1: {"angle": "Wide", "A": "Arrival, misty landscape", "B": "Arrival, searching for Pipo", "C": "Arrival on transport"},
    2: {"angle": "Medium", "A": "Melo rubs eyes", "B": "Melo searching behind corner", "C": "Melo looks ahead steady"},
    3: {"angle": "Close-up", "A": "Pipo glows softly", "B": "Melo walks on tiptoes", "C": "Landscape drifts behind Melo"},
    4: {"angle": "POV", "A": "Melo looks at a detail", "B": "Melo sees a clue", "C": "Melo follows a light cue"},
    5: {"angle": "Medium", "A": "Melo reaches for light", "B": "Melo laughs with Pipo", "C": "Melo drags paw in water"},
    10: {"angle": "Detail", "A": "Melo touches the {obj}", "B": "Melo plays with {animal}", "C": "Melo investigates {obj}"},
    15: {"angle": "Medium", "A": "Melo looks at landmark twinkle", "B": "Landmark sparkles", "C": "Transport stops gently"},
    18: {"angle": "Close-up", "A": "Melo huge slow yawn", "B": "Melo huge slow yawn", "C": "Melo huge slow yawn"},
    20: {"angle": "Wide", "A": "Sleep, fade to black", "B": "Sleep, fade to black", "C": "Sleep, fade to black"}
}
# Note: Tu peux ajouter les autres numéros (6,7,8...) sur le même modèle.

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Production Hub", layout="wide")
st.title("🎭 Dashboard de Production : Les Voyages de Mélo")

with st.sidebar:
    st.header("📍 Localisation")
    l_id = st.selectbox("Lieu", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    
    st.header("☁️ Ambiance")
    meteo = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty", "Dusty"])
    saison = st.selectbox("Saison", ["Spring", "Summer", "Autumn", "Winter"])
    heure = st.selectbox("Moment", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
    
    st.header("🎬 Séquence")
    p_id = st.selectbox("Numéro du Plan", list(PLANS_DATA.keys()))

# --- 5. CALCUL DES PROMPTS ---
lieu = LIEUX[l_id]
plan = PLANS_DATA[p_id]
struct = lieu['struct']
action = plan[struct].format(obj=lieu['obj'], animal=lieu['animal'])

atmo = f"{meteo}, {heure}, {saison}."
wet_effect = "Water droplets and reflections on Glass Suit." if "Rain" in meteo else ""

# --- 6. AFFICHAGE ---
st.info(f"Cible : **{lieu['name']}** | Plan **{p_id}** ({plan['angle']}) | Structure **{struct}**")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Decor (Plate)")
    p1 = f"Environment Plate: {lieu['plate']} {atmo} POETIC, MINIMALIST, empty scene. --ar 16:9"
    st.code(p1)

with col2:
    st.subheader("2. Image (Nanobanana)")
    p2 = f"Character Integration: {MELO_DNA} and {PIPO_DNA}. Pose: {action}. {atmo} {wet_effect} [VERROUS]: {REALISM_LOCK}. Glass suit reflects {heure} environment. --ar 16:9"
    st.code(p2)

with col3:
    st.subheader("3. Vidéo (Veo 3)")
    p3 = f"Animation (8s): {action} in ultra-slow motion. {wet_effect} Inertia on ribbons. Pipo soft light trail. Perfect loop, cinematic PBR."
    st.code(p3)

st.write(f"📖 **Story Context:** Dans ce plan, Mélo interagit avec : **{lieu['obj']}**.")
