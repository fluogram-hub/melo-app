import streamlit as st

# --- 1. ADN MÉLO & PIPO (BIBLE B22 - LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Wearing a blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile. Iridescent multicolor reflections. Soft constant glow."
TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_B22 = "Homogeneous transparent blue glass, no internal anatomy, high IOR 1.5, caustics, micro-reflections."

# --- 2. TRADUCTEURS TECHNIQUES ---
FG_MAP = {
    "Aucun": "clear path",
    "Fleurs sauvages": "highly detailed PBR wild flowers, shallow depth of field",
    "Feuilles mortes": "scattered crisp PBR autumn leaves, detailed vein textures",
    "Flaques d'eau": "realistic water puddles with ray-traced reflections",
    "Cailloux PBR": "highly detailed PBR pebbles with wet shader"
}

# --- 3. LES 20 DESTINATIONS ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris (France)", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "decors": {1: "Trocadéro", 2: "Quais de Seine", 3: "Pied de la Tour", 4: "Champ-de-Mars"}},
    "venice_italy": {"nom": "Venise (Italie)", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "decors": {1: "Grand Canal", 2: "Pont des Soupirs", 3: "Place St-Marc", 4: "Gondole"}},
    "lapland_arctic": {"nom": "Laponie (Arctique)", "struct": "A", "obj_fr": "Chocolat chaud", "obj_en": "Hot cocoa", "decors": {1: "Forêt enneigée", 2: "Igloo", 3: "Traîneau", 4: "Aurores boréales"}}
}

# --- 4. LOGIQUE DES 20 PLANS (ACTIONS VIDÉO PRÉ-PROGRAMMÉES) ---
# A: Contemplatif | B: Exploration | C: Transport
PLANS_DATA = {
    1: {"angle": "Wide", "light": "Golden Hour", "A": "Respiration lente, observe l'horizon", "B": "Arrive et cherche Pipo du regard", "C": "Départ, Mélo regarde la ville s'éloigner"},
    2: {"angle": "Medium", "light": "Golden Hour", "A": "Léger balancement des oreilles", "B": "Se frotte les yeux avec étonnement", "C": "Vibration douce du transport, Mélo est stable"},
    5: {"angle": "Close-up", "light": "Sunset", "A": "Clignement d'yeux lent, sourire doux", "B": "Rit et essaie d'attraper Pipo", "C": "Laisse traîner sa patte dans l'eau/air"},
    10: {"angle": "POV", "light": "Blue Hour", "A": "Observation fixe d'une lueur", "B": "Découvre l'accessoire avec émerveillement", "C": "Regarde les reflets passer sur son costume"},
    18: {"angle": "Close-up", "light": "Deep Night", "A": "Énorme bâillement lent", "B": "S'étire doucement", "C": "Se blottit contre le rebord"},
    20: {"angle": "Wide", "light": "Deep Night", "A": "Sommeil profond", "B": "S'endort assis", "C": "Le transport s'arrête, Mélo dort"}
}
# Remplissage par défaut pour les plans non-spécifiés
for i in range(1, 21):
    if i not in PLANS_DATA:
        PLANS_DATA[i] = {"angle": "Medium", "light": "Noon", "A": "Observation calme", "B": "Exploration lente", "C": "Voyage paisible"}

# --- 5. STYLE & CONFIGURATION ---
st.set_page_config(page_title="Melo Production Master", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("ÉTAPE ACTUELLE :", ["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"], horizontal=True)
st.divider()

# --- 6. LOGIQUE SIDEBAR (DYNAMIQUE) ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("MODE DE CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # Variables par défaut
    s_decor_ui = ville['decors'][auto_d_id]
    s_angle_ui = plan['angle']
    s_light_ui = plan['light']
    s_mat_decor = "Réaliste PBR"
    s_action_fr = plan[ville['struct']]
    s_paws_fr = "Détendu"
    s_expr_fr = "Curiosité"
    s_pipo_pos = "À côté de la tête"
    s_energy = "Douce"

    if mode == "🕹️ MANUEL":
        st.divider()
        st.subheader(f"🛠️ RÉGLAGES {etape.split('.')[1]}")
        
        if "DÉCOR" in etape:
            s_decor_ui = st.selectbox("Lieu précis", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x])
            s_decor_ui = ville['decors'][s_decor_ui]
            s_angle_ui = st.selectbox("Angle de vue", ["Plan Large (Wide)", "Plan Moyen (Medium)", "Gros Plan (Close-up)", "Contre-plongée (Low angle)", "Subjectif (POV)"])
            s_light_ui = st.selectbox("Horaire", ["Aube (Golden Hour)", "Midi (High Sun)", "Crépuscule (Sunset)", "Heure Bleue", "Nuit Profonde"])
            s_mat_decor = st.selectbox("Matériaux du décor", ["Pierre & Béton", "Neige & Glace", "Eau & Reflets", "Métal & Verre"])
            s_season_fr = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_fg_fr = st.selectbox("Premier Plan", list(FG_MAP.keys()))

        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés", "Assis", "Accroupi", "Marche", "S'accroche"])
            s_expr_fr = st.selectbox("Expression facial", ["Curiosité", "Émerveillement", "Sourire", "Somnolence", "Concentration", "Surprise"])
            s_pipo_pos = st.selectbox("Position de Pipo", ["À côté de la tête", "Sur l'épaule", "Devant le torse", "En orbite"])
            s_pipo_col = st.selectbox("Couleur Pipo", ["Blanc Nacré", "Irisé Multicolore", "Lueur Pure"])
            s_acc_fr = st.text_input("Accessoire Mélo", value=ville['obj_fr'])
            s_palette = st.selectbox("Palette de couleurs", ["Naturelle", "Cinématique", "Pastel", "Contrastée"])

        elif "VIDÉO" in etape:
            s_action_fr = st.text_input("Mouvement (FR)", value=plan[ville['struct']])
            s_energy = st.selectbox("Trainée d'énergie Pipo", ["Douce", "Ruban éthéré", "Scintillante", "Forte"])
            s_speed = st.selectbox("Vitesse", ["Ultra-Slow (0.1x)", "Slow-Motion (0.5x)", "Temps Réel"])

# --- 7. ZONE D'AFFICHAGE CONTEXTUELLE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE & HEURE</div><div class="action-text">{s_angle_ui} | {s_light_ui}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">💎 MATÉRIAUX</div><div class="action-text">{s_mat_decor}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Décor (Anglais)")
    st.code(f"Environment Plate: {s_decor_ui}. Angle: {s_angle_ui}. Time: {s_light_ui}. Materials: {s_mat_decor}. Cinematic PBR. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 MÉLO</div><div class="action-text">{s_paws_fr} | {s_expr_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_pos}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🎒 OBJET</div><div class="action-text">{ville["obj_fr"]}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Intégration (Anglais)")
    st.code(f"Integration: MÉLO ({DNA_MELO}). Pose: {s_paws_fr}. Expression: {s_expr_fr}. PIPO ({DNA_PIPO}) at {s_pipo_pos}. Material: {MATERIAL_B22}. [LOCKS]: {TECHNICAL_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT AUTO/MANUEL</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🚀 ÉNERGIE PIPO</div><div class="action-text">{s_energy}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Vidéo (Anglais)")
    st.code(f"Animation (8s): {s_action_fr} in ultra-slow motion. Pipo energy trail: {s_energy}. Perfect loop, cinematic PBR.")

# --- 8. EXPORT FINAL ---
st.divider()
if st.button("💾 EXPORTER TOUS LES PROMPTS DU PLAN"):
    st.code(f"PLAN {p_id} - {ville['nom']}\nDECOR: {s_decor_ui}\nACTION: {s_action_fr}\nPOSE: {s_paws_fr}", language="text")
