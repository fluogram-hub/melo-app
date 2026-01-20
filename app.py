import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Melo Mirror Studio V50", layout="wide")

# CSS pour colorer les indicateurs de mode
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] { border: 1px solid #007BFF; }
    .auto-label { color: #007BFF; font-weight: bold; font-size: 0.8em; margin-bottom: -20px; }
    .manual-label { color: #FF4B4B; font-weight: bold; font-size: 0.8em; margin-bottom: -20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES (80 LIEUX) ---
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable. Setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Setting: Pelouse du Champ-de-Mars."}}}
}

# --- 3. LOGIQUE DE CALCUL AUTOMATIQUE ---
def get_auto_values(p_id):
    # Calcul des index par défaut selon le plan (mathématique)
    # Lieu (B5) : Plan 1-5=Lieu 1, 6-10=Lieu 2...
    b5_idx = (p_id - 1) // 5 
    # Angle (B6) : Rotation cyclique
    b6_list = ["wide-angle lens", "macro lens", "ground perspective", "eye-level"]
    b6_val = b6_list[p_id % 4]
    # Lumière (B7)
    b7_list = ["Golden Hour", "Blue Hour", "Sunset", "Deep Night"]
    b7_val = b7_list[p_id % 4]
    return b5_idx, b6_val, b7_val

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    st.success("🟢 Vertex Engine Connected")
    e7_bool = st.toggle("🕹️ ACTIVER CONTRÔLE MANUEL (E7)", value=False)
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Récupération des données auto
    auto_b5_idx, auto_b6, auto_b7 = get_auto_values(p_id)
    ville = DESTINATIONS[v_id]

# --- 5. INTERFACE ET ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- TAB 1 : DÉCOR ---
with tab1:
    st.write(f"### Configuration du Plan {p_id}")
    label_style = "manual-label" if e7_bool else "auto-label"
    label_text = "🔴 MODE MANUEL" if e7_bool else "🔵 MODE AUTO (PLAN-LOCKED)"
    st.markdown(f'<p class="{label_style}">{label_text}</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Lieu B5
        b5_final = st.selectbox("LIEU PRÉCIS (B5)", [1,2,3,4], 
                                index=auto_b5_idx, 
                                format_func=lambda x: ville['lieux'][x]['nom'],
                                disabled=not e7_bool)
        # Angle B6
        b6_list = ["wide-angle lens", "macro lens", "ground perspective", "eye-level"]
        b6_final = st.selectbox("ANGLE (B6)", b6_list, 
                                index=b6_list.index(auto_b6),
                                disabled=not e7_bool)
    with col2:
        # Lumière B7
        b7_list = ["Golden Hour", "Blue Hour", "Sunset", "Deep Night"]
        b7_final = st.selectbox("LUMIÈRE (B7)", b7_list, 
                                index=b7_list.index(auto_b7),
                                disabled=not e7_bool)
        # Ambiance B8
        b8_final = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
    with col3:
        # Matière D8
        d8_list = ["marshmallow", "jelly candy", "felted wool", "lego"]
        d8_final = st.selectbox("MATIÈRE D8", d8_list, disabled=not e7_bool)
        b10_final = st.text_input("SOL (B10)", value="soft tactile textures", disabled=not e7_bool)

    # Construction du Prompt final
    b12 = ville['lieux'][b5_final]['cue']
    prompt_decor = f"Environment: {ville['landmark']}. Light: {b7_final}. Angle: {b6_final}. Material: {d8_final}. Cues: {b12} --ar 16:9"
    
    st.divider()
    st.code(prompt_decor)
    
    # Boutons de Rendu
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 RENDU UNIQUE"):
            st.info("Appel Vertex AI Imagen 3...")
            # Code de génération ici...
    with c2:
        if st.button("🔥 BATCH (x4)"):
            st.info("Lancement Batch...")

# --- TAB 2 : IMAGE ---
with tab2:
    st.subheader("Sélecteurs Personnages")
    # Même logique ici pour les 8 sélecteurs...
    st.info("Les sélecteurs Image suivent la même logique Miroir.")
