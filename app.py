import streamlit as st

# --- 1. ADN DES PERSONNAGES & VERROUS TECHNIQUES ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES DES LIEUX (Extraite de BASE_LIEUX) ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, blurry distant Eiffel Tower silhouette."},
    "mont_saint_michel": {"name": "Mont Saint Michel", "struct": "B", "obj": "Fishing net", "animal": "Sheep", "plate": "Vast wet sand, mirror reflections, distant island silhouette."},
    "santorini_greece": {"name": "Santorin", "struct": "A", "obj": "Wood flute", "animal": "White cat", "plate": "Simple white curved wall, dark sea, blurry blue dome."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, soft ripples, blurry palaces silhouettes."},
    "neuschwanstein_germany": {"name": "Château Neuschwanstein", "struct": "A", "obj": "Storybook", "animal": "Large stag", "plate": "Dark pine forest, mist, distant fairytale castle silhouette."},
    "fuji_japan": {"name": "Mont Fuji", "struct": "A", "obj": "Paper fan", "animal": "Snow monkey", "plate": "Still water, vast sky, distant triangular mountain silhouette."},
    "taj_mahal_india": {"name": "Taj Mahal", "struct": "A", "obj": "Oil lantern", "animal": "Blue peacock", "plate": "Symmetrical white marble, reflecting pool."},
    "giza_pyramids_egypt": {"name": "Pyramides de Gizeh", "struct": "A", "obj": "Golden compass", "animal": "Fennec fox", "plate": "Vast sand dunes, minimalist horizon."},
    "petra_jordan": {"name": "Petra", "struct": "A", "obj": "Sketchbook", "animal": "Camel", "plate": "Narrow red rock corridor, sliver of starry sky."},
    "lapland_arctic": {"name": "Laponie", "struct": "A", "obj": "Steaming mug", "animal": "Reindeer", "plate": "Vast white snowfield, aurora glow."}
}

# --- 3. LES 20 PLANS (Extraits de PLAN_DE_REALISATION) ---
PLANS = {
    1: {"angle": "Wide", "A_M": "Arrival", "A_P": "Floats next to Melo", "B_M": "Arrival (looks for Pipo)", "B_P": "Hides nearby", "C_M": "Departure on transport", "C_P": "Guides at the front"},
    2: {"angle": "Medium", "A_M": "Rubs eyes", "A_P": "Peeks playfully", "B_M": "Searching", "B_P": "Peeks from behind", "C_M": "Looks ahead", "C_P": "Guides gently"},
    3: {"angle": "Close-up", "A_M": "Watches Pipo glow", "A_P": "Glows softly", "B_M": "Walks on tiptoes", "B_P": "Teases at distance", "C_M": "Landscape drifts", "C_P": "Hovers close"},
    4: {"angle": "POV/Detail", "A_M": "Looks at a detail", "A_P": "Touches with magic", "B_M": "Sees a clue", "B_P": "Pops out", "C_M": "Follows light cue", "C_P": "Creates trails"},
    5: {"angle": "Medium", "A_M": "Reaches for light", "A_P": "Offers soft glow", "B_M": "Tries to catch Pipo", "B_P": "Dodges playfully", "C_M": "Drags paw in water/air", "C_P": "Leaves ribbon trail"},
    8: {"angle": "Medium", "A_M": "Uses the local {obj}", "A_P": "Reacts hovering", "B_M": "Uses the local {obj}", "B_P": "Circles the object", "C_M": "Plays with the local {obj}", "C_P": "Orbits calmly"},
    10: {"angle": "Close-up", "A_M": "Face in awe", "A_P": "Glows near Melo", "B_M": "Looks amazed", "B_P": "Levitates an item", "C_M": "Eyelids heavy", "C_P": "Lowers glow"},
    13: {"angle": "Close-up", "A_M": "Notices animal ({animal})", "A_P": "Stays quiet", "B_M": "Notices animal ({animal})", "B_P": "Stays quiet", "C_M": "Notices animal ({animal})", "C_P": "Stays quiet"},
    18: {"angle": "Close-up", "A_M": "Huge slow yawn", "A_P": "Stays very close", "B_M": "Huge slow yawn", "B_P": "Stays very close", "C_M": "Huge slow yawn", "C_P": "Stays very close"},
    20: {"angle": "Wide", "A_M": "Sleep", "A_P": "Dims to off", "B_M": "Sleep", "B_P": "Dims to off", "C_M": "Sleep", "C_P": "Dims to off"}
}
# (Note: Les plans manquants 6,7,9... peuvent être ajoutés sur le même modèle)

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo 160s Master", layout="wide")
st.title("🎬 Les Voyages de Mélo : Dashboard Intégral")

with st.sidebar:
    st.header("🌍 Géographie")
    l_id = st.selectbox("Lieu", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    
    st.header("🎬 Séquence")
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS.keys()))
    
    st.header("☁️ Ambiance (Contrôle Manuel)")
    meteo = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty", "Dusty"])
    heure = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night", "Dawn"])
    saison = st.selectbox("Saison", ["Spring", "Summer", "Autumn", "Winter"])

# --- 5. LOGIQUE DE RÉCUPÉRATION ---
lieu = LIEUX[l_id]
plan = PLANS[p_id]
s = lieu['struct']

# Actions formatées
melo_act = plan[f"{s}_M"].format(obj=lieu['obj'], animal=lieu['animal'])
pipo_act = plan[f"{s}_P"]

# --- 6. TABLEAU DE BORD D'ACTEURS ---
st.subheader(f"Plateau : {lieu['name']} | Plan {p_id} | Structure {s}")

col_act1, col_act2, col_act3 = st.columns(3)
with col_act1:
    st.metric("Action MÉLO", melo_act)
with col_act2:
    st.metric("Action PIPO", pipo_act)
with col_act3:
    st.metric("Angle Caméra", plan['angle'])

st.divider()

# --- 7. GÉNÉRATION DES PROMPTS ---
atmo = f"{heure}, {meteo}, {saison}."
weather_fx = "Wet surface reflections on Glass Suit." if "Rain" in meteo else ""

c1, c2, c3 = st.columns(3)

with c1:
    st.write("**1. Fond (Plate)**")
    p1 = f"Environment: {lieu['plate']} {atmo} POETIC, MINIMALIST. --ar 16:9"
    st.code(p1)

with c2:
    st.write("**2. Image (Nanobanana)**")
    p2 = f"Integration: {MELO_DNA} and {PIPO_DNA}. Melo is {melo_act}. Pipo is {pipo_act}. {plan['angle']}. {atmo} {weather_fx} [VERROUS]: {VERROUS}. --ar 16:9"
    st.code(p2)

with c3:
    st.write("**3. Vidéo (Veo 3)**")
    p3 = f"Animation (8s): Melo {melo_act} and Pipo {pipo_act}. Ultra-slow motion. {weather_fx} Inertia on ribbons. Soft light trails. Perfect loop."
    st.code(p3)

st.info(f"💡 Rappel Production : Pour {lieu['name']}, Mélo utilise l'objet '{lieu['obj']}' et croise un '{lieu['animal']}'.")
