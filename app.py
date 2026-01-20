import streamlit as st

# --- 1. CONFIGURATION & ADN (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long smooth blue ribbons."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. DONNÉES EXTRAITES DE TON EXCEL ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, blurry distant Eiffel Tower silhouette."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, soft ripples, blurry palaces."},
    "lapland_arctic": {"name": "Laponie", "struct": "A", "obj": "Steaming mug", "animal": "Reindeer", "plate": "Vast white snowfield, aurora glow."}
}

PLANS_AUTO = {
    1: {"angle": "Wide", "light": "Golden Hour", "weather": "Clear Sky"},
    10: {"angle": "Close-up", "light": "Blue Hour", "weather": "Misty"},
    18: {"angle": "Close-up", "light": "Deep Night", "weather": "Clear Sky"},
    20: {"angle": "Wide", "light": "Deep Night", "weather": "Clear Sky"}
}

EXPRESSIONS = ["Curiosité calme", "Sourire Duchenne", "Émerveillement", "Somnolence", "Tristesse poétique"]
POSES = ["Assis", "Debout immobile", "Marche lente", "En lévitation légère", "Accroupi"]

# --- 3. INTERFACE ---
st.set_page_config(page_title="Mélo Studio", layout="wide")
st.title("🎬 Mélo Studio : Contrôle de Production")

with st.sidebar:
    st.header("🎯 Configuration de Scène")
    mode = st.radio("Mode de Génération", ["Automatique (Excel)", "Manuel (Custom)"])
    l_id = st.selectbox("Lieu", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    p_id = st.number_input("Numéro du Plan", min_value=1, max_value=20, value=1)
    
    st.divider()
    
    # --- LOGIQUE AUTO vs MANUEL ---
    lieu = LIEUX[l_id]
    plan_ref = PLANS_AUTO.get(p_id, {"angle": "Medium", "light": "Sunset", "weather": "Clear Sky"})
    
    if mode == "Automatique (Excel)":
        st.info(f"💡 Mode Auto : Paramètres issus du Plan de Réalisation.")
        sel_light = plan_ref["light"]
        sel_weather = plan_ref["weather"]
        sel_expr = EXPRESSIONS[0]
        sel_acc = lieu["obj"]
        sel_pose = POSES[1]
    else:
        st.warning("🕹️ Mode Manuel : Vous avez le contrôle.")
        sel_light = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"], index=0)
        sel_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Foggy"], index=0)
        sel_expr = st.selectbox("Expression de Mélo", EXPRESSIONS)
        sel_pose = st.selectbox("Pose de Mélo", POSES)
        sel_acc = st.text_input("Accessoire (ou laisser objet local)", value=lieu["obj"])

# --- 4. TABLEAU DE BORD DU RÉALISATEUR ---
st.subheader(f"Plateau : {lieu['name']} | Plan {p_id} | Structure {lieu['struct']}")

# Affichage des réglages actuels pour lecture facile
cols = st.columns(4)
cols[0].metric("Horaire", sel_light)
cols[1].metric("Météo", sel_weather)
cols[2].metric("Expression", sel_expr)
cols[3].metric("Accessoire", sel_acc)

st.divider()

# --- 5. GÉNÉRATION DES PROMPTS (LISIBILITÉ MAXIMALE) ---
melo_full_desc = f"{MELO_DNA}. Expression: {sel_expr}. Pose: {sel_pose}. Accessory: {sel_acc}."
atmo = f"{sel_light}, {sel_weather}."

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DECOR (PLATE)", "🎨 2. INTEGRATION (IMAGE)", "🎞️ 3. MOUVEMENT (VIDEO)"])

with tab1:
    st.info("Utilisez ce prompt pour générer le décor vide (Master Plate).")
    p1 = f"Environment Plate: {lieu['plate']} {atmo} POETIC, MINIMALIST, high-end photography. --ar 16:9"
    st.code(p1, language="text")

with tab2:
    st.info("Utilisez ce prompt avec l'Image 1 de Mélo en 'Character Reference'.")
    p2 = f"Integration: {melo_full_desc} and {PIPO_DNA}. Location: {lieu['name']}. {plan_ref['angle']} perspective. {atmo} [VERROUS]: {VERROUS}."
    st.code(p2, language="text")

with tab3:
    st.info("Utilisez ce prompt pour animer l'image générée (Veo 3 / Runway).")
    p3 = f"Animation (8s): Melo in {sel_pose} motion. {sel_expr} breathing. {sel_weather} particles moving slowly. Pipo trailing light. Cinematic PBR."
    st.code(p3, language="text")

st.markdown(f"""
> **Notes de Mise en Scène :** > Pour ce plan à **{lieu['name']}**, Mélo est positionné en **{plan_ref['angle']}**. 
> L'interaction est centrée sur l'accessoire **{sel_acc}**.
""")
