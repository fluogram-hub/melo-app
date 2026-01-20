import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES (4 DÉCORS PAR DESTINATION) ---
DESTINATIONS = {
    "eiffel_paris": {
        "name": "Paris - Tour Eiffel", "struct": "B", "obj": "Béret rouge", "animal": "Caniche",
        "decors": {
            1: {"name": "Le Trocadéro", "plate": "Eiffel Tower silhouette, stone esplanade, warm bokeh."},
            2: {"name": "Les Quais de Seine", "plate": "River reflections, cobble stones, Eiffel Tower behind."},
            3: {"name": "Le Pied de la Tour", "plate": "Close-up iron lattice, low angle ground view."},
            4: {"name": "Le Champ-de-Mars", "plate": "Soft green grass, distant tower silhouette."}
        }
    },
    "venice_italy": {
        "name": "Venise - Italie", "struct": "C", "obj": "Masque de chat", "animal": "Pigeon blanc",
        "decors": {
            1: {"name": "Le Grand Canal", "plate": "Dark ripples, gondola silhouette, historic palaces."},
            2: {"name": "Le Pont des Soupirs", "plate": "Narrow canal, stone bridge, soft reflections."},
            3: {"name": "Place Saint-Marc", "plate": "Paved square, Byzantine arches, blue hour light."},
            4: {"name": "Banc face à l'eau", "plate": "Wooden bench, water surface, distant blurry lights."}
        }
    }
}

# --- 3. LES 20 PLANS (ACTIONS RÉELLES - EXTRAIT EXCEL) ---
PLANS_DATA = {
    1: {"angle": "Wide", "light": "Golden Hour", "A": "Arrival (misty)", "B": "Arrival (searching Pipo)", "C": "Departure (on transport)"},
    2: {"angle": "Medium", "light": "Golden Hour", "A": "Rubs eyes", "B": "Rubs eyes, searching", "C": "Looks ahead steady"},
    3: {"angle": "Close-up", "light": "Sunset", "A": "Watches Pipo glow", "B": "Walks on tiptoes", "C": "Landscape drifts behind"},
    4: {"angle": "POV", "light": "Sunset", "A": "Looks at detail", "B": "Sees a clue", "C": "Follows light cue"},
    5: {"angle": "Medium", "light": "Sunset", "A": "Reaches for light", "B": "Laughs with Pipo", "C": "Drags paw in water"},
    6: {"angle": "Wide", "light": "Dusk", "A": "Watches Pipo fly", "B": "Searches the space", "C": "Passes under arch"},
    7: {"angle": "Detail", "light": "Dusk", "A": "Notices sky change", "B": "Peeks through hole", "C": "Follows small glow"},
    8: {"angle": "Medium", "light": "Dusk", "A": "Uses {obj}", "B": "Uses {obj}", "C": "Plays with {obj}"},
    9: {"angle": "Wide", "light": "Dusk", "A": "Watches monument", "B": "Enters calm space", "C": "Observes quietly"},
    10: {"angle": "Close-up", "light": "Blue Hour", "A": "Face in awe", "B": "Looks amazed", "C": "Eyelids heavy"},
    11: {"angle": "Wide", "light": "Night", "A": "Watches stars", "B": "Quiet break", "C": "Landmark in distance"},
    12: {"angle": "Wide", "light": "Night", "A": "Slows down", "B": "Game ends", "C": "Approaches slowly"},
    13: {"angle": "Close-up", "light": "Night", "A": "Sees {animal}", "B": "Sees {animal}", "C": "Sees {animal}"},
    14: {"angle": "Medium", "light": "Night", "A": "Stands calmly", "B": "Stands calmly", "C": "Relaxes"},
    15: {"angle": "Detail", "light": "Night", "A": "Landmark twinkles", "B": "Landmark sparkles", "C": "Transport stops"},
    16: {"angle": "Medium", "light": "Night", "A": "Prepares spot", "B": "Finds cozy corner", "C": "Settles to sleep"},
    17: {"angle": "Close-up", "light": "Night", "A": "Relaxes", "B": "Relaxes", "C": "Relaxes"},
    18: {"angle": "Close-up", "light": "Night", "A": "Huge yawn", "B": "Huge yawn", "C": "Huge yawn"},
    19: {"angle": "Wide", "light": "Night", "A": "Peaceful scene", "B": "Peaceful scene", "C": "Peaceful scene"},
    20: {"angle": "Wide", "light": "Night", "A": "Sleep", "B": "Sleep", "C": "Sleep"}
}

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Studio Pro", layout="wide")
st.title("🎬 Mélo Studio : Dashboard de Production")

with st.sidebar:
    st.header("⚙️ Pilotage")
    mode = st.radio("Contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    ville_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['name'])
    p_id = st.select_slider("Plan de Scénario (1-20)", options=list(PLANS_DATA.keys()))
    
    st.divider()
    
    # Logique de données
    ville = DESTINATIONS[ville_id]
    plan = PLANS_DATA[p_id]
    struct = ville['struct']
    
    if mode == "🤖 AUTOMATIQUE":
        decor_idx = (p_id - 1) // 5 + 1
        s_decor = ville['decors'][decor_idx]
        s_action = plan[struct].format(obj=ville['obj'], animal=ville['animal'])
        s_light, s_weather = plan['light'], "Clear Sky"
        s_paws, s_gaze, s_expr = "Détendu", "Vers l'horizon", "Curiosité"
        s_acc = ville['obj']
    else:
        st.warning("Mode Manuel")
        d_idx = st.selectbox("Décor", [1,2,3,4], format_func=lambda x: ville['decors'][x]['name'])
        s_decor = ville['decors'][d_idx]
        s_action = st.text_input("Action", value=plan[struct].format(obj=ville['obj'], animal=ville['animal']))
        s_light = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        s_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])
        s_paws = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés", "Derrière le dos"])
        s_gaze = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])
        s_expr = st.selectbox("Expression", ["Émerveillement", "Sourire doux", "Somnolence"])
        s_acc = st.text_input("Accessoire", value=ville['obj'])

# --- 5. DASHBOARD VISUEL (LISIBILITÉ MAXIMALE) ---
st.subheader(f"📍 {ville['name']} — Plan {p_id}")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("DÉCOR", s_decor['name'])
with c2:
    st.metric("ACTION MÉLO", s_action)
with c3:
    st.metric("AMBIANCE", f"{s_light} | {s_weather}")
with c4:
    st.metric("ANATOMIE", f"{s_paws} | {s_gaze}")

st.divider()

# --- 6. PROMPTS ---
t1, t2, t3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with t1:
    p1 = f"Environment Plate: {s_decor['plate']} Time: {s_light}. Weather: {s_weather}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with t2:
    m_anatomy = f"Pose: {s_paws}. Gaze: {s_gaze}. Expression: {s_expr}. Accessory: {s_acc}."
    p2 = f"Integration: {MELO_DNA}. {m_anatomy} Action: {s_action}. Decor: {s_decor['name']}. {s_light}. {VERROUS}. --ar 16:9"
    st.code(p2, language="text")

with t3:
    p3 = f"Animation (8s): {s_action} in ultra-slow motion. Melo in {s_decor['name']}. Pipo soft light trail. {s_weather} effects. Perfect loop."
    st.code(p3, language="text")
