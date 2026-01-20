import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN MÉLO (LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy, white round belly, white paws."
DNA_PIPO = "Microscopic snow-potato companion, iridescent, soft glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES (80 LIEUX) ---
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower recognizable. Setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Setting: Pelouse du Champ-de-Mars."}}}
}

# --- 3. AUTHENTIFICATION ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director V49", layout="wide")

# --- 5. LOGIQUE DE SYNCHRONISATION (PIVOT) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    st.success("🟢 Vertex Engine Connected")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    # Lien mathématique : Plan 1-5 -> Lieu 1, Plan 6-10 -> Lieu 2, etc.
    auto_b5 = (p_id - 1) // 5 + 1
    
    if e7_bool:
        st.info("💡 Mode Manuel : Vous avez le contrôle total.")
    else:
        st.caption(f"🤖 Mode Auto : Paramètres dictés par le Plan {p_id}")

# --- 6. ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- TAB 1 : DÉCOR ---
with tab1:
    st.subheader("Pilotage du Décor")
    
    col1, col2, col3 = st.columns(3)
    
    if e7_bool:
        with col1:
            b5_id = st.selectbox("LIEU (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
            b6 = st.selectbox("ANGLE (B6)", ["wide-angle lens", "macro lens", "ground perspective"])
            b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Blue Hour", "Sunset", "Deep Night"])
        with col2:
            b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"])
            b10 = st.text_input("SOL (B10)", "soft tactile textures")
            b11 = st.selectbox("1er PLAN (B11)", ["none", "wild flowers", "leaves", "puddles"])
        with col3:
            d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "lego"])
            d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"])
    else:
        # MODE AUTOMATIQUE : On affiche les variables sans pouvoir les changer
        b5_id = auto_b5
        b6, b7, b8, b10, b11, d8, d9 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", "none", "marshmallow", "none"
        with col1:
            st.metric("Lieu (B5)", ville['lieux'][b5_id]['nom'])
            st.metric("Angle (B6)", b6)
        with col2:
            st.metric("Lumière (B7)", b7)
            st.metric("Ambiance (B8)", b8)
        with col3:
            st.metric("Matière (D8)", d8)
            st.write(f"**Sol:** {b10}")

    b12 = ville['lieux'][b5_id]['cue']
    prompt_decor = f"Environment: {ville['landmark']}. Light: {b7}. Angle: {b6}. Material: {d8}. Cues: {b12} --ar 16:9"
    st.code(prompt_decor)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 RENDU UNIQUE", key="d1"):
            if init_vertex():
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                imgs = model.generate_images(prompt=prompt_decor, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image)
    with c2:
        if st.button("🔥 BATCH (x4)", key="d4"):
            if init_vertex():
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_decor, number_of_images=4, aspect_ratio="16:9")
                g1, g2 = st.columns(2)
                for i, img in enumerate(batch):
                    with (g1 if i%2==0 else g2): st.image(img._pil_image)

# --- TAB 2 : IMAGE ---
with tab2:
    st.subheader("Réglages Mélo & Pipo")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        s_paws = st.selectbox("Paws", ["relaxed", "walking", "sitting"])
        s_expr = st.selectbox("Expression", ["curious", "smiling", "amazed"])
    with c2:
        s_p_pose = st.selectbox("Pipo Pose", ["floating", "orbiting"])
        s_p_pos = st.selectbox("Pipo Pos", ["near head", "on shoulder"])
    with c3:
        s_acc = st.text_input("Accessoire", "Red Beret")
        s_pal = st.selectbox("Palette", ["Natural", "Pastel"])
    with c4:
        s_p_col = st.selectbox("Pipo Color", ["Iridescent", "White"])
        s_en = st.selectbox("Energy", ["Soft glow", "Sparkles"])

    prompt_image = f"Integration: MÉLO ({DNA_MELO}). PIPO ({DNA_PIPO}). Pose: {s_paws}. Expr: {s_expr}. Acc: {s_acc}. {TECH_LOCKS}"
    st.code(prompt_image)
    
    if st.button("🚀 GÉNÉRER PERSOS"):
        if init_vertex():
            model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
            imgs = model.generate_images(prompt=prompt_image, number_of_images=1, aspect_ratio="16:9")
            st.image(imgs[0]._pil_image)

# --- TAB 3 : VIDÉO ---
with tab3:
    st.subheader("Paramètres de Mouvement")
    v1, v2, v3 = st.columns(3)
    with v1: v_action = st.text_input("Mouvement", "Slow breathing")
    with v2: v_trail = st.selectbox("Énergie", ["Soft glow", "Ribbon", "None"])
    with v3: v_speed = st.selectbox("Vitesse", ["Ultra-slow", "Natural"])
    
    prompt_video = f"Animation (8s): {v_action}. Pipo: {v_trail}. Speed: {v_speed}."
    st.code(prompt_video)
