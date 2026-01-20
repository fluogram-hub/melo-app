import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22 - ANGLAIS POUR L'IA) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. DONNÉES LIEUX (FR/EN) ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "animal_en": "Poodle",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Eiffel Tower silhouette, stone esplanade, warm bokeh."},
            2: {"ui": "Les Quais de Seine", "en": "River reflections, cobble stones, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Close-up iron lattice, low angle ground view."},
            4: {"ui": "Le Champ-de-Mars", "en": "Soft green grass, distant tower silhouette."}
        }
    },
    "venice_italy": {
        "nom": "Venise - Italie", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "animal_en": "White pigeon",
        "decors": {
            1: {"ui": "Le Grand Canal", "en": "Dark ripples, gondola silhouette, historic palaces."},
            2: {"ui": "Le Pont des Soupirs", "en": "Narrow canal, stone bridge, soft reflections."},
            3: {"ui": "Place Saint-Marc", "en": "Paved square, Byzantine arches, blue hour light."},
            4: {"ui": "Banc face à l'eau", "en": "Wooden bench, water surface, distant blurry lights."}
        }
    }
}

# --- 3. LES 20 PLANS (DOUBLAGE FR/EN) ---
PLANS_DATA = {
    1: {"angle": "Wide", "light_ui": "Aube dorée", "light_en": "Golden Hour", "B_M_FR": "Arrivée (Mélo cherche Pipo)", "B_M_EN": "Arrival (Melo looks for Pipo)"},
    2: {"angle": "Medium", "light_ui": "Matinée", "light_en": "Morning", "B_M_FR": "Se frotte les yeux", "B_M_EN": "Rubs his eyes"},
    5: {"angle": "Medium", "light_ui": "Coucher du soleil", "light_en": "Sunset", "B_M_FR": "Rit avec Pipo", "B_M_EN": "Laughs with Pipo"},
    10: {"angle": "Close-up", "light_ui": "Heure Bleue", "light_en": "Blue Hour", "B_M_FR": "Regard émerveillé", "B_M_EN": "Looking in awe"},
    18: {"angle": "Close-up", "light_ui": "Nuit Profonde", "light_en": "Deep Night", "B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge slow yawn"},
    20: {"angle": "Wide", "light_ui": "Nuit Profonde", "light_en": "Deep Night", "B_M_FR": "S'endort paisiblement", "B_M_EN": "Sleeps peacefully"}
}

# --- 4. STYLE CSS ---
st.set_page_config(page_title="Mélo Studio Pro", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.9em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("Mode de contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("Plan de scénario", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    
    if mode == "🤖 AUTOMATIQUE":
        d_id = (p_id - 1) // 5 + 1
        s_decor_ui = ville['decors'][d_id]['ui']
        s_decor_en = ville['decors'][d_id]['en']
        s_action_fr = plan[f"{ville['struct']}_M_FR"]
        s_action_en = plan[f"{ville['struct']}_M_EN"]
        s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
        s_weather_ui, s_weather_en = "Ciel Dégagé", "Clear Sky"
        s_paws_fr, s_paws_en = "Détendu", "relaxed"
        s_gaze_fr, s_gaze_en = "Vers l'horizon", "horizon"
        s_expr_fr, s_expr_en = "Curiosité", "curious"
        s_acc_fr, s_acc_en = ville['obj_fr'], ville['obj_en']
    else:
        st.warning("MODE MANUEL ACTIVÉ")
        d_id = st.selectbox("Décor", [1,2,3,4], format_func=lambda x: ville['decors'][x]['ui'])
        s_decor_ui = ville['decors'][d_id]['ui']
        s_decor_en = ville['decors'][d_id]['en']
        s_action_fr = st.text_input("Action Mélo (FR)", value="Marche lentement")
        s_action_en = "Walking slowly"
        s_light_ui = st.selectbox("Horaire", ["Aube", "Coucher Soleil", "Nuit"], index=1)
        s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"
        s_weather_ui = st.selectbox("Météo", ["Beau temps", "Pluie", "Neige"], index=0)
        s_weather_en = "Clear Sky"
        s_paws_fr = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés"])
        s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
        s_gaze_fr = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers le sol"])
        s_gaze_en = "straight ahead"
        s_expr_fr = st.selectbox("Expression", ["Joie", "Fatigue", "Émerveillement"])
        s_expr_en = "happy"
        s_acc_fr = st.text_input("Accessoire", value=ville['obj_fr'])
        s_acc_en = ville['obj_en']

# --- 6. AFFICHAGE (UI FRANÇAISE) ---
st.title(f"🎬 {ville['nom']} — Plan {p_id}")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION MÉLO</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="info-card"><div class="action-title">🌅 AMBIANCE</div><div class="action-text">{s_light_ui} | {s_weather_ui}</div></div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown(f'<div class="info-card"><div class="action-title">🐾 ANATOMIE & REGARD</div><div class="action-text">{s_paws_fr} | Regard : {s_gaze_fr}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="info-card"><div class="action-title">🎒 ACCESSOIRE</div><div class="action-text">{s_acc_fr}</div></div>', unsafe_allow_html=True)

# --- 7. PROMPTS (ANGLAIS) ---
st.divider()
t1, t2, t3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with t1:
    p1 = f"Environment: {s_decor_en} Time: {s_light_en}. Weather: {s_weather_en}. --ar 16:9"
    st.code(p1)
with t2:
    p2 = f"Integration: {MELO_DNA}. Pose: {s_paws_en}. Looking {s_gaze_en}. Action: {s_action_en}. {s_light_en}. {VERROUS}."
    st.code(p2)
with t3:
    p3 = f"Animation (8s): {s_action_en} in ultra-slow motion. Melo in {s_decor_ui}. Perfect loop."
    st.code(p3)
