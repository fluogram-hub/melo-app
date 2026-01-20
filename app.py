import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE MÉLO (B22 LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
MATERIAL_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high IOR 1.5, caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# --- 2. MATÉRIAUX (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "jelly candy": "Translucent jelly candy (glossy), subsurface scattering",
        "marshmallow": "Marshmallow foam (matte soft), squishy appearance",
        "fondant": "Fondant sugar paste (matte)",
        "chocolate": "Chocolate tri-blend (milk, dark, white - marble effect)"
    },
    "🧶 TEXTILES": {"felted wool": "Felted wool fabric", "velvet": "Velvet microfabric"},
    "📜 PAPIER/BOIS": {"paper mâché": "Paper mâché (smooth)", "toy wood": "Toy wood (rounded edges)"},
    "🧩 JOUETS": {"lego": "Lego plastic ABS, high gloss", "clay": "Soft clay (matte)"}
}

# --- 3. BASE DE DONNÉES LIEUX ---
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable. Setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Setting: Pelouse du Champ-de-Mars."}}}
}

# --- 4. AUTHENTIFICATION ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

# --- 5. INITIALISATION PAR DÉFAUT (ANTI-ERREUR) ---
b6, b7, b8, b10, b11 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", "none"
d8_p, d9_p = "Marshmallow foam (matte soft)", "none"
s_paws, s_expr, s_p_pose, s_p_pos, s_acc, s_pal, s_p_col, s_en = "relaxed", "curious", "floating", "head", "Beret", "Natural", "White", "Soft"
v_action, v_trail, v_speed = "Slow breathing", "Soft glow", "Ultra-slow"

# --- 6. CONFIG UI ---
st.set_page_config(page_title="Melo Director Studio V48", layout="wide")

# --- 7. SIDEBAR (NAVIGATION) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    st.success("🟢 Moteur Vertex Connecté")
    e7_bool = st.toggle("🕹️ MODE MANUEL (E7)", value=False)
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    b5_id = auto_b5

# --- 8. ONGLETS ET SÉLECTEURS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

with tab1:
    st.subheader("Réglages du Décor (B6-B11 + D8-D9)")
    c1, c2, c3 = st.columns(3)
    if e7_bool:
        with c1:
            b5_id = st.selectbox("LIEU (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
            b6 = st.selectbox("ANGLE (B6)", ["wide-angle lens", "macro lens", "eye-level"])
            b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Blue Hour", "Sunset"])
        with c2:
            b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"])
            b10 = st.text_input("SOL (B10)", "soft tactile textures")
            b11 = st.selectbox("1er PLAN (B11)", ["none", "wild flowers", "leaves", "puddles"])
        with c3:
            cat = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()))
            d8_name = st.selectbox("D8 (Principal)", list(MAT_MAP[cat].keys()))
            d8_p = MAT_MAP[cat][d8_name]
            d9_p = st.selectbox("D9 (Secondaire)", ["none", "frosted glass", "gold dust"])
    
    final_light = "bedtime-friendly soft light" if e7_bool else b7
    b12 = ville['lieux'][b5_id]['cue']
    prompt_decor = f"Environment: {ville['landmark']}. Light: {final_light}. Angle: {b6}. Vibe: {b8}. Material: {d8_p} and {d9_p}. Ground: {b10}. Foreground: {b11}. Cues: {b12} --ar 16:9"
    st.code(prompt_decor)
    
    if st.button("🚀 GÉNÉRER DÉCOR"):
        if init_vertex():
            with st.spinner("Rendu..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                imgs = model.generate_images(prompt=prompt_decor, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)

with tab2:
    st.subheader("Réglages Mélo & Pipo (Les 8 sélecteurs)")
    c1, c2 = st.columns(2)
    with c1:
        s_paws = st.selectbox("1. Paws/Pose", ["relaxed", "sitting", "walking", "one paw raised"])
        s_expr = st.selectbox("2. Expression", ["curious", "amazed", "smiling", "sleepy"])
        s_p_pose = st.selectbox("3. Pipo Pose", ["floating", "orbiting", "static"])
        s_p_pos = st.selectbox("4. Pipo Position", ["near head", "on shoulder", "in front"])
    with c2:
        s_acc = st.text_input("5. Accessoire", "Red Beret")
        s_pal = st.selectbox("6. Palette", ["Natural cinematic", "Pastel tones", "Vibrant"])
        s_p_col = st.selectbox("7. Pipo Color", ["Iridescent White", "Pure Pearl"])
        s_en = st.selectbox("8. Energy Trail", ["Soft glow", "Ribbon of light", "Sparkles"])

    prompt_image = f"Integration: MÉLO ({DNA_MELO}). PIPO ({DNA_PIPO}). Pose: {s_paws}. Expr: {s_expr}. Acc: {s_acc}. Palette: {s_pal}. Pipo Color: {s_p_col}. Trail: {s_en}. Material: {MATERIAL_DNA}. {TECH_LOCKS}"
    st.code(prompt_image)
    
    if st.button("🚀 GÉNÉRER PERSONNAGES"):
        if init_vertex():
            with st.spinner("Rendu personnages..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                imgs = model.generate_images(prompt=prompt_image, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)

with tab3:
    st.subheader("Réglages Vidéo (Mouvement)")
    c1, c2 = st.columns(2)
    with c1:
        v_action = st.text_input("Action Mélo", "Slow cinematic breathing")
        v_trail = st.selectbox("Énergie Pipo", ["Soft glow", "Long ribbon", "None"])
    with c2:
        v_speed = st.selectbox("Vitesse", ["Ultra-slow", "Natural", "Fast motion"])
    
    prompt_video = f"Animation (8s): {v_action}. Pipo energy: {v_trail}. Speed: {v_speed}. Perfect loop. cinematic 4k."
    st.code(prompt_video)
