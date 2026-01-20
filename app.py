import streamlit as st

# --- 1. ADN MÉLO & PIPO (BIBLE B22 - LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. TRADUCTEURS TECHNIQUES (FR -> EN) ---
FOREGROUND_MAP = {
    "Aucun": "clear ground with minimal dust",
    "Fleurs sauvages": "highly detailed PBR wild flowers in shallow depth of field, delicate petals with translucency",
    "Feuilles mortes": "scattered crisp autumn leaves, detailed vein textures, dry and crunchy look",
    "Flaques d'eau": "realistic water puddles with ray-traced reflections and wet mud textures",
    "Cailloux PBR": "highly detailed PBR pebbles and stones with wet shader, micro-surface roughness"
}

# --- 3. DONNÉES DE BASE (LIEUX & PLANS) ---
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

PLANS_DATA = {i: {"angle_ui": "Plan Moyen", "light_ui": "Aube", "light_en": "Golden Hour", "B_M_FR": f"Scène {i}", "B_M_EN": f"Scene {i}"} for i in range(1, 21)}

# --- 4. STYLE & CONFIGURATION ---
st.set_page_config(page_title="Melo Production Master", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTÉGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)

# --- 5. INITIALISATION DES VARIABLES (ANTI-ERREUR) ---
v_id = "eiffel_paris" # Valeur par défaut
ville = DESTINATIONS[v_id]
p_id = 1
plan = PLANS_DATA[p_id]
s_light_en = plan['light_en']
s_decor_en = ville['decors'][1]['en']
s_action_en = plan['B_M_EN']
s_weather_en = "Clear Sky"
s_season_en = "Spring"
s_foreground_en = FOREGROUND_MAP["Aucun"]
s_paws_en = "relaxed"
s_expr_en = "calm curiosity"
s_pipo_pose_en = "floating still"
s_pipo_pos_en = "near Melo's head"
s_palette_en = "cinematic natural colors"
s_pipo_col_en = "iridescent white"
s_energy_en = "soft glow"

# --- 6. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    if mode == "🤖 AUTOMATIQUE":
        s_decor_ui = ville['decors'][auto_d_id]['ui']
        s_action_fr = plan[f"{ville['struct']}_M_FR"]
    else:
        st.divider()
        st.subheader(f"🛠️ AJUSTEMENTS {etape.split('.')[1]}")
        
        if "DÉCOR" in etape:
            m_d_id = st.selectbox("Lieu précis", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
            s_decor_en = ville['decors'][m_d_id]['en']
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"
            s_season_ui = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_season_en = {"Printemps": "Spring", "Été": "Summer", "Automne": "Autumn", "Hiver": "Winter"}[s_season_ui]
            s_fg_ui = st.selectbox("Élément premier plan", list(FOREGROUND_MAP.keys()))
            s_foreground_en = FOREGROUND_MAP[s_fg_ui]

        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés"])
            s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
            s_expr_fr = st.selectbox("Expression Mélo", ["Curiosité", "Émerveillement", "Sourire"])
            s_expr_en = "curious"
            s_pipo_pose = st.selectbox("Pose Pipo", ["Flottement doux", "Rotation", "Statique"])
            s_pipo_pose_en = "softly floating"
            s_pipo_pos = st.selectbox("Position Pipo", ["À droite de la tête", "Sur l'épaule", "Devant le torse"])
            s_pipo_pos_en = "next to Melo's head"
            s_acc_fr = st.text_input("Melo accessory", value=ville['obj_fr'])
            s_palette = st.selectbox("Color palette", ["Naturelle", "Contraste élevé", "Pastel"])
            s_palette_en = "natural cinematic palette"
            s_pipo_col = st.selectbox("Pipo color", ["Blanc Nacré", "Irisé Multicolore", "Lueur Pure"])
            s_pipo_col_en = "iridescent white snow-potato texture"
            s_energy_fr = st.selectbox("Pipo energy trail", ["Minimaliste", "Ruban de lumière", "Scintillement"])
            s_energy_en = "minimal soft energy trail"

# --- 7. ZONE D'AFFICHAGE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")



if "DÉCOR" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{ville["decors"][auto_d_id]["ui"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🍂 SAISON</div><div class="action-text">{s_season_en}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌿 PREMIER PLAN</div><div class="action-text">{s_foreground_en}</div></div>', unsafe_allow_html=True)
    p_decor = f"Environment Plate: {s_decor_en}. Season: {s_season_en}. Foreground: {s_foreground_en}. Light: {s_light_en}. --ar 16:9"
    st.code(p_decor)

elif "IMAGE" in etape:
    st.markdown(f'<div class="info-card"><div class="action-title">🎭 CONFIGURATION B22 COMPLETE</div><div class="action-text">{s_paws_en} | {s_pipo_col_en} | Palette: {s_palette_en}</div></div>', unsafe_allow_html=True)
    p_image = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws_en}. Expression: {s_expr_en}. Pipo Pose: {s_pipo_pose_en} at {s_pipo_pos_en}. Color Palette: {s_palette_en}. Pipo: {s_pipo_col_en}. Energy: {s_energy_en}. [LOCKS]: {TECH_LOCKS}. --ar 16:9"
    st.code(p_image)

elif "VIDÉO" in etape:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT VIDÉO</div><div class="action-text">{s_energy_en}</div></div>', unsafe_allow_html=True)
    p_video = f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo energy trail: {s_energy_en}. Perfect loop."
    st.code(p_video)

# --- 8. BOUTON D'EXPORTATION GÉNÉRALE ---
st.divider()
st.subheader("📦 Exportation de Production")
if st.button("Générer le récapitulatif complet du plan"):
    full_export = f"""--- PLAN {p_id} EXPORT ---
PROMPT 1 (DÉCOR): Environment Plate: {s_decor_en}. Season: {s_season_en}. Foreground: {s_foreground_en}. Light: {s_light_en}. --ar 16:9

PROMPT 2 (IMAGE): Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws_en}. Expression: {s_expr_en}. Pipo: {s_pipo_col_en}. Energy: {s_energy_en}. [LOCKS]: {TECH_LOCKS}. --ar 16:9

PROMPT 3 (VIDÉO): Animation (8s): {s_action_en} in ultra-slow motion. Pipo energy trail: {s_energy_en}. Perfect loop.
----------------------"""
    st.code(full_export, language="text")
