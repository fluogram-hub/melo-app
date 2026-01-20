import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22 - TOUJOURS EN ANGLAIS POUR L'IA) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES (DOUBLAGE FR/EN) ---
DESTINATIONS = {
    "eiffel_paris": {
        "name_ui": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "animal_fr": "Caniche", "animal_en": "Poodle",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Eiffel Tower silhouette, stone esplanade, warm bokeh."},
            2: {"ui": "Les Quais de Seine", "en": "River reflections, cobble stones, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Close-up iron lattice, low angle ground view."},
            4: {"ui": "Le Champ-de-Mars", "en": "Soft green grass, distant tower silhouette."}
        }
    },
    "venice_italy": {
        "name_ui": "Venise - Italie", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "animal_fr": "Pigeon blanc", "animal_en": "White pigeon",
        "decors": {
            1: {"ui": "Le Grand Canal", "en": "Dark ripples, gondola silhouette, historic palaces."},
            2: {"ui": "Le Pont des Soupirs", "en": "Narrow canal, stone bridge, soft reflections."},
            3: {"ui": "Place Saint-Marc", "en": "Paved square, Byzantine arches, blue hour light."},
            4: {"ui": "Banc face à l'eau", "en": "Wooden bench, water surface, distant blurry lights."}
        }
    }
}

# --- 3. LES 20 PLANS (DOUBLAGE FR/EN) ---
# Format: {ID: {Angle, Light, A_M_FR, A_M_EN, ...}}
PLANS_DATA = {
    1: {"angle": "Wide", "light_ui": "Aube dorée", "light_en": "Golden Hour", 
        "B_M_FR": "Arrivée (Mélo cherche Pipo)", "B_M_EN": "Arrival (Melo looks for Pipo)"},
    18: {"angle": "Close-up", "light_ui": "Nuit Profonde", "light_en": "Deep Night", 
        "B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge slow yawn"},
    20: {"angle": "Wide", "light_ui": "Nuit Profonde", "light_en": "Deep Night", 
        "B_M_FR": "S'endort / Fondu au noir", "B_M_EN": "Sleep / fade to black"}
}

# --- 4. STYLE & INTERFACE ---
st.set_page_config(page_title="Mélo Studio", layout="wide")

st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    .action-title { color: #007BFF; font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
    .action-text { color: #333333; font-size: 1.3em; line-height: 1.4; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ CONFIGURATION")
    mode = st.radio("Mode de travail", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['name_ui'])
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    
    if mode == "🤖 AUTOMATIQUE":
        d_id = (p_id - 1) // 5 + 1
        s_decor_ui = ville['decors'][d_id]['ui']
        s_decor_en = ville['decors'][d_id]['en']
        s_action_fr = plan[f"{ville['struct']}_M_FR"]
        s_action_en = plan[f"{ville['struct']}_M_EN"]
        s_light_ui = plan['light_ui']
        s_light_en = plan['light_en']
        s_weather_ui, s_weather_en = "Ciel Dégagé", "Clear Sky"
        s_acc_fr, s_acc_en = ville['obj_fr'], ville['obj_en']
    else:
        st.warning("Mode Manuel")
        # Ici on pourrait ajouter des sélecteurs manuels traduits
        s_action_fr, s_action_en = "Action Manuelle", "Manual Action"
        s_decor_ui, s_decor_en = "Décor Manuel", "Manual Decor"
        # etc...

# --- 5. TABLEAU DE BORD (100% FRANÇAIS & LISIBLE) ---
st.title(f"🎬 FICHE DE TOURNAGE : {ville['name_ui']}")
st.markdown(f"### SÉQUENCE : {s_decor_ui} (Plan {p_id}/20)")

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""<div class="info-card"><div class="action-title">🎭 ACTION DE MÉLO</div>
    <div class="action-text">{s_action_fr}</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="info-card"><div class="action-title">🌅 AMBIANCE & LUMIÈRE</div>
    <div class="action-text">{s_light_ui} | {s_weather_ui}</div></div>""", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown(f"""<div class="info-card"><div class="action-title">🐾 ACCESSOIRE</div>
    <div class="action-text">Utilise : {s_acc_fr}</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="info-card"><div class="action-title">📸 CADRAGE</div>
    <div class="action-text">Angle : {plan['angle']}</div></div>""", unsafe_allow_html=True)

st.divider()

# --- 6. PROMPTS (100% ANGLAIS POUR L'IA) ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (NANOBANANA)", "🎞️ 3. VIDÉO (VEO 3)"])

with tab1:
    st.markdown("#### Prompt du fond vide (English)")
    p1 = f"Environment Plate: {s_decor_en} Time: {s_light_en}. Weather: {s_weather_en}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tab2:
    st.markdown("#### Prompt d'intégration (English)")
    p2 = f"Integration: {MELO_DNA}. Action: {s_action_en}. Holding: {s_acc_en}. Decor: {s_decor_ui}. {s_light_en}. {VERROUS}."
    st.code(p2, language="text")

with tab3:
    st.markdown("#### Prompt d'animation (English)")
    p3 = f"Animation (8s): {s_action_en} in ultra-slow motion. Melo in {s_decor_ui}. Pipo trail. {s_weather_en} particles. Perfect loop."
    st.code(p3, language="text")
