import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN MÉLO (LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy, white round belly, white paws."
DNA_PIPO = "Microscopic snow-potato companion, iridescent, soft glow."

# --- 2. DONNÉES DE BASE (RESTO COMPLÈTE) ---
MAT_MAP = {
    "🍭 SUCRERIES": {"jelly candy": "Translucent jelly candy", "marshmallow": "Marshmallow foam", "chocolate": "Chocolate tri-blend", "candy": "Sugar-coated candy"},
    "🧶 TEXTILES": {"felted wool": "Felted wool", "velvet": "Velvet", "crochet": "Crochet"},
    "🧩 JOUETS": {"lego": "Lego plastic ABS", "clay": "Soft clay", "toy wood": "Polished toy wood"}
}

DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower in distant soft-focus."},
        2: {"nom": "Les Quais de Seine", "cue": "River Seine reflections, distant tower."},
        3: {"nom": "Au pied de la Tour", "cue": "Metallic structure details, looking up."},
        4: {"nom": "Champ-de-Mars", "cue": "Green grass, distant silhouette."}}}
}

# --- 3. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director Studio V54", layout="wide")

# --- 4. SIDEBAR (PILOTAGE FR) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    st.success("🟢 Moteur Ultra Connecté")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Logique automatique de base
    auto_b5_idx = (p_id - 1) // 5
    auto_b6 = "wide-angle lens"
    auto_b7 = "Golden Hour"
    auto_b8 = "calm"
    
    ville = DESTINATIONS[v_id]

# --- 5. INTERFACE ET ONGLETS (FR) ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- TAB 1 : DÉCOR (LA FORMULE XLSX) ---
with tab1:
    st.write(f"### Configuration du Décor — Plan {p_id}")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # B5 & B9
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_idx, format_func=lambda x: ville['lieux'][x]['nom'], disabled=not e7_bool)
        b9_val = ville['nom']
        
        # B6 & I34 (Camera)
        i34 = st.selectbox("CAMÉRA MANUELLE (I34)", ["macro lens", "eye-level"], disabled=not e7_bool)
        b6 = st.selectbox("ANGLE AUTO (B6)", ["wide-angle lens", "ground perspective"], disabled=not e7_bool)
        cam_final = i34 if e7 == "yes" else b6

    with c2:
        # B7 & I35 (Lighting)
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Soft Moonlight", "Deep Night"], disabled=not e7_bool)
        b7 = st.selectbox("LUMIÈRE AUTO (B7)", ["Golden Hour", "Blue Hour", "Sunset"], disabled=not e7_bool)
        light_final = i35 if e7 == "yes" else b7
        
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
        b11 = st.selectbox("1er PLAN (B11)", ["", "wild flowers", "leaves", "puddles"], disabled=not e7_bool)

    with c3:
        # D8 & D9 (Materials)
        cat = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8 = st.selectbox("MATIÈRE D8", list(MAT_MAP[cat].keys()), disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", "soft tactile textures", disabled=not e7_bool)

    # --- CONSTRUCTION DU PROMPT 1 (FORMULE EXACTE) ---
    e5_name = ville['lieux'][b5_val]['nom']
    b12 = ville['lieux'][b5_val]['cue']
    
    # Logique D9
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    # Logique Candy texture
    texture_logic = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"
    # Logique B11
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
    # Logique B12
    b12_str = f"PLATE CUES (STRICT): {b12}. " if b12 != "" else ""

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_name}. "
        f"The scene is set in {b9_val} during the {light_final}, with a {b8} atmosphere. "
        f"The camera uses a {cam_final} with a low-angle ground perspective. "
        f"{b11_str}"
        f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {texture_logic}. "
        f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant, soft-focus silhouette, suggested only by blurred shapes and glowing light. "
        f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays, bedtime-friendly calm palette. "
        f"GROUND DETAIL: The ground is {b10} with high-tactile micro-textures. "
        f"{b12_str}"
        f"RULES: No characters, no people, no text, no logos, no watermarks. Pure background plate."
    )

    st.divider()
    st.subheader("📝 PROMPT 1 (Généré selon XLSX)")
    st.code(prompt_1)

# --- BOUTONS DE GÉNÉRATION ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("🚀 LANCER LE RENDU UNIQUE"):
        if init_vertex():
            with st.spinner("Nanobanana Pro calcule..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)
with col_b2:
    if st.button("🔥 BATCH PRODUCTION (x4)"):
        if init_vertex():
            with st.spinner("Série Nanobanana..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_1, number_of_images=4, aspect_ratio="16:9")
                cols = st.columns(2)
                for i, img in enumerate(batch):
                    with cols[i%2]: st.image(img._pil_image)
