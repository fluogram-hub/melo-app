import streamlit as st

# --- 1. BIBLE B22 : ADN & LOCKS (ANGLAIS POUR L'IA) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile."
TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. DONNÉES DE BASE ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
            2: {"ui": "Les Quais de Seine", "en": "Wet cobblestone banks, soft river ripples, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Macro view of iron lattice structure, sharp focus on metal textures."},
            4: {"ui": "Le Champ-de-Mars", "en": "Minimalist green grass field, distant blurry tower."}
        }
    }
}

PLANS_DATA = {i: {"light_ui": "Aube", "light_en": "Golden Hour", "B_M_FR": f"Action Plan {i}", "B_M_EN": f"Action {i}"} for i in range(1, 21)}
PLANS_DATA[18].update({"B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge, slow, cinematic yawn"})
PLANS_DATA[20].update({"B_M_FR": "S'endort paisiblement", "B_M_EN": "Deep peaceful sleep"})

# --- 3. STYLE CSS ---
st.set_page_config(page_title="Mélo Production Hub", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BARRE LATÉRALE (DYNAMIQUE) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    
    # ÉTAPE DE PRODUCTION (Remplace les onglets pour le contrôle Sidebar)
    etape = st.radio("ÉTAPE DE TRAVAIL", ["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTÉGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])
    
    st.divider()
    
    mode = st.radio("MODE DE CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # --- RÉGLAGES CONTEXTUELS EN MODE MANUEL ---
    st.divider()
    if mode == "🕹️ MANUEL":
        st.subheader("🛠️ RÉGLAGES MANUELS")
        
        if etape == "🖼️ 1. DÉCOR (PLATE)":
            m_decor_id = st.selectbox("Choisir le décor", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
            m_light = st.selectbox("Horaire", ["Aube (Golden Hour)", "Midi (High Sun)", "Crépuscule (Sunset)", "Nuit (Deep Night)"])
            m_weather = st.selectbox("Météo", ["Ciel dégagé", "Pluie", "Neige", "Brouillard"])
            
            # Mapping
            s_decor_ui, s_decor_en = ville['decors'][m_decor_id]['ui'], ville['decors'][m_decor_id]['en']
            s_light_en = "Golden Hour" if "Aube" in m_light else "Deep Night"
            s_weather_en = "Clear Sky"
            
        elif etape == "🎨 2. IMAGE (INTÉGRATION)":
            m_paws = st.selectbox("Pose des pattes", ["Détendu", "Patte levée", "Bras croisés", "Derrière le dos"])
            m_gaze = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon", "Vers le sol"])
            m_pipo_col = st.selectbox("Reflets Pipo", ["Nacré Irisé", "Lueur Blanche", "Multicolore doux"])
            m_material = st.selectbox("Rendu Verre", ["Ultra Glossy", "Satiné", "Translucide Gélatineux"])
            
            # Mapping
            s_paws_en = "relaxed" if m_paws == "Détendu" else "one paw raised"
            s_pipo_color_en = "iridescent multicolor pearl reflections"
            s_material_en = "transparent blue glass effect, high glossy"
            s_action_en = plan[f"{ville['struct']}_M_EN"]
            s_action_fr = plan[f"{ville['struct']}_M_FR"]
            s_light_en = plan['light_en']
            s_decor_en = ville['decors'][auto_d_id]['en']
            
        elif etape == "🎞️ 3. VIDÉO (MOUVEMENT)":
            m_action = st.text_input("Mouvement (FR)", value=plan[f"{ville['struct']}_M_FR"])
            m_energy = st.selectbox("Trainée Pipo", ["Minimaliste", "Ruban éthéré", "Lueur traînante"])
            m_speed = st.selectbox("Vitesse", ["Ultra-Slow", "Slow-Motion", "Temps Réel"])
            
            # Mapping
            s_action_en = "Huge slow yawn" if "bâillement" in m_action else "Moving slowly"
            s_energy_en = "minimal bedtime-friendly energy trail"
            s_speed_en = m_speed.lower()
            s_decor_ui = ville['decors'][auto_d_id]['ui']
    
    # --- LOGIQUE AUTOMATIQUE (BACKUP) ---
    if mode == "🤖 AUTOMATIQUE":
        s_decor_ui = ville['decors'][auto_d_id]['ui']
        s_decor_en = ville['decors'][auto_d_id]['en']
        s_action_fr = plan[f"{ville['struct']}_M_FR"]
        s_action_en = plan[f"{ville['struct']}_M_EN"]
        s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
        s_weather_ui, s_weather_en = "Ciel Dégagé", "Clear Sky"
        s_material_en = "transparent blue glass effect, high glossy"
        s_pipo_color_en = "subtle iridescent multicolor pearl reflections"
        s_paws_fr, s_paws_en = "Détendu", "relaxed"
        s_gaze_fr, s_gaze_en = "Vers l'horizon", "horizon"
        s_energy_en = "minimal bedtime-friendly energy trail"

# --- 5. AFFICHAGE CONTEXTUEL (MAIN AREA) ---
st.title(f"{etape}")

if "DÉCOR" in etape:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">📍 LIEU</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🌅 AMBIANCE</div><div class="action-text">{plan["light_ui"]}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Décor (Plate)")
    st.code(f"Environment Plate: {s_decor_en} {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">💎 MATIÈRE</div><div class="action-text">Verre IOR 1.5</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_color_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Intégration (Nanobanana)")
    st.code(f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Material: {s_material_en}. Pipo: {s_pipo_color_en}. Pose: {s_action_en}. Decor: {s_decor_en}. {TECHNICAL_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🚀 TRAINÉE ÉNERGÉTIQUE</div><div class="action-text">{s_energy_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Vidéo (Veo 3)")
    st.code(f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo energy trail: {s_energy_en}. Glossy glass suit reflections. Perfect loop.")
