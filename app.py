import streamlit as st
import io

# --- SÉCURITÉ INSTALLATION ---
try:
    from google.cloud import aiplatform
    from vertexai.preview.vision_models import ImageGenerationModel
    VERTEX_READY = True
except ImportError:
    VERTEX_READY = False

# --- 1. ADN MÉLO & MATÉRIAUX ---
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy."
MAT_LIST = ["Translucent jelly candy", "Marshmallow foam", "Lego plastic ABS", "Toy wood"]

# --- 2. BASE DE DONNÉES (EXTRAIT) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR. Eiffel Tower recognizable. Setting: Le Trocadéro."}}}
}

# --- 3. UI ---
st.set_page_config(page_title="Melo Director V44", layout="wide")

if not VERTEX_READY:
    st.error("❌ ERREUR : Les bibliothèques Google Cloud ne sont pas installées.")
    st.info("👉 Vérifie que ton fichier 'requirements.txt' contient bien 'google-cloud-aiplatform' et redémarre l'app.")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎬 MOTEUR VERTEX AI")
    project_id = st.text_input("PROJECT ID", placeholder="melo-prompt-gen-XXXXXX")
    location = st.selectbox("REGION", ["us-central1", "europe-west1"])
    st.divider()
    p_id = st.select_slider("PLAN", options=list(range(1, 21)))
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])

# --- 5. LOGIQUE ---
ville = DESTINATIONS[v_id]
auto_b5 = (p_id - 1) // 5 + 1
b12 = ville['lieux'][auto_b5]['cue']
prompt_1 = f"{b12} Material: Marshmallow foam. --ar 16:9"

st.title(f"📍 {ville['nom']} — {ville['lieux'][auto_b5]['nom']}")
st.code(prompt_1)

# --- 6. RENDU ---
if st.button("🚀 RENDU NANOBANANA PRO"):
    if not project_id:
        st.warning("⚠️ Entre ton Project ID à gauche.")
    else:
        try:
            with st.spinner("Vertex AI (Imagen 3) prépare le rendu..."):
                from PIL import Image
                aiplatform.init(project=project_id, location=location)
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                
                images = model.generate_images(
                    prompt=prompt_1,
                    number_of_images=1,
                    aspect_ratio="16:9",
                    guidance_scale=15.0
                )
                
                if images:
                    st.image(images[0]._pil_image, use_column_width=True)
        except Exception as e:
            st.error(f"Erreur : {e}")
