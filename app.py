import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES (4 DÉCORS PAR VILLE) ---
DESTINATIONS = {
    "eiffel_paris": {
        "name": "PARIS - TOUR EIFFEL", "struct": "B", "obj": "Béret rouge", "animal": "Caniche",
        "decors": {
            1: {"name": "Le Trocadéro", "plate": "Empty stone esplanade, blurry distant Eiffel Tower silhouette."},
            2: {"name": "Les Quais de Seine", "plate": "River banks, cobble stones, Eiffel Tower reflected in the water."},
            3: {"name": "Au pied de la Tour", "plate": "Close-up of the iron lattice structure, low angle perspective."},
            4: {"name": "Pelouse du Champ-de-Mars", "plate": "Green grass, distant Eiffel Tower, soft focus trees."}
        }
    },
    "venice_italy": {
        "name": "VENISE - ITALIE", "struct": "C", "obj": "Masque de chat", "animal": "Pigeon blanc",
        "decors": {
            1: {"name": "Le Grand Canal", "plate": "Calm water, gondola silhouette, historic palaces."},
            2: {"name": "Le Pont des Soupirs", "plate": "Narrow canal, stone bridge, soft reflections."},
            3: {"name": "Place Saint-Marc", "plate": "Paved square, Byzantine arches, blue hour light."},
            4: {"name": "Banc face à l'eau", "plate": "Dark wood, velvet, ripples visible nearby."}
        }
    }
}

# --- 3. LES 20 PLANS (SÉQUENCES UNIQUES) ---
PLANS_DATA = {
    1: {"angle": "Wide / Establishing", "light": "Golden Hour", "A": "Arrival in misty landscape", "B": "Arrival (Melo looks for Pipo)", "C": "Departure (Melo on transport)"},
    2: {"angle": "Medium shot", "light": "Golden Hour", "A": "Melo rubs his eyes for color", "B": "Melo rubs his eyes, searching", "C": "Melo looks ahead steady"},
    5: {"angle": "Medium shot", "light": "Sunset", "A": "Melo smiles, reaching for light", "B": "Melo laughs, catching Pipo", "C": "Melo drags paw in water"},
    10: {"angle": "Close-up", "light": "Blue Hour", "A": "Face in awe, lit by color", "B": "Melo looks amazed, then calmer", "C": "Melo eyelids getting heavy"},
    18: {"angle": "Close-up", "light": "Night", "A": "Melo makes a huge, slow yawn", "B": "Melo makes a huge, slow yawn", "C": "Melo makes a huge, slow yawn"},
    20: {"angle": "Wide / Final", "light": "Night", "A": "Sleep, fade to black", "B": "Sleep, fade to black", "C": "Sleep, fade to black"}
}

# --- 4. INTERFACE & STYLE ---
st.set_page_config(page_title="Mélo Studio", layout="wide")

# CSS pour forcer la lisibilité et éviter les coupures
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 20px; border-radius: 5px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
    .action-text { color: #333333; font-size: 1.2em; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ RÉGLAGES")
    mode = st.radio("Contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['name'])
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    
    if mode == "🤖 AUTOMATIQUE":
        d_id = (p_id - 1) // 5 + 1
        s_decor = ville['decors'][d_id]
        s_action = plan[ville['struct']].format(obj=ville['obj'], animal=ville['animal'])
        s_light, s_weather = plan['light'], "Clear Sky"
        s_paws, s_gaze, s_expr = "Détendu", "Vers l'horizon", "Curiosité"
        s_acc = ville['obj']
    else:
        d_idx = st.selectbox("Décor", [1,2,3,4], format_func=lambda x: ville['decors'][x]['name'])
        s_decor = ville['decors'][d_idx]
        s_action = st.text_area("Action personnalisée", value=plan[ville['struct']].format(obj=ville['obj'], animal=ville['animal']))
        s_light = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        s_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])
        s_paws = st.selectbox("Anatomie", ["Détendu", "Patte levée", "Bras croisés", "Derrière le dos"])
        s_gaze = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])
        s_expr = st.selectbox("Expression", ["Émerveillement", "Sourire doux", "Somnolence"])
        s_acc = st.text_input("Accessoire", value=ville['obj'])

# --- 5. FICHE DE TOURNAGE (LISIBLE) ---
st.title(f"🎬 {ville['name']}")
st.markdown(f"### SÉQUENCE : {s_decor['name']} (Plan {p_id}/20)")

# Remplacement des metrics par des boites qui ne coupent pas le texte
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""<div class="info-card"><div class="action-title">🎭 ACTION MÉLO</div>
    <div class="action-text">{s_action}</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="info-card"><div class="action-title">✨ ÉMOTION & REGARD</div>
    <div class="action-text">{s_expr} — Regarde {s_gaze.lower()}</div></div>""", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown(f"""<div class="info-card"><div class="action-title">🌅 AMBIANCE</div>
    <div class="action-text">{s_light} | {s_weather}</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="info-card"><div class="action-title">🐾 ANATOMIE</div>
    <div class="action-text">{s_paws} | Avec {s_acc}</div></div>""", unsafe_allow_html=True)

st.divider()

# --- 6. PROMPTS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    st.markdown("#### Prompt pour le fond vide")
    p1 = f"Environment Plate: {s_decor['plate']} Time: {s_light}. Weather: {s_weather}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tab2:
    st.markdown("#### Prompt pour l'intégration de Mélo & Pipo")
    p2 = f"Integration: {MELO_DNA}. Pose: {s_paws}. Gaze: {s_gaze}. Expression: {s_expr}. Accessory: {s_acc}. Action: {s_action}. Location: {s_decor['name']}. {s_light}. {VERROUS}."
    st.code(p2, language="text")

with tab3:
    st.markdown("#### Prompt pour l'animation Veo 3")
    p3 = f"Animation (8s): {s_action} in ultra-slow motion. Melo in {s_decor['name']}. Pipo soft light trail. {s_weather} particles. Perfect loop."
    st.code(p3, language="text")
