import streamlit as st

# --- 1. ADN & LOCKS B22 (ANGLAIS POUR L'IA) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_MAIN = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."

# --- 2. TRADUCTEURS TECHNIQUES (FR -> EN) ---
FG_MAP = {
    "Aucun": "clear ground",
    "Fleurs sauvages": "highly detailed PBR wild flowers with subsurface scattering, shallow depth of field",
    "Feuilles mortes": "scattered crisp PBR autumn leaves, detailed vein textures, dry look",
    "Flaques d'eau": "realistic water puddles with ray-traced reflections and wet mud shader",
    "Cailloux PBR": "highly detailed PBR pebbles and stones with wet shader, micro-surface roughness"
}

# --- 3. DONNÉES DE BASE ---
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
PLANS_DATA[18].update({"B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge, slow, cinematic yawn"})
PLANS_DATA[20].update({"B_M_FR": "Sommeil profond", "B_M_EN": "Deep peaceful sleep"})

# --- 4. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Melo Director Studio", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Navigation par étapes (Onglets simulés en Français)
etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. INITIALISATION (SÉCURITÉ ANTI-ERREUR) ---
v_id = "eiffel_paris"
ville = DESTINATIONS[v_id]
p_id = 1
plan = PLANS_DATA[p_id]
s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
s_decor_ui, s_decor_en = ville['decors'][1]['ui'], ville['decors'][1]['en']
s_action_fr, s_action_en = plan['B_M_FR'], plan['B_M_EN']
s_season_fr, s_season_en = "Printemps", "Spring"
s_fg_fr, s_fg_en = "Aucun", FG_MAP["Aucun"]
s_angle_ui, s_angle_en = "Plan Moyen", "Medium shot"
s_weather_fr, s_weather_en = "Beau temps", "Clear Sky"
s_paws_fr, s_paws_en = "Détendu", "relaxed"
s_expr_fr, s_expr_en = "Curiosité", "curious"
s_pipo_pose_fr, s_pipo_pose_en = "Flottement doux", "softly floating"
s_pipo_pos_fr, s_pipo_pos_en = "À côté de la tête", "next to head"
s_palette_fr, s_palette_en = "Naturelle", "cinematic natural palette"
s_pipo_col_fr, s_pipo_col_en = "Blanc Nacré", "iridescent white"
s_energy_fr, s_energy_en = "Douce", "soft minimal energy trail"
s_acc_fr, s_acc_en = ville['obj_fr'], ville['obj_en']

# --- 6. LOGIQUE BARRE LATÉRALE (DYNAMIQUE) ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    if mode == "🤖 AUTOMATIQUE":
        s_decor_ui, s_decor_en = ville['decors'][auto_d_id]['ui'], ville['decors'][auto_d_id]['en']
        s_action_fr, s_action_en = plan[f"{ville['struct']}_M_FR"], plan[f"{ville['struct']}_M_EN"]
    else:
        st.divider()
        st.subheader(f"🛠️ RÉGLAGES {etape.split('.')[1]}")
        
        if "DÉCOR" in etape:
            m_d_id = st.selectbox("Lieu", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
            s_decor_ui, s_decor_en = ville['decors'][m_d_id]['ui'], ville['decors'][m_d_id]['en']
            s_season_fr = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_season_en = {"Printemps": "Spring", "Été": "Summer", "Automne": "Autumn", "Hiver": "Winter"}[s_season_fr]
            s_fg_fr = st.selectbox("Premier Plan", list(FG_MAP.keys()))
            s_fg_en = FG_MAP[s_fg_fr]
            s_angle_ui = st.selectbox("Angle", ["Plan Large", "Plan Moyen", "Gros Plan"])
            s_angle_en = "Wide shot" if "Large" in s_angle_ui else "Close-up"
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"

        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés", "S'accroche à l'objet"])
            s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
            s_expr_fr = st.selectbox("Expression Mélo", ["Curiosité", "Émerveillement", "Somnolence"])
            s_expr_en = "curious"
            s_pipo_pose_fr = st.selectbox("Pose Pipo", ["Flottement doux", "Statique", "Orbitale"])
            s_pipo_pos_fr = st.selectbox("Position Pipo", ["À côté de la tête", "Sur l'épaule", "Devant le torse"])
            s_acc_fr = st.text_input("Accessoire Mélo", value=ville['obj_fr'])
            s_palette_fr = st.selectbox("Palette de couleurs", ["Naturelle", "Pastel", "Contraste élevé"])
            s_pipo_col_fr = st.selectbox("Couleur Pipo", ["Blanc Nacré", "Irisé Multicolore"])
            s_energy_fr = st.selectbox("Trainée d'énergie Pipo", ["Douce", "Ruban éthéré", "Scintillante"])

        elif "VIDÉO" in etape:
            s_action_fr = st.text_input("Mouvement (FR)", value=plan[f"{ville['struct']}_M_FR"])
            s_action_en = "Huge slow yawn" if "bâillement" in s_action_fr else "Slow breathing"
            s_speed_ui = st.selectbox("Vitesse", ["Ultra-Slow", "Slow-Motion"])
            s_energy_fr = st.selectbox("Intensité de traînée", ["Faible", "Moyenne", "Forte"])

# --- 7. AFFICHAGE CONTEXTUEL ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🍂 SAISON</div><div class="action-text">{s_season_fr}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌿 PREMIER PLAN</div><div class="action-text">{s_fg_fr}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{s_light_ui}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Master Plate (Anglais)")
    st.code(f"Environment Plate: {s_decor_en}. Season: {s_season_en}. Foreground: {s_fg_en}. Angle: {s_angle_en}. Time: {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 POSE MÉLO</div><div class="action-text">{s_paws_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_col_fr}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🎨 PALETTE</div><div class="action-text">{s_palette_fr}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Intégration (Anglais)")
    st.code(f"Integration: MÉLO ({DNA_MELO}). Material: {MATERIAL_MAIN}. PIPO ({DNA_PIPO}). Pose: {s_paws_en}. Pipo: {s_pipo_col_fr}. Palette: {s_palette_fr}. [LOCKS]: {TECH_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🚀 ÉNERGIE</div><div class="action-text">{s_energy_fr}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Vidéo (Anglais)")
    st.code(f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo energy: {s_energy_fr}. Perfect loop, cinematic PBR.")

# --- 8. EXPORT DE PRODUCTION ---
st.divider()
st.subheader("📦 Exportation Générale")
if st.button("💾 Générer le récapitulatif complet"):
    export_text = f"""--- PRODUCTION EXPORT | PLAN {p_id} ---
DECOR: Environment Plate: {s_decor_en}. Season: {s_season_en}. Foreground: {s_fg_en}. --ar 16:9
IMAGE: Integration: MÉLO ({DNA_MELO}). Material: {MATERIAL_MAIN}. PIPO ({DNA_PIPO}). [LOCKS]: {TECH_LOCKS}. --ar 16:9
VIDEO: Animation (8s): {s_action_en} in ultra-slow motion. Perfect loop.
---------------------------------------"""
    st.code(export_text, language="text")
