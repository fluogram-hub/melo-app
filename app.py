import streamlit as st

# --- 1. ADN & LOCKS B22 (ANGLAIS POUR L'IA) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile. Iridescent multicolor reflections. Soft constant glow."
TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_B22 = "Homogeneous transparent blue glass, no internal anatomy, high IOR 1.5, caustics, micro-reflections."

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX (L'équivalent de Lists!$AL$2:$AL$400) ---
LISTE_MATERIAUX_PBR = [
    "Weathered Concrete with micro-cracks", "Polished White Carrara Marble", "Aged Oxidized Bronze with green patina",
    "Raw Basalt Rock textures", "Brushed Aerospace Aluminum", "Dark Volcanic Sand", "Wet PBR Mud with puddles",
    "Old Oak Wood with deep grain", "Frosted Crystalline Ice", "Powdery Fresh Snow", "Ancient Red Brick masonry",
    "Polished Gold leaf reflections", "Rough Sandstone blocks", "Translucent Jade stone", "Corroded Industrial Steel",
    "Moss-covered Granite", "Satin Smooth Plaster", "Glossy Ceramic Tiles", "Burnished Copper surface",
    "Natural Slate shingles", "Exposed Aggregate Concrete", "Limestone with fossil details", "Asphalt with oil sheen",
    "Hand-carved Dark Teak", "Iridescent Glass panels", "Hammered Silver finish", "Raw Red Clay", "Etched Mirror surfaces"
    # ... extensible jusqu'à 400 entrées
]

FG_MAP = {
    "Aucun": "clear path",
    "Fleurs sauvages": "highly detailed PBR wild flowers with subsurface scattering",
    "Feuilles mortes": "scattered crisp PBR autumn leaves, micro-textures",
    "Flaques d'eau": "realistic water puddles with ray-traced reflections",
    "Cailloux PBR": "highly detailed PBR pebbles with wet surface shader",
    "Brume au sol": "low-lying volumetric ground fog"
}

# --- 3. LES 20 DESTINATIONS DU MONDE ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris (France)", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "decors": {1: "Trocadéro", 2: "Quais de Seine", 3: "Pied de la Tour", 4: "Champ-de-Mars"}},
    "venice_italy": {"nom": "Venise (Italie)", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "decors": {1: "Grand Canal", 2: "Pont des Soupirs", 3: "Place St-Marc", 4: "Gondole"}},
    "taj_mahal": {"nom": "Taj Mahal (Inde)", "struct": "A", "obj_fr": "Lanterne", "obj_en": "Oil lantern", "decors": {1: "Bassin miroir", 2: "Jardins", 3: "Dôme principal", 4: "Bord de rivière"}},
    "fuji_japan": {"nom": "Mont Fuji (Japon)", "struct": "A", "obj_fr": "Éventail", "obj_en": "Paper fan", "decors": {1: "Lac Kawaguchi", 2: "Pagode Chureito", 3: "Cerisiers", 4: "Sentier enneigé"}},
    # ... (les 20 destinations sont injectées ici)
}

# 20 PLANS AUTO (A/B/C)
PLANS_DATA = {i: {"angle": "Medium", "light_fr": "Aube", "light_en": "Golden Hour", "A": f"Action {i} (Contemplatif)", "B": f"Action {i} (Exploration)", "C": f"Action {i} (Transport)"} for i in range(1, 21)}
PLANS_DATA[18].update({"A": "Énorme bâillement lent", "B": "Énorme bâillement lent", "C": "Énorme bâillement lent"})
PLANS_DATA[20].update({"A": "Sommeil profond", "B": "Dodo assis", "C": "Sommeil en mouvement"})

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Master", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Navigation par étape (Réactive avec la sidebar)
etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTÉGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. LOGIQUE SIDEBAR DYNAMIQUE ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("MODE DE CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # Valeurs par défaut pour éviter les erreurs d'affichage
    s_decor_ui = ville['decors'][auto_d_id]
    s_angle_en = "Medium shot"
    s_light_en = plan['light_en']
    s_mat_decor_en = LISTE_MATERIAUX_PBR[0]
    s_weather_en = "Clear Sky"
    s_season_en = "Spring"
    s_fg_en = FG_MAP["Aucun"]
    s_action_fr = plan[ville['struct']]
    s_paws_en = "relaxed"
    s_expr_en = "calm curiosity"
    s_pipo_pose_en = "floating softly"
    s_pipo_pos_en = "near Melo's head"
    s_palette_en = "natural cinematic"
    s_pipo_col_en = "iridescent white"
    s_energy_en = "soft glow"

    if mode == "🕹️ MANUEL":
        st.divider()
        st.subheader(f"🛠️ RÉGLAGES {etape.split('.')[1]}")
        
        if "DÉCOR" in etape:
            m_d_id = st.selectbox("Lieu précis", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x])
            s_decor_ui = ville['decors'][m_d_id]
            s_angle_ui = st.selectbox("Angle de vue", ["Plan Large", "Plan Moyen", "Gros Plan", "Subjectif (POV)"])
            s_angle_en = "Wide shot" if "Large" in s_angle_ui else "Medium shot"
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"
            s_mat_ui = st.selectbox("Matériaux du décor (AL2:AL400)", LISTE_MATERIAUX_PBR)
            s_mat_decor_en = s_mat_ui
            s_weather_ui = st.selectbox("Météo", ["Ciel pur", "Brume", "Pluie", "Neige"])
            s_weather_en = "Clear Sky" if "pur" in s_weather_ui else "Atmospheric"
            s_season_ui = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_season_en = s_season_ui
            s_fg_ui = st.selectbox("Premier Plan", list(FG_MAP.keys()))
            s_fg_en = FG_MAP[s_fg_ui]

        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés", "Assis"])
            s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
            s_expr_fr = st.selectbox("Expression de Mélo", ["Curiosité", "Émerveillement", "Somnolence"])
            s_expr_en = "curious wonder"
            s_pipo_pose = st.selectbox("Pose Pipo", ["Flottement doux", "Orbitale", "Statique"])
            s_pipo_pos = st.selectbox("Position Pipo", ["À droite de la tête", "Sur l'épaule", "Devant le torse"])
            s_acc_en = st.text_input("Melo accessory (EN)", value=ville['obj_en'])
            s_palette_en = st.selectbox("Color palette", ["Natural cinematic", "High contrast", "Pastel soft"])
            s_pipo_col_en = st.selectbox("Pipo color", ["Iridescent Pearl", "Pure White", "Glow Multicolore"])
            s_energy_en = st.selectbox("Pipo energy trail", ["Soft glow", "Ribbon trail", "Sparkling"])

        elif "VIDÉO" in etape:
            s_action_fr = st.text_input("Mouvement (FR)", value=plan[ville['struct']])
            s_energy_en = st.selectbox("Trainée d'énergie", ["Minimal", "Long ribbon", "Sparkling trail"])
            s_speed = st.selectbox("Vitesse", ["Ultra-Slow", "Slow-Motion"])

# --- 6. AFFICHAGE FINAL ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE</div><div class="action-text">{s_angle_en}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">💎 MATÉRIAU</div><div class="action-text">{s_mat_decor_en}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{s_light_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Master Plate (FOND)")
    st.code(f"Environment: {s_decor_ui}. Material Spec: {s_mat_decor_en}. Season: {s_season_en}. Foreground: {s_fg_en}. Angle: {s_angle_en}. Time: {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    st.markdown(f'<div class="info-card"><div class="action-title">🎭 CONFIGURATION B22</div><div class="action-text">{s_paws_en} | {s_expr_en} | Palette: {s_palette_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Intégration (IMAGE)")
    st.code(f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws_en}. Pipo: {s_pipo_col_en} at {s_pipo_pos_en}. Material: {MATERIAL_B22}. {TECHNICAL_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Vidéo (MOUVEMENT)")
    st.code(f"Animation (8s): {s_action_fr} in ultra-slow motion. Pipo trail: {s_energy_en}. Perfect loop, cinematic PBR.")

# --- 7. EXPORT COMPLET ---
st.divider()
if st.button("💾 GÉNÉRER L'EXPORT COMPLET DU PLAN"):
    export = f"PLAN {p_id} | {ville['nom']}\nDECOR: {s_decor_ui} | MAT: {s_mat_decor_en}\nIMAGE: {s_paws_en} | PIPO: {s_pipo_col_en}\nVIDEO: {s_action_fr} | TRAIL: {s_energy_en}"
    st.code(export, language="text")
