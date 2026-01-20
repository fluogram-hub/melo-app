import streamlit as st

# --- 1. BIBLE B22 : DNA & LOCKS (ANGLAIS) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile."
MATERIAL_B22 = "Homogeneous transparent blue glass, no internal anatomy, high IOR 1.5, caustics, micro-reflections."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography."

# --- 2. DONNÉES (DESTINATIONS & PLANS) ---
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

PLANS_DATA = {i: {"light_ui": "Aube", "light_en": "Golden Hour", "B_M_FR": f"Action Plan {i}", "B_M_EN": f"Action {i}"} for i in range(1, 21)}
PLANS_DATA[18].update({"B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge, slow, cinematic yawn"})
PLANS_DATA[20].update({"B_M_FR": "S'endort paisiblement", "B_M_EN": "Deep peaceful sleep"})

# --- 3. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Mélo Production Hub", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    /* Style pour simuler des onglets avec le radio */
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION PRINCIPALE (REMPLACE LES TABS POUR LA DYNAMIQUE) ---
# On place le sélecteur d'étape en haut de la zone principale
etape = st.radio("SÉLECTIONNER L'ÉTAPE DE PRODUCTION :", 
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
    
    # 1. INITIALISATION DES VALEURS PAR DÉFAUT (AUTO)
    s_decor_ui = ville['decors'][auto_d_id]['ui']
    s_decor_en = ville['decors'][auto_d_id]['en']
    s_action_fr = plan[f"{ville['struct']}_M_FR"]
    s_action_en = plan[f"{ville['struct']}_M_EN"]
    s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
    s_weather_ui, s_weather_en = "Beau temps", "Clear Sky"
    s_paws_fr, s_paws_en = "Détendu", "relaxed"
    s_gaze_fr, s_gaze_en = "Vers l'horizon", "horizon"
    s_material = MATERIAL_B22
    s_pipo_col_fr, s_pipo_col_en = "Nacré irisé", "iridescent multicolor reflections"
    s_energy_fr, s_energy_en = "Minimaliste", "minimal bedtime-friendly energy trail"

    # 2. SURCHARGE MANUELLE SI BESOIN
    if mode == "🕹️ MANUEL":
        st.divider()
        st.subheader("🛠️ AJUSTEMENTS MANUELS")
        
        if "DÉCOR" in etape:
            m_d_id = st.selectbox("Choisir le décor", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
            s_decor_ui, s_decor_en = ville['decors'][m_d_id]['ui'], ville['decors'][m_d_id]['en']
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"
            
        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Position Pattes", ["Détendu", "Patte levée", "Bras croisés", "Derrière le dos"])
            s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
            s_gaze_fr = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])
            s_pipo_col_fr = st.selectbox("Couleur Pipo", ["Nacré irisé", "Lueur blanche", "Multicolore"])
            s_material = st.selectbox("Rendu Verre Mélo", [MATERIAL_B22, "Verre Satiné", "Effet Gélatineux"])
            
        elif "VIDÉO" in etape:
            s_action_fr = st.text_input("Mouvement (FR)", value=plan[f"{ville['struct']}_M_FR"])
            s_action_en = "Huge slow yawn" if "bâillement" in s_action_fr else "Slow breathing motion"
            s_energy_fr = st.selectbox("Trainée Énergie Pipo", ["Minimaliste", "Ruban éthéré", "Lueur traînante"])
            s_energy_en = "minimal bedtime-friendly energy trail"

# --- 6. ZONE D'AFFICHAGE (MAIN AREA) ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🌅 AMBIANCE</div><div class="action-text">{s_light_ui}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Décor (Solid Plate)")
    st.code(f"Environment Plate: {s_decor_en} {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🐾 ANATOMIE</div><div class="action-text">{s_paws_fr} | {s_gaze_fr}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_col_fr}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Intégration (B22 Specs)")
    p2 = f"Integration: MÉLO ({DNA_MELO}). Material: {s_material}. Pipo: {DNA_PIPO} with {s_pipo_col_en}. Pose: {s_action_en}. {TECH_LOCKS}. --ar 16:9"
    st.code(p2)

elif "VIDÉO" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🚀 ÉNERGIE PIPO</div><div class="action-text">{s_energy_fr}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Vidéo (Veo 3)")
    p3 = f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo energy: {s_energy_en}. Perfect loop."
    st.code(p3)
