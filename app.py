import streamlit as st

# --- 1. BIBLE B22 & PARAMÈTRES TECHNIQUES ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long smooth blue ribbons."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
REALISM_LOCK = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. DONNÉES EXTRAITES DE TON EXCEL ---
LIEUX = {
    "eiffel_paris": {"name": "Paris - Tour Eiffel", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
    "mont_saint_michel": {"name": "Mont Saint-Michel", "struct": "B", "obj": "Fishing net", "animal": "Sheep", "plate": "Vast wet sand, mirror reflections, distant blurry island silhouette."},
    "santorini_greece": {"name": "Santorin - Grèce", "struct": "A", "obj": "Wood flute", "animal": "White cat", "plate": "Simple white curved wall, dark sea, one distant blurry blue dome."},
    "venice_italy": {"name": "Venise - Italie", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, soft ripples, blurry silhouettes of distant palaces."},
    "fuji_japan": {"name": "Mont Fuji - Japon", "struct": "A", "obj": "Paper fan", "animal": "Snow monkey", "plate": "Still water, vast sky, distant blurry triangular mountain silhouette."},
    "taj_mahal_india": {"name": "Taj Mahal - Inde", "struct": "A", "obj": "Lotus flower", "animal": "Peacock", "plate": "Symmetrical white marble, reflecting pool, warm dusk glow."},
    "lapland_arctic": {"name": "Laponie - Arctique", "struct": "A", "obj": "Wooden sled", "animal": "Reindeer", "plate": "Snowy landscape, soft aurora glow, pine trees with heavy snow."}
}

METEO_OPTIONS = ["Clear Sky", "Heavy Rain", "Soft Snow", "Foggy / Misty", "Dusty Storm"]
SAISONS = ["Spring", "Summer", "Autumn", "Winter"]
HEURES = ["Golden Hour", "Sunset", "Blue Hour", "Deep Night", "Dawn"]

PLANS_LOGIC = {
    1: {"angle": "Wide", "A": "Arrival in landscape", "B": "Melo looks for Pipo", "C": "Melo on transport"},
    2: {"angle": "Medium", "A": "Melo rubs his eyes", "B": "Melo searching", "C": "Melo looks ahead"},
    10: {"angle": "Detail", "A": "Melo touches the {obj}", "B": "Melo plays with {animal}", "C": "Melo follows a light trail"},
    18: {"angle": "Close-up", "A": "Melo makes a huge, slow yawn", "B": "Melo makes a huge, slow yawn", "C": "Melo makes a huge, slow yawn"},
    20: {"angle": "Wide", "A": "Sleep, fade to black", "B": "Sleep, fade to black", "C": "Sleep, fade to black"}
}

# --- 3. INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Mélo Production Hub", layout="wide")
st.title("🎭 Les Voyages de Mélo : Dashboard de Production")

with st.sidebar:
    st.header("🌍 Géographie")
    l_id = st.selectbox("Destination", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    
    st.header("☁️ Atmosphère")
    meteo = st.selectbox("Météo", METEO_OPTIONS)
    saison = st.selectbox("Saison", SAISONS)
    heure = st.selectbox("Moment de la journée", HEURES)
    
    st.header("🎬 Séquence")
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_LOGIC.keys()))

# --- 4. LOGIQUE DE GÉNÉRATION ---
lieu = LIEUX[l_id]
plan = PLANS_LOGIC[p_id]
struct = lieu['struct']

# Insertion de l'objet ou animal local si c'est le plan 10
action_raw = plan[struct]
action_final = action_raw.format(obj=lieu['obj'], animal=lieu['animal'])

# Construction des blocs de contexte
atmo_context = f"Atmosphere: {meteo} during {heure} in {saison}."
weather_effect = ""
if "Rain" in meteo: weather_effect = "Reflective wet surfaces, water droplets on Melo's glass suit."
if "Snow" in meteo: weather_effect = "Thin layer of frost and snow dust on the blue glass."

# --- 5. AFFICHAGE ---
st.header(f"Plan {p_id} : {lieu['name']}")
st.write(f"**Variables :** {meteo} | {heure} | {saison} | Structure {struct}")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Decor (Plate)")
    p1 = f"Environment Plate: {lieu['plate']} {atmo_context} Minimalist, bedtime-friendly, empty scene. --ar 16:9"
    st.code(p1, language="text")

with col2:
    st.subheader("2. Image (Nanobanana)")
    p2 = f"Character Integration: {MELO_DNA} and {PIPO_DNA}. Pose: {action_final}. {plan['angle']} shot. {atmo_context} {weather_effect} [VERROUS]: {REALISM_LOCK}. Glass suit reflects {heure} light. --ar 16:9"
    st.code(p2, language="text")

with col3:
    st.subheader("3. Vidéo (Veo 3)")
    p3 = f"Animation (8s): {action_final} in ultra-slow motion. {weather_effect} Particles moving slowly. Persistent glossy reflections on the blue suit. Perfect loop."
    st.code(p3, language="text")

st.divider()
st.write(f"**Notes de Production :** Ce plan utilise l'objet local : *{lieu['obj']}* et l'animal : *{lieu['animal']}*.")
