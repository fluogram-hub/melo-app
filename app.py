import streamlit as st

# --- 1. BIBLE B22 : PARAMÈTRES TECHNIQUES (ANGLAIS POUR L'IA) ---
DNA_MELO = """Bunny-shaped high-end designer toy. Wearing a blue glass suit (transparent blue glass effect), ultra-glossy resin finish. 
White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."""

MATERIAL_MAIN = "Homogeneous transparent blue jelly/glass, no internal anatomy, high light refraction (IOR 1.5), realistic caustics, micro-reflections."

DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile."
PIPO_COLOR = "Solid white base with subtle iridescent multicolor pearl reflections (opalescent)."
PIPO_ENERGY_TRAIL = "Soft constant glow, minimal bedtime-friendly energy trail, no flickering, ethereal light ribbon."

TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES : DÉCORS & PLANS ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
            2: {"ui": "Les Quais de Seine", "en": "Wet cobblestone banks, soft river ripples, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Macro view of iron lattice structure, sharp focus on metal textures, low angle perspective."},
            4: {"ui": "Le Champ-de-Mars", "en": "Minimalist green grass field, distant blurry tower."}
        }
    }
}

PLANS_DATA = {i: {"angle": "Medium shot", "light_ui": "Aube", "light_en": "Golden Hour", "B_M_FR": f"Action Plan {i}", "B_M_EN": f"Action {i}"} for i in range(1, 21)}
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

# --- 4. BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    
    # RÉINTÉGRATION DU CHOIX MANUEL / AUTO
    mode = st.radio("Mode de contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    
    st.divider()
    
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("Numéro du Plan (Scénario)", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    struct = ville['struct']
    
    # Logique de calcul du décor auto
    auto_d_id = (p_id - 1) // 5 + 1
    
    if mode == "🤖 AUTOMATIQUE":
        st.success("Mode scénario activé.")
        s_decor_ui = ville['decors'][auto_d_id]['ui']
        s_decor_en = ville['decors'][auto_d_id]['en']
        s_action_fr = plan[f"{struct}_M_FR"]
        s_action_en = plan[f"{struct}_M_EN"]
        s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
        s_weather_ui, s_weather_en = "Ciel Dégagé", "Clear Sky"
        s_paws_fr, s_paws_en = "Détendu", "relaxed"
    else:
        st.warning("Mode manuel activé.")
        manual_d = st.selectbox("Choisir le décor", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x]['ui'])
        s_decor_ui = ville['decors'][manual_d]['ui']
        s_decor_en = ville['decors'][manual_d]['en']
        s_action_fr = st.text_input("Action Mélo (FR)", value=plan[f"{struct}_M_FR"])
        s_action_en = "Walking slowly" # Version EN simplifiée pour le manuel
        s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Heure Bleue", "Nuit"])
        s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"
        s_weather_ui = st.selectbox("Météo", ["Beau temps", "Pluie", "Neige"])
        s_weather_en = "Clear Sky"
        s_paws_fr = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés"])
        s_paws_en = "relaxed"

# --- 5. ZONE DE TRAVAIL CONTEXTUELLE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🌅 AMBIANCE</div><div class="action-text">{s_light_ui} | {s_weather_ui}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Décor (Plate)")
    st.code(f"Environment Plate: {s_decor_en} {s_light_en}. Weather: {s_weather_en}. POETIC, MINIMALIST. --ar 16:9")

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION & ANATOMIE</div><div class="action-text">{s_action_fr} | {s_paws_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">💎 MATIÈRE MÉLO (B22)</div><div class="action-text">Glass Suit | IOR 1.5</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO SPECS</div><div class="action-text">Pearl Iridescent | 5-10% scale</div></div>', unsafe_allow_html=True)

    st.subheader("Prompt Intégration (Solid B22 Specs)")
    p2 = f"Character Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Material: {MATERIAL_MAIN}. Pipo Specs: {PIPO_COLOR}. Pose: {s_action_en}. Decor: {s_decor_en}. [LOCKS]: {TECHNICAL_LOCKS}. --ar 16:9"
    st.code(p2)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT (8S)</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🚀 ÉNERGIE PIPO</div><div class="action-text">{PIPO_ENERGY_TRAIL}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Vidéo (Veo 3 Motion)")
    p3 = f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo energy trail: {PIPO_ENERGY_TRAIL}. Realistic glass caustics. Perfect loop."
    st.code(p3)
