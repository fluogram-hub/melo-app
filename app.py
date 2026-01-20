import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & CONFIGURATION ---
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy, white round belly, white paws."
DNA_PIPO = "Microscopic snow-potato companion, iridescent, soft glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

st.set_page_config(page_title="Melo Mirror Studio V51", layout="wide")

# Style CSS pour l'identité visuelle des modes
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] { border: 1px solid #007BFF; }
    .auto-label { color: #007BFF; font-weight: bold; font-size: 0.9em; margin-bottom: -10px; }
    .manual-label { color: #FF4B4B; font-weight: bold; font-size: 0.9em; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE DE CALCUL DES DONNÉES AUTOMATIQUES (PROD) ---
def get_prod_settings(p_id):
    # DÉCOR
    b5_idx = (p_id - 1) // 5
    b7_list = ["Golden Hour", "Blue Hour", "Sunset", "Deep Night"]
    b7_val = b7_list[p_id % 4]
    # IMAGE
    paws_list = ["relaxed", "sitting", "walking", "one paw raised"]
    expr_list = ["curious", "amazed", "smiling", "sleepy"]
    paws_val = paws_list[p_id % 4]
    expr_val = expr_list[p_id % 4]
    # VIDÉO
    act_list = ["Slow breathing", "Looking around", "Soft floating", "Gentle swaying"]
    act_val = act_list[p_id % 4]
    
    return {
        "b5": b5_idx, "b7": b7_val,
        "paws": paws_val, "expr": expr_val,
        "action": act_val
    }

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    st.success("🟢 Vertex Engine Connected")
    e7_bool = st.toggle("🕹️ ACTIVER CONTRÔLE MANUEL (E7)", value=False)
    
    st.divider()
    # On imagine ici les 20 destinations (Paris, Santorin, etc.)
    DESTINATIONS = {"paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {1:{"nom":"Trocadéro","cue":"..."}, 2:{"nom":"Seine","cue":"..."}, 3:{"nom":"Tour","cue":"..."}, 4:{"nom":"Champ-de-Mars","cue":"..."}}}}
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    prod = get_prod_settings(p_id)
    ville = DESTINATIONS[v_id]

# --- 4. AUTHENTIFICATION ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

# --- 5. INTERFACE PRINCIPALE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")
mode_tag = '<p class="manual-label">🔴 MODE MANUEL (ÉDITION LIBRE)</p>' if e7_bool else '<p class="auto-label">🔵 MODE AUTO (CONTRÔLE PROD)</p>'
st.markdown(mode_tag, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- TAB 1 : DÉCOR ---
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_f = st.selectbox("LIEU (B5)", [1,2,3,4], index=prod['b5'], disabled=not e7_bool)
        b6_f = st.selectbox("ANGLE (B6)", ["wide-angle lens", "macro", "ground"], disabled=not e7_bool)
    with c2:
        b7_list = ["Golden Hour", "Blue Hour", "Sunset", "Deep Night"]
        b7_f = st.selectbox("LUMIÈRE (B7)", b7_list, index=b7_list.index(prod['b7']), disabled=not e7_bool)
        b8_f = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious"], disabled=not e7_bool)
    with c3:
        d8_f = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool"], disabled=not e7_bool)
        b10_f = st.text_input("SOL (B10)", "soft tactile textures", disabled=not e7_bool)

    prompt_d = f"Environment: {ville['nom']}. Light: {b7_f}. Angle: {b6_f}. Material: {d8_f}. Ground: {b10_f} --ar 16:9"
    st.code(prompt_d)
    if st.button("🚀 RENDU DÉCOR"):
        st.info("Vertex AI: Génération Imagen 3 en cours...")

# --- TAB 2 : IMAGE ---
with tab2:
    st.subheader("Les 8 Sélecteurs de Personnages")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        p_list = ["relaxed", "sitting", "walking", "one paw raised"]
        s_paws = st.selectbox("1. Paws/Pose", p_list, index=p_list.index(prod['paws']), disabled=not e7_bool)
        e_list = ["curious", "amazed", "smiling", "sleepy"]
        s_expr = st.selectbox("2. Expression", e_list, index=e_list.index(prod['expr']), disabled=not e7_bool)
    with c2:
        s_ppose = st.selectbox("3. Pipo Pose", ["floating", "orbiting"], disabled=not e7_bool)
        s_ppos = st.selectbox("4. Pipo Position", ["near head", "on shoulder"], disabled=not e7_bool)
    with c3:
        s_acc = st.text_input("5. Accessoire", "Red Beret", disabled=not e7_bool)
        s_pal = st.selectbox("6. Palette", ["Natural", "Pastel"], disabled=not e7_bool)
    with c4:
        s_pcol = st.selectbox("7. Pipo Color", ["Iridescent White", "Pure Pearl"], disabled=not e7_bool)
        s_en = st.selectbox("8. Energy Trail", ["Soft glow", "Ribbon"], disabled=not e7_bool)

    prompt_i = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws}. Expr: {s_expr}. Acc: {s_acc}. Trail: {s_en}. {TECH_LOCKS}"
    st.code(prompt_i)
    if st.button("🚀 RENDU MÉLO & PIPO"):
        st.info("Vertex AI: Intégration Personnages...")

# --- TAB 3 : VIDÉO ---
with tab3:
    st.subheader("Paramètres de Mouvement")
    v1, v2, v3 = st.columns(3)
    with v1:
        act_list = ["Slow breathing", "Looking around", "Soft floating", "Gentle swaying"]
        v_act = st.selectbox("Mouvement", act_list, index=act_list.index(prod['action']), disabled=not e7_bool)
    with v2:
        v_trail = st.selectbox("Énergie Pipo", ["Soft glow", "Long ribbon", "None"], disabled=not e7_bool)
    with v3:
        v_speed = st.selectbox("Vitesse", ["Ultra-slow", "Natural"], disabled=not e7_bool)
    
    prompt_v = f"Animation (8s): {v_act}. Pipo energy: {v_trail}. Speed: {v_speed}. Perfect loop."
    st.code(prompt_v)
