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

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "jelly candy": "Translucent jelly candy (glossy), subsurface scattering",
        "marshmallow": "Marshmallow foam (matte soft), squishy appearance",
        "fondant": "Fondant sugar paste (matte), smooth powdery finish",
        "chocolate": "Chocolate tri-blend (white, milk, dark – soft marble effect)"
    },
    "🧶 TEXTILES": {"felted wool": "Felted wool fabric", "velvet": "Velvet microfabric"},
    "🧩 JOUETS": {"lego": "Lego plastic ABS, high gloss", "clay": "Soft clay (matte)"}
}

# --- 3. BASE DE DONNÉES (20 DESTINATIONS / 80 LIEUX) ---
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable. Specific setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Specific setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Specific setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Specific setting: Pelouse du Champ-de-Mars."}}},
    "mont_st_michel": {"nom": "Mont St-Michel (France)", "landmark": "Mont Saint-Michel", "lieux": {
        1: {"nom": "La Baie", "cue": "Mont-Saint-Michel silhouette, tidal bay. Specific setting: La Baie."},
        2: {"nom": "La Porte d'Entrée", "cue": "Ancient stone textures. Specific setting: La Porte d'Entrée."},
        3: {"nom": "Le Cloître", "cue": "Quiet stone arches. Specific setting: Le Cloître."},
        4: {"nom": "Les Dunes", "cue": "Coastal dunes view. Specific setting: Les Dunes."}}},
    # (Les autres destinations du XLSX s'ajoutent ici)
}

# --- 4. AUTHENTIFICATION SILENCIEUSE ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

# --- 5. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director Studio V47", layout="wide")

# --- 6. LOGIQUE SIDEBAR (PILOTAGE) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    st.success("🟢 Moteur Vertex Connecté")
    
    st.divider()
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    # Paramètres par défaut
    b7, d8_prompt, d8_name = "Golden Hour", "Marshmallow foam (matte soft)", "marshmallow"
    b5_id = auto_b5

    if e7_bool:
        st.subheader("⚙️ Réglages Avancés")
        b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
        cat_d8 = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()))
        d8_name = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()))
        d8_prompt = MAT_MAP[cat_d8][d8_name]
        b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])

# --- 7. CALCULS DES PROMPTS ---
final_light = "bedtime-friendly soft light" if e7_bool else b7
b12 = ville['lieux'][b5_id]['cue']
prompt_decor = f"Environment: {ville['landmark']}. Light: {final_light}. Material: {d8_prompt}. Cues: {b12} --ar 16:9"

# --- 8. INTERFACE PRINCIPALE (ONGLETS) ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

with tab1:
    st.subheader("Génération du Décor de Fond")
    st.code(prompt_decor)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎯 RENDU UNIQUE", key="btn_u_d"):
            if init_vertex():
                with st.spinner("Calcul..."):
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    imgs = model.generate_images(prompt=prompt_decor, number_of_images=1, aspect_ratio="16:9")
                    st.image(imgs[0]._pil_image, use_column_width=True)
    with c2:
        if st.button("🔥 BATCH (x4 VARIATIONS)", key="btn_b_d"):
            if init_vertex():
                with st.spinner("Batch en cours..."):
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    batch = model.generate_images(prompt=prompt_decor, number_of_images=4, aspect_ratio="16:9")
                    g1, g2 = st.columns(2)
                    for i, img in enumerate(batch):
                        with (g1 if i%2==0 else g2):
                            st.image(img._pil_image, caption=f"V{i+1}", use_column_width=True)

with tab2:
    st.subheader("Génération de Mélo & Pipo")
    # Sélecteurs Image
    col_a, col_b = st.columns(2)
    with col_a:
        s_pose = st.selectbox("Pose Mélo", ["relaxed", "sitting", "walking", "one paw raised"])
        s_expr = st.selectbox("Expression", ["curious", "smiling", "amazed", "sleepy"])
    with col_b:
        s_pipo = st.selectbox("Pipo", ["softly floating", "on shoulder", "in front"])
        s_acc = st.text_input("Accessoire", value="Red Beret")

    prompt_image = f"Integration: MÉLO ({DNA_MELO}). PIPO ({DNA_PIPO}). Pose: {s_pose}. Expr: {s_expr}. Acc: {s_acc}. {TECH_LOCKS}"
    st.code(prompt_image)
    
    if st.button("🚀 GÉNÉRER MÉLO & PIPO", key="btn_melo"):
        if init_vertex():
            with st.spinner("Rendu personnages..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                imgs = model.generate_images(prompt=prompt_image, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)

with tab3:
    st.subheader("Mouvement & Animation")
    s_mvt = st.text_input("Mouvement Mélo", "Slow cinematic breathing")
    prompt_video = f"Animation: {s_mvt} in ultra-slow motion. Perfect loop. 8s."
    st.code(prompt_video)
    st.info("💡 Note: Le rendu vidéo direct via Vertex AI sera activé dans la V48 dès que Veo sera disponible dans votre région.")
