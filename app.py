import streamlit as st

# --- 1. ADN MÉLO & PIPO (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small spirit companion, white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES DES DÉCORS (Extraite de ton Excel) ---
# J'ai structuré ici les 4 lieux par destination
DESTINATIONS = {
    "eiffel_paris": {
        "name": "Paris - Tour Eiffel", "struct": "B", "obj": "Béret rouge", "animal": "Caniche",
        "decors": {
            1: {"name": "Le Trocadéro", "plate": "Eiffel Tower silhouette, stone esplanade, warm distant streetlamps bokeh."},
            2: {"name": "Les Quais de Seine", "plate": "River banks, cobble stones, Eiffel Tower reflected in the water."},
            3: {"name": "Au pied de la Tour", "plate": "Close-up of the iron lattice structure, low angle, ground level."},
            4: {"name": "Pelouse du Champ-de-Mars", "plate": "Green grass, distant Eiffel Tower, soft focus trees."}
        }
    },
    "venice_italy": {
        "name": "Venise - Italie", "struct": "C", "obj": "Masque de chat", "animal": "Pigeon blanc",
        "decors": {
            1: {"name": "Le Grand Canal", "plate": "Calm green water, historic facades, gondola silhouette."},
            2: {"name": "La Petite Ruelle", "plate": "Narrow stone street, soft lantern light, historic walls."},
            3: {"name": "La Place Saint-Marc", "plate": "Vast paved square, Byzantine architecture, soft blue hour light."},
            4: {"name": "L'Intérieur de la Gondole", "plate": "Dark wood textures, water ripples nearby, velvet seats."}
        }
    }
}

# --- 3. LES 20 PLANS (ACTIONS) ---
PLANS_ACTIONS = {
    1: {"angle": "Wide", "action": "Arrivée dans le paysage", "pipo": "Flotte à côté"},
    5: {"angle": "Medium", "action": "Sourit et tend la patte", "pipo": "Lueur douce"},
    10: {"angle": "Close-up", "action": "Observe l'accessoire local", "pipo": "Cercle l'objet"},
    18: {"angle": "Close-up", "action": "Fait un énorme bâillement lent", "pipo": "Reste très proche"},
    20: {"angle": "Wide", "action": "S'endort paisiblement", "pipo": "S'éteint doucement"}
}

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Studio Pro", layout="wide")
st.title("🎬 Studio Mélo : Gestion des Décors & Plans")

with st.sidebar:
    st.header("📍 Configuration")
    mode = st.radio("Contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    ville_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['name'])
    plan_id = st.number_input("Plan (1 à 20)", 1, 20, 1)
    
    # Logique automatique de sélection du décor (1 décor pour 5 plans)
    auto_decor_id = (plan_id - 1) // 5 + 1
    
    ville = DESTINATIONS[ville_id]
    
    if mode == "🤖 AUTOMATIQUE":
        decor_id = auto_decor_id
        st.success(f"Mode Auto : Décor {decor_id} sélectionné.")
    else:
        decor_id = st.selectbox("Choisir le Décor spécifique", [1, 2, 3, 4], format_func=lambda x: ville['decors'][x]['name'])

    st.divider()
    h_val = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
    m_val = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])

# --- 5. RÉCAPITULATIF ---
decor = ville['decors'][decor_id]
action_ref = PLANS_ACTIONS.get(plan_id, PLANS_ACTIONS[1])

st.markdown(f"### 📍 Destination : {ville['name']}")
st.markdown(f"#### 🎥 Scène actuelle : **{decor['name']}** (Décor {decor_id}/4)")

c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"**Action MÉLO**\n\n{action_ref['action']}")
with c2:
    st.info(f"**Action PIPO**\n\n{action_ref['pipo']}")
with c3:
    st.info(f"**Angle**\n\n{action_ref['angle']}")

st.divider()

# --- 6. PROMPTS ---
tab1, tab2, tab3 = st.tabs(["[ 1. FOND ]", "[ 2. IMAGE ]", "[ 3. VIDÉO ]"])

with tab1:
    st.write("### 🖼️ Prompt Décor (Master Plate)")
    p1 = f"Environment Plate: {decor['plate']} Time: {h_val}. Weather: {m_val}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tab2:
    st.write("### 🎨 Prompt Intégration (Nanobanana)")
    # Intégration explicite du nom du décor
    p2 = f"Integration: {MELO_DNA} in {decor['name']}. Action: {action_ref['action']}. Companion: {PIPO_DNA}. Location: {ville['name']}. {h_val}, {m_val}. [VERROUS]: {VERROUS}. --ar 16:9"
    st.code(p2, language="text")

with tab3:
    st.write("### 🎞️ Prompt Animation (Veo 3)")
    p3 = f"Animation (8s): {action_ref['action']} in ultra-slow motion. Melo in {decor['name']}. Pipo trailing soft light. {m_val} effects. Perfect loop, cinematic PBR."
    st.code(p3, language="text")
