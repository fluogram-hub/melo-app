import streamlit as st

# --- 1. ADN & LOCKS B22 (ANGLAIS POUR L'IA) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile. Iridescent multicolor reflections. Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_B22 = "Homogeneous transparent blue glass, no internal anatomy, high IOR 1.5, caustics, micro-reflections."

# --- 2. TRADUCTEURS TECHNIQUES (FR -> EN) ---
MAT_DECOR_MAP = {
    "Pierre / Béton brute": "weathered raw stone and architectural concrete, high relief, micro-displacement",
    "Métal / Fer oxydé": "oxidized aged metal, ray-traced reflections, realistic rust textures",
    "Eau / Liquide": "calm water surface, real-time reflections, high transparency, subsurface scattering",
    "Bois ancien": "aged wood grain, satin finish, highly detailed procedural textures",
    "Neige / Glace": "powdery snow and crystalline blue ice, sparkling subsurface scattering, frost details",
    "Marbre poli": "polished luxury marble, deep veining, mirror-like reflections, high gloss",
    "Végétation / Herbe": "highly detailed PBR grass and foliage, translucent leaves, realistic organic shaders"
}

FG_MAP = {
    "Aucun": "clear path",
    "Fleurs sauvages": "detailed PBR wild flowers, shallow depth of field",
    "Feuilles mortes": "scattered crisp PBR autumn leaves",
    "Flaques d'eau": "realistic water puddles with ray-traced reflections",
    "Cailloux PBR": "highly detailed PBR pebbles with wet shader"
}

# --- 3. DONNÉES DE BASE (DESTINATIONS & PLANS) ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris (France)", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "decors": {1: "Trocadéro", 2: "Quais de Seine", 3: "Pied de la Tour", 4: "Champ-de-Mars"}},
    "venice_italy": {"nom": "Venise (Italie)", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "decors": {1: "Grand Canal", 2: "Pont des Soupirs", 3: "Place St-Marc", 4: "Gondole"}},
}

# 20 ACTIONS AUTO (A/B/C)
PLANS_DATA = {i: {"angle_ui": "Plan Moyen", "light_ui": "Aube", "light_en": "Golden Hour", 
                  "A": f"Action Contemplative {i}", "B": f"Action Explorative {i}", "C": f"Action Voyage {i}"} for i in range(1, 21)}
PLANS_DATA[1].update({"A": "Observe l'horizon brumeux", "B": "Arrive et cherche Pipo", "C": "Départ en transport"})
PLANS_DATA[18].update({"A": "Énorme bâillement lent", "B": "Énorme bâillement lent", "C": "Énorme bâillement lent"})
PLANS_DATA[20].update({"A": "Dort paisiblement", "B": "Sommeil profond", "C": "Dodo transport"})

# --- 4. STYLE & NAVIGATION ---
st.set_page_config(page_title="Melo Production Master", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("ÉTAPE ACTUELLE :", ["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTÉGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. LOGIQUE SIDEBAR (DYNAMIQUE ET BILINGUE) ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("MODE DE CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # --- INITIALISATION DES VARIABLES (ANTI-ERREUR) ---
    s_decor_ui = ville['decors'][auto_d_id]
    s_angle_ui, s_angle_en = "Plan Moyen", "Medium shot"
    s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
    s_weather_ui, s_weather_en = "Beau temps", "Clear sky"
    s_mat_decor_en = MAT_DECOR_MAP["Pierre / Béton brute"]
    s_season_en = "Spring"
    s_fg_en = FG_MAP["Aucun"]
    s_action_fr = plan[ville['struct']]
    s_paws_en = "relaxed"
    s_expr_en = "calm curiosity"
    s_pipo_pose_en = "floating softly"
    s_pipo_pos_en = "next to head"
    s_palette_en = "natural cinematic"
    s_pipo_col_en = "iridescent white"
    s_energy_en = "soft glow"
    s_acc_en = ville['obj_en']

    if mode == "🕹️ MANUEL":
        st.divider()
        st.subheader(f"🛠️ AJUSTEMENTS {etape.split('.')[1]}")
        
        if "DÉCOR" in etape:
            s_decor_ui = st.selectbox("Lieu précis", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x])
            s_decor_ui = ville['decors'][s_decor_ui]
            s_angle_ui = st.selectbox("Angle de vue", ["Plan Large", "Plan Moyen", "Gros Plan", "Subjectif (POV)"])
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_mat_ui = st.selectbox("Matériaux (XLSX)", list(MAT_DECOR_MAP.keys()))
            s_mat_decor_en = MAT_DECOR_MAP[s_mat_ui]
            s_weather_ui = st.selectbox("Météo", ["Beau temps", "Brume", "Pluie"])
            s_season_ui = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])

        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés", "S'accroche"])
            s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
            s_expr_fr = st.selectbox("Expression Mélo", ["Curiosité", "Émerveillement", "Sourire"])
            s_pipo_pose = st.selectbox("Pose Pipo", ["Flottement doux", "Orbital", "Statique"])
            s_pipo_pos = st.selectbox("Position Pipo", ["À côté de la tête", "Sur l'épaule", "Devant le torse"])
            s_acc_en = st.text_input("Melo Accessory (EN)", value=ville['obj_en'])
            s_palette_en = st.selectbox("Color Palette", ["Natural", "Pastel", "High Contrast"])
            s_pipo_col_en = st.selectbox("Pipo Color", ["Iridescent Pearl", "Pure White", "Glow Blue"])
            s_energy_en = st.selectbox("Pipo Energy Trail", ["Soft glow", "Ribbon trail", "Sparkles"])

        elif "VIDÉO" in etape:
            s_action_fr = st.text_input("Action Vidéo", value=plan[ville['struct']])
            s_energy_en = st.selectbox("Intensité de traînée", ["Minimal", "Medium", "Cinematic Long"])
            s_speed = st.selectbox("Vitesse", ["Ultra-Slow", "Slow-Motion"])

# --- 6. AFFICHAGE FINAL (MAIN AREA) ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE</div><div class="action-text">{s_angle_ui}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">💎 MATÉRIAU DÉCOR</div><div class="action-text">{s_mat_decor_en[:30]}...</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Master Plate")
    st.code(f"Environment: {s_decor_ui} at {ville['nom']}. Materials: {s_mat_decor_en}. Light: {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 MÉLO</div><div class="action-text">{s_paws_en}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_col_en}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🎨 PALETTE</div><div class="action-text">{s_palette_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Intégration B22")
    st.code(f"Integration: MÉLO ({DNA_MELO}). Material: {MATERIAL_B22}. PIPO ({DNA_PIPO}). Pose: {s_paws_en}. Pipo: {s_pipo_col_en}. Palette: {s_palette_en}. Accessory: {s_acc_en}. {TECH_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎞️ ACTION</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🚀 ÉNERGIE</div><div class="action-text">{s_energy_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Vidéo")
    st.code(f"Animation (8s): {s_action_fr} in ultra-slow motion. Pipo trail: {s_energy_en}. Perfect loop, cinematic PBR.")

# --- 7. EXPORT DE PRODUCTION ---
st.divider()
if st.button("💾 GÉNÉRER L'EXPORT COMPLET DU PLAN"):
    export = f"PLAN {p_id} | {ville['nom']}\nDECOR: {s_decor_ui}\nACTION: {s_action_fr}\nMÉLO POSE: {s_paws_en}\nPIPO ENERGY: {s_energy_en}"
    st.code(export, language="text")
