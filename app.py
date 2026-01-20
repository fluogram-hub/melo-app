import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES (4 DÉCORS PAR VILLE) ---
DESTINATIONS = {
    "eiffel_paris": {
        "name": "Paris - Tour Eiffel", "struct": "B", "obj": "Béret rouge", "animal": "Caniche",
        "decors": {
            1: {"name": "Le Trocadéro", "plate": "Empty stone esplanade, blurry distant Eiffel Tower."},
            2: {"name": "Les Quais de Seine", "plate": "Cobble stones, river reflections, Eiffel Tower behind."},
            3: {"name": "Le Pied de la Tour", "plate": "Close-up iron lattice, ground level perspective."},
            4: {"name": "Le Champ-de-Mars", "plate": "Soft green grass, distant tower, evening bokeh."}
        }
    },
    "venice_italy": {
        "name": "Venise", "struct": "C", "obj": "Masque de chat", "animal": "Pigeon blanc",
        "decors": {
            1: {"name": "Le Grand Canal", "plate": "Dark ripples, gondola silhouette, historic palaces."},
            2: {"name": "Le Pont des Soupirs", "plate": "Narrow canal, stone bridge, soft reflections."},
            3: {"name": "Place Saint-Marc", "plate": "Paved square, Byzantine arches, blue hour light."},
            4: {"name": "Intérieur Gondole", "plate": "Dark wood, velvet seats, water surface nearby."}
        }
    }
}

# --- 3. LES 20 PLANS (ACTIONS RÉELLES) ---
PLANS_DATA = {
    1: {"angle": "Wide", "light": "Golden Hour", "A": "Arrivée misty", "B": "Arrivée cherche Pipo", "C": "Arrivée transport"},
    2: {"angle": "Medium", "light": "Golden Hour", "A": "Se frotte les yeux", "B": "Cherche partout", "C": "Regarde au loin"},
    3: {"angle": "Close-up", "light": "Sunset", "A": "Observe la lueur", "B": "Marche sur la pointe des pieds", "C": "Paysage défile"},
    5: {"angle": "Medium", "light": "Sunset", "A": "Sourit à la lumière", "B": "Rit avec Pipo", "C": "Touche l'eau"},
    8: {"angle": "Medium", "light": "Dusk", "A": "Utilise {obj}", "B": "Manipule {obj}", "C": "Joue avec {obj}"},
    10: {"angle": "Close-up", "light": "Blue Hour", "A": "Visage émerveillé", "B": "Regard curieux", "C": "Paupières lourdes"},
    13: {"angle": "Close-up", "light": "Night", "A": "Voit {animal} dormir", "B": "Voit {animal} dormir", "C": "Voit {animal} dormir"},
    18: {"angle": "Close-up", "light": "Night", "A": "Énorme bâillement", "B": "Énorme bâillement", "C": "Énorme bâillement"},
    20: {"angle": "Wide", "light": "Night", "A": "Dodo final", "B": "Dodo final", "C": "Dodo final"}
}

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Studio", layout="wide")
st.title("🎬 Mélo Studio : Dashboard de Production")

with st.sidebar:
    st.header("⚙️ Pilotage")
    mode = st.radio("Contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    ville_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['name'])
    p_id = st.select_slider("Plan (1-20)", options=list(PLANS_DATA.keys()))
    
    st.divider()
    
    # Logique AUTO
    ville = DESTINATIONS[ville_id]
    plan = PLANS_DATA[p_id]
    struct = ville['struct']
    decor_id = (p_id - 1) // 5 + 1 # Change tous les 5 plans
    
    if mode == "🤖 AUTOMATIQUE":
        s_decor = ville['decors'][decor_id]
        s_action = plan[struct].format(obj=ville['obj'], animal=ville['animal'])
        s_light = plan['light']
        s_weather = "Clear Sky"
        s_paws = "Détendu"
        s_gaze = "Vers l'horizon"
    else:
        st.warning("Mode Manuel")
        s_decor = st.selectbox("Décor", [1,2,3,4], format_func=lambda x: ville['decors'][x]['name'])
        s_decor = ville['decors'][s_decor]
        s_action = st.text_input("Action", value=plan[struct].format(obj=ville['obj'], animal=ville['animal']))
        s_light = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        s_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])
        s_paws = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés", "Derrière le dos"])
        s_gaze = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])

# --- 5. DASHBOARD (L'INTERFACE QUE TU PRÉFÈRES) ---
st.subheader(f"📍 {ville['name']} — Plan {p_id}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("DÉCOR", s_decor['name'])
with col2:
    st.metric("ACTION MÉLO", s_action)
with col3:
    st.metric("AMBIANCE", f"{s_light}")
with col4:
    st.metric("ANATOMIE", f"{s_paws}")

st.divider()

# --- 6. PROMPTS ---
t1, t2, t3 = st.tabs(["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"])

with t1:
    p1 = f"Environment Plate: {s_decor['plate']} Time: {s_light}. Weather: {s_weather}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with t2:
    p2 = f"Integration: {MELO_DNA}. Pose: {s_paws}. Looking {s_gaze}. Action: {s_action}. Location: {s_decor['name']}. {s_light}. {VERROUS}. --ar 16:9"
    st.code(p2, language="text")

with t3:
    p3 = f"Animation (8s): {s_action} in ultra-slow motion. Melo in {s_decor['name']}. Pipo soft light trail. {s_weather} effects. Perfect loop."
    st.code(p3, language="text")
