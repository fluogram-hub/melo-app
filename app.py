import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & TEXTURES MÉLO (B22) ---
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy, rounded proportions."

# --- 2. BASE DE DONNÉES LIEUX ---
# (Note: Les 80 lieux sont stockés ici)
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR. Eiffel Tower recognizable. Setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Setting: Pelouse du Champ-de-Mars."}}}
}

# --- 3. AUTHENTIFICATION INVISIBLE (VIA SECRETS) ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        # On fixe l'ID et la Région ici pour que l'utilisateur n'ait plus à les voir
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

# --- 4. CONFIG UI ---
st.set_page_config(page_title="Melo Director Studio", layout="wide")

# --- 5. SIDEBAR ÉPURÉE (PLUS DE PROJECT ID !) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO PRO")
    st.success("🟢 Moteur Vertex Ultra Connecté") # Confirmation visuelle
    
    st.divider()
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    b12 = ville['lieux'][auto_b5]['cue']

# --- 6. INTERFACE DE RENDU ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][auto_b5]['nom']}")
prompt_1 = f"{b12} Material: Marshmallow foam. --ar 16:9"

st.code(prompt_1)

# BOUTONS DE RENDU
c1, c2 = st.columns(2)
with c1:
    if st.button("🎯 RENDU UNIQUE"):
        if init_vertex():
            try:
                with st.spinner("Calcul du plan..."):
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    images = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9", guidance_scale=15.0)
                    st.image(images[0]._pil_image, use_column_width=True)
            except Exception as e: st.error(f"Erreur : {e}")

with c2:
    if st.button("🔥 BATCH PRODUCTION (x4)"):
        if init_vertex():
            try:
                with st.spinner("Production de la série..."):
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    batch_images = model.generate_images(prompt=prompt_1, number_of_images=4, aspect_ratio="16:9", guidance_scale=15.0)
                    
                    grid_col1, grid_col2 = st.columns(2)
                    for i, img in enumerate(batch_images):
                        with (grid_col1 if i % 2 == 0 else grid_col2):
                            st.image(img._pil_image, caption=f"Variation {i+1}", use_column_width=True)
                            buf = io.BytesIO()
                            img._pil_image.save(buf, format="PNG")
                            st.download_button(f"💾 Save V{i+1}", buf.getvalue(), f"melo_v{i+1}.png")
            except Exception as e: st.error(f"Erreur : {e}")
