import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22 - ANGLAIS POUR L'IA) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES : 4 DÉCORS PAR VILLE ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Eiffel Tower silhouette, stone esplanade, warm bokeh."},
            2: {"ui": "Les Quais de Seine", "en": "River reflections, cobble stones, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Close-up iron lattice, low angle ground view."},
            4: {"ui": "Le Champ-de-Mars", "en": "Soft green grass, distant tower silhouette."}
        }
    },
    "venice_italy": {
        "nom": "Venise - Italie", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask",
        "decors": {
            1: {"ui": "Le Grand Canal", "en": "Dark ripples, gondola silhouette, historic palaces."},
            2: {"ui": "Le Pont des Soupirs", "en": "Narrow canal, stone bridge, soft reflections."},
            3: {"ui": "Place Saint-Marc", "en": "Paved square, Byzantine arches, blue hour light."},
            4: {"ui": "Ruelle typique", "en": "Narrow stone street, soft lantern light, historic walls."}
        }
    }
}

# --- 3. LES 20 PLANS COMPLETS (ACTIONS FR/EN) ---
# Chaque plan de 1 à 20 est maintenant défini.
PLANS_DATA = {}
for i in range(1, 21):
    if i <= 5: ang, light_ui, light_en = "Wide", "Aube dorée", "Golden Hour"
    elif i <= 10: ang, light_ui, light_en = "Medium", "Coucher du Soleil", "Sunset"
    elif i <= 15: ang, light_ui, light_en = "Close-up", "Heure Bleue", "Blue Hour"
    else: ang, light_ui, light_en = "Wide", "Nuit Profonde", "Deep Night"
    
    # Remplissage générique des actions pour l'exemple (à affiner avec tes phrases exactes)
    PLANS_DATA[i] = {
        "angle": ang, "light_ui": light_ui, "light_en": light_en,
        "A_M_FR": f"Action Plan {i} (Structure A)", "A_M_EN": f"Action Plan {i} (A)",
        "B_M_FR": f"Action Plan {i} (Structure B)", "B_M_EN": f"Action Plan {i} (B)",
        "C_M_FR": f"Action Plan {i} (Structure C)", "C_M_EN": f"Action Plan {i} (C)"
    }

# --- 4. STYLE & INTERFACE ---
st.set_page_config(page_title="Mélo Studio Contextuel", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #f8f9fa; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }
    .action-text { color: #333333; font-size: 1.15em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎬 CONFIGURATION")
    mode = st.radio("Mode de contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    struct = ville['struct']
    
    # LOGIQUE DE CHANGEMENT DE DÉCOR (1 décor pour 5 plans)
    d_id = (p_id - 1) // 5 + 1
    
    if mode == "🤖 AUTOMATIQUE":
        s_decor_ui = ville['decors'][d_id]['ui']
        s_decor_en = ville['decors'][d_id]['en']
        s_action_fr = plan[f"{struct}_M_FR"]
        s_action_en = plan[f"{struct}_M_EN"]
        s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
        s_weather_ui, s_weather_en = "Ciel Dégagé", "Clear Sky"
        s_paws_fr, s_paws_en = "Détendu", "relaxed"
        s_gaze_fr, s_gaze_en = "Vers l'horizon", "horizon"
        s_acc_fr, s_acc_en = ville['obj_fr'], ville['obj_en']
        s_expr_fr, s_expr_en = "Émerveillement", "amazed"
    else:
        st.warning("🕹️ MODE MANUEL")
        manual_d = st.selectbox("Décor", [1,2,3,4], index=d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
        s_decor_ui = ville['decors'][manual_d]['ui']
        s_decor_en = ville['decors'][manual_d]['en']
        s_action_fr = st.text_input("Action (FR)", value=plan[f"{struct}_M_FR"])
        s_action_en = plan[f"{struct}_M_EN"]
        s_light_ui = st.selectbox("Horaire", ["Aube", "Coucher Soleil", "Heure Bleue", "Nuit"])
        s_light_en = "Golden Hour"
        s_weather_ui = st.selectbox("Météo", ["Beau temps", "Pluie", "Neige"])
        s_weather_en = "Clear Sky"
        s_paws_fr = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés"])
        s_paws_en = "one paw raised"
        s_gaze_fr = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])
        s_gaze_en = "straight ahead"
        s_acc_fr = st.text_input("Accessoire", value=ville['obj_fr'])
        s_acc_en = ville['obj_en']
        s_expr_fr = "Manuel"
        s_expr_en = "manual"

# --- 6. ZONE DE TRAVAIL CONTEXTUELLE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR ACTUEL (Plan {p_id})</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🌅 AMBIANCE LUMINEUSE</div><div class="action-text">{s_light_ui} | {s_weather_ui}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Decor (English)")
    st.code(f"Environment Plate: {s_decor_en} Time: {s_light_en}. Weather: {s_weather_en}. POETIC, MINIMALIST. --ar 16:9")

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎭 ANATOMIE</div><div class="action-text">{s_paws_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">👁️ REGARD</div><div class="action-text">{s_gaze_fr}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><div class="action-title">🎒 ACCESSOIRE</div><div class="action-text">{s_acc_fr}</div></div>', unsafe_allow_html=True)

    st.subheader("Prompt Intégration (English)")
    p2 = f"Integration: {MELO_DNA}. Pose: {s_paws_en}. Looking {s_gaze_en}. Action: {s_action_en}. Holding: {s_acc_en}. Decor: {s_decor_ui}. {s_light_en}. {VERROUS}."
    st.code(p2)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT VIDÉO</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🚀 EFFETS</div><div class="action-text">Ultra-slow motion | Particules {s_weather_ui}</div></div>', unsafe_allow_html=True)

    st.subheader("Prompt Animation (English)")
    p3 = f"Animation (8s): {s_action_en} in ultra-slow motion. {s_weather_en} particles. Melo in {s_decor_ui}. Perfect loop."
    st.code(p3)
