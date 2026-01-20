import streamlit as st

# --- 1. ADN DES PERSONNAGES (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. DONNÉES LIEUX ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, blurry distant Eiffel Tower silhouette."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, soft ripples, blurry palaces."},
    "lapland_arctic": {"name": "Laponie", "struct": "A", "obj": "Steaming mug", "animal": "Reindeer", "plate": "Vast white snowfield, aurora glow."}
}

# --- 3. OPTIONS DE MISE EN SCÈNE ---
EXPRESSIONS = ["Curiosité calme", "Sourire Duchenne", "Émerveillement", "Somnolence", "Tristesse poétique", "Concentration"]
REGARDS = ["Droit devant", "Vers Pipo", "Vers l'horizon", "Vers le monument", "Vers l'accessoire", "Vers le sol"]
POSES_PATTES = [
    "Détendu (pendantes)", 
    "Bras croisés", 
    "Patte gauche levée (curiosité)", 
    "Pattes derrière le dos", 
    "S'accroche à l'accessoire", 
    "Mains sur les hanches", 
    "Se frotte les yeux"
]

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Director Studio", layout="wide")
st.title("🎬 Mélo Studio : Direction d'Acteur & Anatomie")

with st.sidebar:
    st.header("🎯 Configuration")
    mode = st.radio("Mode de Génération", ["Automatique (Excel)", "Manuel (Custom)"])
    l_id = st.selectbox("Lieu", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    p_id = st.number_input("Plan n°", min_value=1, max_value=20, value=1)
    
    st.divider()
    
    lieu = LIEUX[l_id]
    
    if mode == "Automatique (Excel)":
        st.info("💡 Mode Auto : Paramètres hérités du scénario.")
        # Valeurs par défaut pour le mode auto (simulé ici)
        sel_light, sel_weather = "Golden Hour", "Clear Sky"
        sel_expr, sel_gaze, sel_paws = EXPRESSIONS[0], REGARDS[0], POSES_PATTES[0]
        sel_acc = lieu["obj"]
    else:
        st.warning("🕹️ Mode Manuel")
        sel_light = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night", "Dawn"])
        sel_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Foggy"])
        sel_expr = st.selectbox("Expression de Mélo", EXPRESSIONS)
        sel_gaze = st.selectbox("Où regarde Mélo ?", REGARDS)
        sel_paws = st.selectbox("Position des pattes", POSES_PATTES)
        sel_acc = st.text_input("Accessoire", value=lieu["obj"])

# --- 5. TABLEAU DE BORD (CAPTURE DE PROD) ---
st.subheader(f"Fiche de Tournage : {lieu['name']} | Plan {p_id}")

# Affichage clair des paramètres choisis
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.write("**Ambiance**")
    st.caption(f"🌅 {sel_light}")
    st.caption(f"☁️ {sel_weather}")
with c2:
    st.write("**Visage**")
    st.caption(f"🎭 {sel_expr}")
    st.caption(f"👁️ Regard : {sel_gaze}")
with c3:
    st.write("**Corps**")
    st.caption(f"🐾 {sel_paws}")
    st.caption(f"🎒 {sel_acc}")
with c4:
    st.write("**Acteur 2**")
    st.caption(f"✨ Pipo : {PIPO_DNA[:30]}...")

st.divider()

# --- 6. GÉNÉRATION DES PROMPTS ---
melo_anatomy = f"Pose: {sel_paws}. Gaze: looking {sel_gaze}. Expression: {sel_expr}. Accessory: {sel_acc}."
atmo = f"{sel_light}, {sel_weather}."

tabs = st.tabs(["🖼️ 1. DECOR", "🎨 2. IMAGE", "🎞️ 3. VIDEO"])

with tabs[0]:
    p1 = f"Environment Plate: {lieu['plate']} {atmo} POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tabs[1]:
    # Ici on injecte les verrous de pose et regard
    p2 = f"Integration: {MELO_DNA}. {melo_anatomy} Companion: {PIPO_DNA}. Location: {lieu['name']}. {atmo} [VERROUS]: {VERROUS}."
    st.code(p2, language="text")

with tabs[2]:
    p3 = f"Animation (8s): Melo {melo_anatomy}. Ultra-slow motion breathing. Pipo soft light trail. {sel_weather} effects. Perfect loop, cinematic PBR."
    st.code(p3, language="text")

# --- 7. RÉCAPITULATIF DE CAPTURE ---
with st.expander("📝 Récapitulatif pour export"):
    summary = f"LIEU: {lieu['name']} | PLAN: {p_id} | POSE: {sel_paws} | REGARD: {sel_gaze} | ACC: {sel_acc}"
    st.text_area("Copier la fiche technique", summary)
    
