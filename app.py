import streamlit as st

# --- 1. ADN & LOCKS B22 (ANGLAIS) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile. Iridescent multicolor reflections."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. DONNÉES DE BASE ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Empty stone esplanade, blurry Eiffel Tower."},
            2: {"ui": "Les Quais de Seine", "en": "River reflections, cobblestones, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Macro iron lattice, low angle ground view."},
            4: {"ui": "Le Champ-de-Mars", "en": "Green grass field, distant tower silhouette."}
        }
    }
}

PLANS_DATA = {i: {"angle_ui": "Plan Large", "angle_en": "Wide shot", "light_ui": "Aube", "light_en": "Golden Hour", "B_M_FR": f"Action Plan {i}", "B_M_EN": f"Action {i}"} for i in range(1, 21)}

# --- 3. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Mélo Production Hub", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION PAR ÉTAPE ---
etape = st.radio("SÉLECTIONNER L'ÉTAPE :", 
                 ["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTÉGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"],
                 horizontal=True)

st.divider()

# --- 5. LOGIQUE DE CALCUL & SIDEBAR ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("MODE DE CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # --- INITIALISATION PAR DÉFAUT (ANTI-ERREUR) ---
    s_decor_ui = ville['decors'][auto_d_id]['ui']
    s_decor_en = ville['decors'][auto_d_id]['en']
    s_angle_ui, s_angle_en = "Plan Large", "Wide shot"
    s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
    s_weather_ui, s_weather_en = "Ciel Dégagé", "Clear Sky"
    s_season_ui, s_season_en = "Printemps", "Spring"
    s_foreground_ui, s_foreground_en = "Aucun", "empty foreground"
    s_material_en = "Realistic PBR textures"
    s_action_fr, s_action_en = plan[f"{ville['struct']}_M_FR"], plan[f"{ville['struct']}_M_EN"]

    if mode == "🕹️ MANUEL":
        st.divider()
        st.subheader(f"🛠️ RÉGLAGES {etape.split('.')[1]}")
        
        if "DÉCOR" in etape:
            m_d_id = st.selectbox("Lieu précis", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
            s_decor_ui, s_decor_en = ville['decors'][m_d_id]['ui'], ville['decors'][m_d_id]['en']
            
            s_season_ui = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_season_en = {"Printemps": "Spring", "Été": "Summer", "Automne": "Autumn", "Hiver": "Winter"}[s_season_ui]
            
            s_foreground_ui = st.selectbox("Élément au premier plan", ["Aucun", "Fleurs sauvages", "Feuilles mortes", "Flaques d'eau", "Poussière en suspension"])
            s_foreground_en = {"Aucun": "clear path", "Fleurs sauvages": "blurred wild flowers in foreground", "Feuilles mortes": "scattered autumn leaves in foreground", "Flaques d'eau": "wet ground with puddles", "Poussière en suspension": "floating dust motes"}[s_foreground_ui]
            
            s_angle_ui = st.selectbox("Angle de vue", ["Plan Large", "Plan Moyen", "Gros Plan"])
            s_angle_en = "Wide shot" if "Large" in s_angle_ui else "Close-up"
            
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"

        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Position Pattes", ["Détendu", "Patte gauche levée", "Bras croisés", "S'accroche à l'objet"])
            s_gaze_fr = st.selectbox("Regard", ["Vers l'horizon", "Vers Pipo", "Vers l'accessoire"])
            s_expr_fr = st.selectbox("Expression", ["Émerveillement", "Sourire doux", "Concentration"])

        elif "VIDÉO" in etape:
            s_energy = st.selectbox("Trainée Pipo", ["Douce", "Fluide éthéré", "Scintillement"])
            s_speed = st.selectbox("Vitesse du mouvement", ["Ultra-Slow", "Cinématique"])

# --- 6. AFFICHAGE CONTEXTUEL ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🍂 SAISON</div><div class="action-text">{s_season_ui}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌿 PREMIER PLAN</div><div class="action-text">{s_foreground_ui}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{s_light_ui}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Master Plate (Fond)")
    st.code(f"Environment Plate: {s_decor_en}. Season: {s_season_en}. Foreground: {s_foreground_en}. Angle: {s_angle_en}. Time: {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🐾 ANATOMIE</div><div class="action-text">{s_paws_fr}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🎒 OBJET</div><div class="action-text">{ville["obj_fr"]}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Intégration (Melo & Pipo)")
    st.code(f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). In: {s_decor_ui}. {TECH_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Animation (8s)")
    st.code(f"Animation (8s): {s_action_en} in ultra-slow motion. Perfect loop.")
