import streamlit as st

# --- 1. ADN & LOCKS (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long blue ribbons."
PIPO_DNA = "Small spirit companion, white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. DONNÉES LIEUX ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, blurry Eiffel Tower silhouette."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, ripples, blurry palaces."},
    "taj_mahal_india": {"name": "Taj Mahal", "struct": "A", "obj": "Oil lantern", "animal": "Peacock", "plate": "Symmetrical white marble, reflecting pool."}
}

# --- 3. OPTIONS DE DIRECTION D'ACTEUR ---
EXPRESSIONS = ["Curiosité calme", "Sourire doux", "Émerveillement", "Somnolence", "Concentration"]
REGARDS = ["Droit devant", "Vers Pipo", "Vers l'horizon", "Vers l'accessoire", "Vers le sol"]
POSES_PATTES = ["Détendu", "Bras croisés", "Patte levée", "Pattes derrière le dos", "S'accroche à l'objet"]
ACTIONS_VIDEO = [
    "Respiration lente (mouvement d'épaules)", 
    "Hochement de tête très lent", 
    "Clignement d'yeux et petit sourire", 
    "Salut de la patte très lent", 
    "Sert l'accessoire contre lui", 
    "Se tourne lentement vers la caméra"
]

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Video Studio", layout="wide")
st.title("🎬 Mélo Studio : Direction & Mouvement")

with st.sidebar:
    st.header("🎯 Paramètres de Production")
    mode = st.radio("Mode", ["Automatique (Excel)", "Manuel (Custom)"])
    l_id = st.selectbox("Lieu", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    p_id = st.number_input("Séquence n°", 1, 20, 1)
    
    st.divider()
    
    lieu = LIEUX[l_id]
    
    if mode == "Automatique (Excel)":
        st.info("💡 Mode Auto activé")
        s_light, s_weather = "Golden Hour", "Clear Sky"
        s_expr, s_gaze, s_paws, s_video = EXPRESSIONS[0], REGARDS[0], POSES_PATTES[0], ACTIONS_VIDEO[0]
        s_acc = lieu["obj"]
    else:
        st.warning("🕹️ Mode Manuel activé")
        s_light = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        s_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])
        s_expr = st.selectbox("Expression", EXPRESSIONS)
        s_gaze = st.selectbox("Regard", REGARDS)
        s_paws = st.selectbox("Position des pattes", POSES_PATTES)
        s_video = st.selectbox("Mouvement Vidéo (8s)", ACTIONS_VIDEO)
        s_acc = st.text_input("Accessoire", value=lieu["obj"])

# --- 5. DASHBOARD LISIBLE ---
st.markdown(f"### 📋 Fiche Technique : {lieu['name']} | Plan {p_id}")

# Organisation en tuiles pour une lecture instantanée
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.help("**Ambiance**\n\n" + f"{s_light}\n\n{s_weather}")
with c2:
    st.help("**Visage**\n\n" + f"{s_expr}\n\nRegard: {s_gaze}")
with c3:
    st.help("**Corps**\n\n" + f"{s_paws}\n\nAcc: {s_acc}")
with c4:
    st.help("**Vidéo**\n\n" + f"Action: {s_video}")

st.divider()

# --- 6. GÉNÉRATION DES PROMPTS (TABS LISIBLES) ---
melo_stat = f"Pose: {s_paws}. Gaze: {s_gaze}. Expression: {s_expr}. Accessory: {s_acc}."
atmo = f"{s_light}, {s_weather}."

tabs = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tabs[0]:
    st.markdown("#### `Générer le décor vide d'abord`")
    p1 = f"Environment Plate: {lieu['plate']} {atmo} POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tabs[1]:
    st.markdown("#### `Intégrer Mélo & Pipo (Image-to-Image)`")
    p2 = f"Integration: {MELO_DNA}. {melo_stat} Companion: {PIPO_DNA}. Location: {lieu['name']}. {atmo} [VERROUS]: {VERROUS}."
    st.code(p2, language="text")

with tabs[2]:
    st.markdown("#### `Animer la scène (8 secondes)`")
    # L'action vidéo est ici la clé du prompt Veo 3
    p3 = f"Animation (8s): {s_video}. Melo is {s_expr} while looking {s_gaze}. Ultra-slow motion. Inertia on ribbons. {s_weather} particles. Perfect loop, cinematic PBR."
    st.code(p3, language="text")

# --- 7. EXPORT ---
with st.expander("💾 Sauvegarder la configuration du plan"):
    final_log = f"PLAN_{p_id}_{lieu['name']}: {s_expr} | {s_paws} | {s_video} | {s_light}"
    st.text_area("Copie cette ligne pour ton suivi de production", final_log)
