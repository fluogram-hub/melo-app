import streamlit as st

# --- 1. CONFIGURATION VISUELLE ---
st.set_page_config(page_title="Mélo Studio Pro", layout="wide")

# Style personnalisé pour améliorer la lisibilité
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stCode { background-color: #1e1e1e !important; color: #d4d4d4 !important; border-radius: 10px; }
    .main-title { font-size: 32px; font-weight: bold; color: #0e1117; margin-bottom: 20px; }
    .section-header { font-size: 20px; font-weight: bold; color: #007bff; margin-top: 20px; }
    .metric-container { background: white; padding: 15px; border-radius: 10px; border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DONNÉES (LIEUX & PLANS) ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Béret rouge", "animal": "Caniche", "plate": "Esplanade vide, Tour Eiffel floue au loin."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Masque de chat", "animal": "Pigeon blanc", "plate": "Eau calme, palais flous en arrière-plan."},
    "lapland_arctic": {"name": "Laponie", "struct": "A", "obj": "Chocolat chaud", "animal": "Renne", "plate": "Neige immaculée, aurore boréale douce."}
}

# Paramètres par défaut pour le mode Auto
AUTO_CONFIG = {
    "light": "Golden Hour", "weather": "Clear Sky", "expr": "Curiosité calme", 
    "gaze": "Vers l'horizon", "paws": "Détendu", "action": "Respiration lente"
}

# --- 3. BARRE LATÉRALE (CONTRÔLES) ---
with st.sidebar:
    st.markdown("<div class='main-title'>🎬 RÉGLAGES</div>", unsafe_allow_html=True)
    
    mode = st.radio("Système de contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    
    st.divider()
    
    lieu_id = st.selectbox("Destination", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    plan_id = st.number_input("Numéro du Plan", 1, 20, 1)
    
    if mode == "🤖 AUTOMATIQUE":
        # En mode auto, on affiche les valeurs mais on ne peut pas les changer
        st.success("Mode automatique activé. L'appli suit la bible Excel.")
        h_val, m_val, e_val = AUTO_CONFIG["light"], AUTO_CONFIG["weather"], AUTO_CONFIG["expr"]
        g_val, p_val, a_val = AUTO_CONFIG["gaze"], AUTO_CONFIG["paws"], AUTO_CONFIG["action"]
        acc_val = LIEUX[lieu_id]["obj"]
    else:
        st.warning("Mode manuel : définissez vos propres poses.")
        h_val = st.selectbox("Horaire", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        m_val = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])
        e_val = st.selectbox("Expression", ["Curiosité", "Sourire doux", "Émerveillement", "Somnolence"])
        g_val = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon", "Vers l'objet"])
        p_val = st.selectbox("Anatomie (Pattes)", ["Détendu", "Patte gauche levée", "Bras croisés", "Pattes derrière le dos", "S'accroche à l'objet"])
        a_val = st.selectbox("Mouvement Vidéo", ["Respiration", "Salut lent", "Hochement de tête", "Sert l'objet"])
        acc_val = st.text_input("Accessoire de Mélo", value=LIEUX[lieu_id]["obj"])

# --- 4. AFFICHAGE PRINCIPAL (LISIBILITÉ) ---
st.markdown(f"<div class='main-title'>PLATEAU : {LIEUX[lieu_id]['name']} | PLAN {plan_id}</div>", unsafe_allow_html=True)

# Dashboard de lecture rapide (Horizontal et aéré)
st.markdown("<div class='section-header'>📋 FICHE TECHNIQUE ACTUELLE</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"**ATMOSPHÈRE**\n\n🌅 {h_val}\n\n☁️ {m_val}")
with c2:
    st.markdown(f"**VISAGE**\n\n🎭 {e_val}\n\n👁️ Regard: {g_val}")
with c3:
    st.markdown(f"**CORPS & OBJET**\n\n🐾 {p_val}\n\n🎒 {acc_val}")
with c4:
    st.markdown(f"**MOUVEMENT**\n\n🎞️ {a_val}")

st.divider()

# --- 5. LES PROMPTS (DANS DES BLOCS SÉPARÉS) ---
st.markdown("<div class='section-header'>🚀 GÉNÉRATEUR DE PROMPTS</div>", unsafe_allow_html=True)

# Onglets larges et lisibles
tab1, tab2, tab3 = st.tabs(["[ 1. FOND ]", "[ 2. IMAGE ]", "[ 3. VIDÉO ]"])

with tab1:
    st.write("### 🖼️ Prompt Décor (Master Plate)")
    st.markdown("*Générez d'abord le fond vide pour garantir la stabilité.*")
    p1 = f"Environment: {LIEUX[lieu_id]['plate']} Time: {h_val}. Weather: {m_val}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tab2:
    st.write("### 🎨 Prompt Intégration (Nanobanana)")
    st.markdown("*Utilisez ce prompt pour placer Mélo et Pipo dans le décor.*")
    melo_spec = f"Melo pose: {p_val}, gaze: {g_val}, expression: {e_val}, holding: {acc_val}."
    p2 = f"Integration: 45cm blue Glass Suit character. {melo_spec} Companion: Pipo (small white spirit). {h_val}, {m_val}. [LOCKS]: Cinematic PBR, 8k. --ar 16:9"
    st.code(p2, language="text")

with tab3:
    st.write("### 🎞️ Prompt Animation (Veo 3)")
    st.markdown("*Utilisez ce prompt pour créer le mouvement de 8 secondes.*")
    p3 = f"Animation (8s): {a_val} in ultra-slow motion. Melo looking {g_val}. Pipo trailing soft light. {m_val} effects. Perfect loop, cinematic PBR."
    st.code(p3, language="text")

# --- 6. EXPORT ---
st.divider()
with st.expander("💾 EXPORTER LA CONFIGURATION"):
    st.text_area("Copier le récapitulatif", f"PLAN_{plan_id}_{LIEUX[lieu_id]['name']}: {h_val}/{m_val} | {p_val}/{g_val} | {a_val}")
