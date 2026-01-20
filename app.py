import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE MÉLO (STRICT V31) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Blue glass suit (transparent blue glass effect), ultra-glossy. Rounded child proportions. No internal anatomy."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
MATERIAL_DNA = "Homogeneous transparent blue glass/jelly, high IOR 1.5, caustics, cinematic refraction."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, Ray-traced lighting, 2026 CGI standards."

# --- 2. RESTAURATION DES LISTES V31 ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "jelly candy": "Translucent jelly candy (glossy), subsurface scattering",
        "marshmallow": "Marshmallow foam (matte soft), squishy appearance",
        "chocolate": "Chocolate tri-blend (milk, dark, white - marble effect)",
        "fondant": "Smooth sugar fondant (matte)",
        "candy cane": "Striped polished candy cane"
    },
    "🧶 TEXTILES": {
        "felted wool": "Felted wool fabric, soft fibers",
        "velvet": "Velvet microfabric, deep sheen",
        "crochet": "Hand-knitted wool crochet pattern",
        "corduroy": "Ridged corduroy fabric texture"
    },
    "🧩 JOUETS": {
        "lego": "Lego plastic ABS, high gloss",
        "clay": "Soft hand-modeled clay (matte)",
        "tin metal": "Vintage painted tin toy metal",
        "toy wood": "Polished toy wood, rounded edges"
    }
}

# --- 3. BASE DE DONNÉES LIEUX ---
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable. Setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Setting: Pelouse du Champ-de-Mars."}}}
}

# --- 4. LOGIQUE MIROIR (V31 SYNC) ---
def get_auto_data(p_id):
    b5_idx = (p_id - 1) // 5 
    angles = ["wide-angle lens", "macro lens", "ground level camera", "low-angle cinematic perspective"]
    lights = ["Golden Hour", "Blue Hour", "Cinematic Sunset", "Soft Moonlight"]
    vibes = ["calm and poetic", "mysterious", "joyful", "nostalgic"]
    return {"b5": b5_idx + 1, "b6": angles[p_id % 4], "b7": lights[p_id % 4], "b8": vibes[p_id % 4]}

# --- 5. INITIALISATION ---
st.set_page_config(page_title="Melo Legacy V53", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    e7_bool = st.toggle("🕹️ MODE MANUEL (E7)", value=False)
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    prod = get_auto_data(p_id)
    ville = DESTINATIONS[v_id]

# --- 6. INTERFACE ONGLETS (STRUCTURE V31) ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

with tab1:
    st.subheader("Pilotage du Décor (B5-B11 + D8-D9)")
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_f = st.selectbox("LIEU (B5)", [1,2,3,4], index=prod['b5']-1, format_func=lambda x: ville['lieux'][x]['nom'], disabled=not e7_bool)
        b6_list = ["wide-angle lens", "macro lens", "ground level camera", "low-angle cinematic perspective", "bird's eye view"]
        b6_f = st.selectbox("ANGLE (B6)", b6_list, index=b6_list.index(prod['b6']), disabled=not e7_bool)
    with c2:
        b7_list = ["Golden Hour", "Blue Hour", "Cinematic Sunset", "Soft Moonlight", "Deep Night"]
        b7_f = st.selectbox("LUMIÈRE (B7)", b7_list, index=b7_list.index(prod['b7']), disabled=not e7_bool)
        b8_f = st.selectbox("AMBIANCE (B8)", ["calm and poetic", "mysterious", "joyful", "nostalgic", "dramatic"], disabled=not e7_bool)
    with c3:
        cat = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8_f = st.selectbox("D8 (Principal)", list(MAT_MAP[cat].keys()), disabled=not e7_bool)
        d9_f = st.selectbox("D9 (Secondaire)", ["none", "frosted glass", "gold dust", "sugar coating"], disabled=not e7_bool)

    # STRUCTURE PROMPT DÉCOR (Héritée V31)
    b12_cue = ville['lieux'][b5_f]['cue']
    prompt_decor = f"Cinematic Environment Plate: {b12_cue}. Light: {b7_f}. Angle: {b6_f}. Vibe: {b8_f}. Materials: {MAT_MAP[cat][d8_f]} and {d9_f}. Ground: tactile textures. {TECH_LOCKS} --ar 16:9"
    st.code(prompt_decor)

with tab2:
    st.subheader("Les 8 Sélecteurs Personnages (V31)")
    ic1, ic2, ic3, ic4 = st.columns(4)
    with ic1:
        s_paws = st.selectbox("1. Paws/Pose", ["relaxed", "sitting", "walking", "dancing", "curled up"], disabled=not e7_bool)
        s_expr = st.selectbox("2. Expression", ["curious", "amazed", "smiling", "sleepy", "thoughtful"], disabled=not e7_bool)
    with ic2:
        s_ppose = st.selectbox("3. Pipo Pose", ["floating", "orbiting", "sitting", "hiding"], disabled=not e7_bool)
        s_ppos = st.selectbox("4. Pipo Position", ["near head", "on shoulder", "on paw", "behind"], disabled=not e7_bool)
    with ic3:
        s_acc = st.text_input("5. Accessoire", "Red Beret", disabled=not e7_bool)
        s_pal = st.selectbox("6. Palette", ["Natural cinematic", "Pastel tones", "Vibrant colors", "Monochrome blue"], disabled=not e7_bool)
    with ic4:
        s_pcol = st.selectbox("7. Pipo Color", ["Iridescent White", "Pure Pearl", "Golden Glow", "Soft Blue"], disabled=not e7_bool)
        s_en = st.selectbox("8. Energy Trail", ["Soft glow", "Ribbon of light", "Sparkles", "None"], disabled=not e7_bool)

    # STRUCTURE PROMPT IMAGE (Héritée V31)
    prompt_image = f"Character Study: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws}. Expression: {s_expr}. Accessory: {s_acc}. Color Palette: {s_pal}. Pipo Color: {s_pcol}. Energy: {s_en}. Material: {MATERIAL_DNA}. {TECH_LOCKS}"
    st.code(prompt_image)

with tab3:
    st.subheader("Fix Vidéo (Structure V31)")
    vc1, vc2, vc3 = st.columns(3)
    with vc1: v_act = st.selectbox("Action", ["Slow breathing", "Looking around", "Blinking", "Soft swaying"], disabled=not e7_bool)
    with vc2: v_trail = st.selectbox("Effet Énergie", ["Glow", "Ribbon", "None"], disabled=not e7_bool)
    with vc3: v_speed = st.selectbox("Vitesse", ["Ultra-slow", "Slow-mo"], disabled=not e7_bool)

    # STRUCTURE PROMPT VIDÉO (Héritée V31)
    prompt_video = f"Cinematic Animation: {v_act}. Pipo trail: {v_trail}. Speed: {v_speed}. Perfect loop. 4K 60fps cinematic feel. Ray-traced shadows."
    st.code(prompt_video)

# --- 7. BOUTONS DE GÉNÉRATION ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

st.divider()
c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    if st.button("🚀 RENDU UNIQUE"):
        if init_vertex():
            with st.spinner("Nanobanana Pro calcule..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                # On utilise ici le prompt de l'onglet actif
                target_prompt = prompt_decor if tab1 else prompt_image
                imgs = model.generate_images(prompt=target_prompt, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)

with c_btn2:
    if st.button("🔥 BATCH PRODUCTION (x4)"):
        if init_vertex():
            with st.spinner("Série Nanobanana..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_decor, number_of_images=4, aspect_ratio="16:9")
                cols = st.columns(2)
                for i, img in enumerate(batch):
                    with cols[i%2]: st.image(img._pil_image, caption=f"V{i+1}")
