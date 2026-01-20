import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES : DÉCORS PAR VILLE ---
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

# --- 3. LES 20 PLANS RÉELS (ACTIONS DÉTAILLÉES) ---
# Ici, chaque plan a une action unique pour la Structure B (Paris) et C (Venise)
PLANS_DATA = {
    1: {"light_ui": "Aube", "light_en": "Golden Hour", "B_FR": "Arrive et cherche Pipo du regard", "B_EN": "Arrival, looking for Pipo", "C_FR": "Départ sur le transport", "C_EN": "Departure on transport"},
    2: {"light_ui": "Matin", "light_en": "Morning", "B_FR": "Se frotte les yeux avec étonnement", "B_EN": "Rubs eyes with wonder", "C_FR": "Regarde l'horizon défiler", "C_EN": "Watching the horizon drift"},
    3: {"light_ui": "Matin", "light_en": "Morning", "B_FR": "Marche sur la pointe des pieds", "B_EN": "Walking on tiptoes", "C_FR": "S'accroche au rebord du transport", "C_EN": "Holding onto the transport edge"},
    4: {"light_ui": "Midi", "light_en": "High Noon", "B_FR": "Découvre un indice au sol", "B_EN": "Finds a clue on the ground", "C_FR": "Suit une lueur dans l'eau", "C_EN": "Following a glow in the water"},
    5: {"light_ui": "Midi", "light_en": "High Noon", "B_FR": "Rit aux éclats avec Pipo", "B_EN": "Laughing out loud with Pipo", "C_FR": "Laisse traîner sa patte dans l'eau", "C_EN": "Dragging paw in the water"},
    6: {"light_ui": "Après-midi", "light_en": "Afternoon", "B_FR": "Explore le nouvel espace", "B_EN": "Exploring the new space", "C_FR": "Passe sous un pont sombre", "C_EN": "Passing under a dark bridge"},
    7: {"light_ui": "Après-midi", "light_en": "Afternoon", "B_FR": "Observe le changement de ciel", "B_EN": "Watching the sky change", "C_FR": "Regarde les reflets sur les murs", "C_EN": "Watching reflections on walls"},
    8: {"light_ui": "Après-midi", "light_en": "Afternoon", "B_FR": "Manipule l'accessoire {obj}", "B_EN": "Handling the {obj}", "C_FR": "Joue avec l'accessoire {obj}", "C_EN": "Playing with the {obj}"},
    9: {"light_ui": "Fin de journée", "light_en": "Late Afternoon", "B_FR": "S'assoit pour admirer la vue", "B_EN": "Sits to admire the view", "C_FR": "Le transport ralentit doucement", "C_EN": "Transport slowing down gently"},
    10: {"light_ui": "Coucher Soleil", "light_en": "Sunset", "B_FR": "Visage illuminé par le monument", "B_EN": "Face lit by the landmark", "C_FR": "Émerveillement total devant la lumière", "C_EN": "Total wonder at the light"},
    11: {"light_ui": "Crépuscule", "light_en": "Dusk", "B_FR": "Prend une pause avec Pipo", "B_EN": "Taking a break with Pipo", "C_FR": "Observe le monument au loin", "C_EN": "Watching the landmark in the distance"},
    12: {"light_ui": "Crépuscule", "light_en": "Dusk", "B_FR": "Le jeu se calme", "B_EN": "Playtime ends calmly", "C_FR": "S'approche du quai final", "C_EN": "Approaching the final dock"},
    13: {"light_ui": "Heure Bleue", "light_en": "Blue Hour", "B_FR": "Regarde un animal dormir", "B_EN": "Watching a sleeping animal", "C_FR": "Regarde un animal dormir", "C_EN": "Watching a sleeping animal"},
    14: {"light_ui": "Heure Bleue", "light_en": "Blue Hour", "B_FR": "Reste immobile et serein", "B_EN": "Standing still and serene", "C_FR": "Se relaxe contre le rebord", "C_EN": "Relaxing against the edge"},
    15: {"light_ui": "Nuit", "light_en": "Night", "B_FR": "Le monument scintille", "B_EN": "The landmark sparkles", "C_FR": "Le transport s'arrête", "C_EN": "The transport stops"},
    16: {"light_ui": "Nuit", "light_en": "Night", "B_FR": "Prépare un coin douillet", "B_EN": "Preparing a cozy corner", "C_FR": "S'installe pour la nuit", "C_EN": "Settling in for the night"},
    17: {"light_ui": "Nuit", "light_en": "Night", "B_FR": "Ferme doucement les yeux", "B_EN": "Gently closing eyes", "C_FR": "Ferme doucement les yeux", "C_EN": "Gently closing eyes"},
    18: {"light_ui": "Nuit", "light_en": "Night", "B_FR": "Fait un énorme bâillement", "B_EN": "Huge slow yawn", "C_FR": "Fait un énorme bâillement", "C_EN": "Huge slow yawn"},
    19: {"light_ui": "Nuit", "light_en": "Night", "B_FR": "Paysage paisible final", "B_EN": "Final peaceful landscape", "C_FR": "Paysage paisible final", "C_EN": "Final peaceful landscape"},
    20: {"light_ui": "Nuit", "light_en": "Night", "B_FR": "Sommeil profond", "B_EN": "Deep sleep", "C_FR": "Sommeil profond", "C_EN": "Deep sleep"}
}

# --- 4. STYLE CSS ---
st.set_page_config(page_title="Mélo Contextual Studio", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #f8f9fa; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }
    .action-text { color: #333333; font-size: 1.15em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR (LOGIQUE DYNAMIQUE) ---
with st.sidebar:
    st.title("🎬 CONFIGURATION")
    mode = st.radio("Mode de contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    struct = ville['struct']
    
    # CALCUL DÉCOR ET ACTION
    d_id = (p_id - 1) // 5 + 1
    
    if mode == "🤖 AUTOMATIQUE":
        s_decor_ui = ville['decors'][d_id]['ui']
        s_decor_en = ville['decors'][d_id]['en']
        s_action_fr = plan[f"{struct}_FR"].format(obj=ville['obj_fr'])
        s_action_en = plan[f"{struct}_EN"].format(obj=ville['obj_en'])
        s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
        s_paws_fr, s_paws_en = "Détendu", "relaxed"
        s_gaze_fr, s_gaze_en = "Vers l'horizon", "horizon"
    else:
        st.warning("🕹️ MODE MANUEL")
        manual_d = st.selectbox("Décor", [1,2,3,4], index=d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
        s_decor_ui = ville['decors'][manual_d]['ui']
        s_decor_en = ville['decors'][manual_d]['en']
        s_action_fr = st.text_input("Action (FR)", value=plan[f"{struct}_FR"].format(obj=ville['obj_fr']))
        s_action_en = plan[f"{struct}_EN"].format(obj=ville['obj_en'])
        s_light_ui = st.selectbox("Horaire", ["Aube", "Coucher Soleil", "Nuit"])
        s_light_en = "Golden Hour"
        s_paws_fr = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés"])
        s_paws_en = "one paw raised"
        s_gaze_fr = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])
        s_gaze_en = "straight ahead"

# --- 6. ZONE DE TRAVAIL ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR DU PLAN {p_id}</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{s_light_ui}</div></div>', unsafe_allow_html=True)
    st.code(f"Environment: {s_decor_en} | Light: {s_light_en}")

with tab2:
    # ICI LES INFOS DOIVENT CHANGER DYNAMIQUEMENT
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION DÉTECTÉE</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🐾 ANATOMIE</div><div class="action-text">{s_paws_fr}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><div class="action-title">👁️ REGARD</div><div class="action-text">{s_gaze_fr}</div></div>', unsafe_allow_html=True)

    st.subheader("Prompt Image")
    p2 = f"Integration: {MELO_DNA}. Pose: {s_paws_en}. Looking {s_gaze_en}. Action: {s_action_en}. In: {s_decor_ui}. {s_light_en}. {VERROUS}."
    st.code(p2)

with tab3:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT VIDÉO</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    st.code(f"Animation (8s): {s_action_en} in ultra-slow motion. Perfect loop.")
