import streamlit as st

# --- 1. PARAMÈTRES TECHNIQUES FIXES (Bible B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
REALISM_LOCK = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_LOCK = "Melo's suit is homogeneous transparent blue jelly, no internal anatomy, high gloss, light refraction."

# --- 2. TOUS LES LIEUX (Extraits de BASE_LIEUX) ---
LIEUX = {
    'eiffel_paris': {'name': 'Paris - Tour Eiffel', 'struct': 'B', 'obj': 'Red beret', 'animal': 'Poodle', 'plate': 'Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette.'},
    'mont_saint_michel': {'name': 'Mont Saint Michel', 'struct': 'B', 'obj': 'Fishing net', 'animal': 'Sheep', 'plate': 'Vast wet sand, mirror reflections, distant blurry island silhouette.'},
    'santorini_greece': {'name': 'Santorin - Grèce', 'struct': 'A', 'obj': 'Wood flute', 'animal': 'White cat', 'plate': 'Simple white curved wall, dark sea, one distant blurry blue dome.'},
    'venice_italy': {'name': 'Venise - Italie', 'struct': 'C', 'obj': 'Cat mask', 'animal': 'White pigeon', 'plate': 'Dark calm water, soft ripples, blurry silhouettes of distant palaces.'},
    'neuschwanstein_germany': {'name': 'Château Neuschwanstein', 'struct': 'A', 'obj': 'Storybook', 'animal': 'Large stag', 'plate': 'Dark pine forest, mist, distant blurry fairytale castle silhouette.'},
    'big_ben_london': {'name': 'Londres - Big Ben', 'struct': 'B', 'obj': 'Umbrella', 'animal': 'Red fox', 'plate': 'Simple stone bridge, foggy sky, distant blurry clock tower silhouette.'},
    'fuji_japan': {'name': 'Mont Fuji - Japon', 'struct': 'A', 'obj': 'Paper fan', 'animal': 'Snow monkey', 'plate': 'Still water, vast sky, distant blurry triangular mountain silhouette.'},
    'taj_mahal_india': {'name': 'Taj Mahal - Inde', 'struct': 'A', 'obj': 'Oil lantern', 'animal': 'Blue peacock', 'plate': 'Symmetrical white marble, reflecting pool, warm dusk glow.'},
    'giza_pyramids_egypt': {'name': 'Pyramides de Gizeh', 'struct': 'A', 'obj': 'Golden compass', 'animal': 'Fennec fox', 'plate': 'Vast sand dunes, minimalist horizon, distant blurry pyramid shape.'},
    'lapland_arctic': {'name': 'Laponie - Arctique', 'struct': 'A', 'obj': 'Steaming mug', 'animal': 'Reindeer', 'plate': 'Vast white snowfield, simple snowy pine silhouettes, aurora glow.'}
}

# --- 3. LES 20 PLANS COMPLETS (Extraits de PLAN_DE_REALISATION) ---
PLANS_DATA = {
    1: {'angle': 'Wide', 'A': 'Arrival (grey/misty landscape)', 'B': 'Arrival (Melo looks for Pipo)', 'C': 'Departure (Melo on transport)'},
    2: {'angle': 'Medium', 'A': 'Melo rubs his eyes, looking for color', 'B': 'Melo rubs his eyes, searching', 'C': 'Melo looks ahead, steady'},
    3: {'angle': 'Close-up', 'A': 'Pipo glows softly, ready to help', 'B': 'Melo walks on tiptoes, curious', 'C': 'Landscape drifts slowly behind Melo'},
    4: {'angle': 'POV/Detail', 'A': 'Melo looks at a small detail', 'B': 'Melo sees a clue in the decor', 'C': 'Melo follows a light cue'},
    5: {'angle': 'Medium', 'A': 'Melo smiles, reaching for light', 'B': 'Melo laughs, trying to catch Pipo', 'C': 'Melo drags his paw through air/water'},
    6: {'angle': 'Wide', 'A': 'Melo watches Pipo fly away', 'B': 'Melo searches the space', 'C': 'Melo passes under a bridge/tunnel'},
    7: {'angle': 'Detail', 'A': 'Melo notices the sky changing', 'B': 'Melo peeks through a hole (POV)', 'C': 'Melo follows a small glow'},
    8: {'angle': 'Medium', 'A': 'Melo uses the {obj}', 'B': 'Melo uses the {obj}', 'C': 'Melo plays with the {obj}'},
    9: {'angle': 'Wide', 'A': 'Melo watches the monument shift', 'B': 'Melo enters a calmer space', 'C': 'Melo slows down, observing'},
    10: {'angle': 'Close-up', 'A': 'Melo face in awe, lit by color', 'B': 'Melo looks amazed, then calmer', 'C': 'Melo eyelids getting heavy'},
    11: {'angle': 'Wide', 'A': 'Melo watches the sky', 'B': 'Melo and Pipo take a quiet break', 'C': 'Melo sees the landmark in distance'},
    12: {'angle': 'Wide', 'A': 'Melo slows, everything softens', 'B': 'Melo stops, game ends calmly', 'C': 'Melo approaches the landmark slowly'},
    13: {'angle': 'Close-up', 'A': 'Melo notices a small animal ({animal}) asleep', 'B': 'Melo notices a small animal ({animal}) asleep', 'C': 'Melo notices a small animal ({animal}) asleep'},
    14: {'angle': 'Medium', 'A': 'Melo stands calmly', 'B': 'Melo stands calmly', 'C': 'Melo relaxes'},
    15: {'angle': 'Detail', 'A': 'Melo looks at the landmark twinkle', 'B': 'Melo looks at the landmark sparkle', 'C': 'Melo reaches the transport stop'},
    16: {'angle': 'Medium', 'A': 'Melo prepares a sleeping spot', 'B': 'Melo finds a cozy corner', 'C': 'Melo settles down to sleep'},
    17: {'angle': 'Close-up', 'A': 'Melo relaxes', 'B': 'Melo relaxes', 'C': 'Melo relaxes'},
    18: {'angle': 'Close-up', 'A': 'Melo makes a huge, slow yawn', 'B': 'Melo makes a huge, slow yawn', 'C': 'Melo makes a huge, slow yawn'},
    19: {'angle': 'Wide', 'A': 'Final peaceful landscape', 'B': 'Final peaceful landscape', 'C': 'Final peaceful landscape'},
    20: {'angle': 'Wide', 'A': 'Sleep / fade to black', 'B': 'Sleep / fade to black', 'C': 'Sleep / fade to black'}
}

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo 160s Production", layout="wide")
st.title("🎬 Les Voyages de Mélo : Générateur 160 Secondes")

with st.sidebar:
    st.header("📍 Lieu du Film")
    l_id = st.selectbox("Destination (Reste sur la même pour 160s)", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    
    st.header("🎬 Progression (Plan 1 à 20)")
    p_id = st.select_slider("Choisir la séquence", options=list(PLANS_DATA.keys()))
    
    st.header("☁️ Météo & Temps")
    meteo = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Foggy"])
    heure = st.selectbox("Heure", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
    saison = st.selectbox("Saison", ["Spring", "Summer", "Autumn", "Winter"])

# --- 5. LOGIQUE ---
lieu = LIEUX[l_id]
plan = PLANS_DATA[p_id]
struct = lieu['struct']
# Remplacement dynamique des objets/animaux
action = plan[struct].format(obj=lieu['obj'], animal=lieu['animal'])

atmo = f"{meteo}, {heure}, {saison}."
weather_fx = "Wet reflections and droplets on Glass Suit." if "Rain" in meteo else ""

# --- 6. AFFICHAGE DES PROMPTS ---
st.success(f"Production en cours : **{lieu['name']}** | Plan **{p_id}/20**")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Decor Plate")
    p1 = f"Environment: {lieu['plate']} {atmo} POETIC, MINIMALIST. --ar 16:9"
    st.code(p1)

with col2:
    st.subheader("2. Image (Nanobanana)")
    p2 = f"Integration: {MELO_DNA} and {PIPO_DNA}. Action: {action}. {plan['angle']}. {atmo} {weather_fx} [VERROUS]: {REALISM_LOCK}. --ar 16:9"
    st.code(p2)

with col3:
    st.subheader("3. Vidéo (Veo 3)")
    p3 = f"Animation (8s): {action} in ultra-slow motion. {weather_fx} Inertia on ribbons. Pipo trail. Loopable cinematic PBR."
    st.code(p3)
