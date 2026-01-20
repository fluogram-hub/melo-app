import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image

# --- 1. ADN & BIBLE B22 (LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES (80 LIEUX) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable. Specific setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower clearly recognizable. Specific setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower clearly recognizable. Specific setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower clearly recognizable. Specific setting: Pelouse du Champ-de-Mars."}}},
    # ... (Ajoute les autres destinations ici)
}

# --- 3. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production - Vertex Engine", layout="wide")

# --- 4. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 MOTEUR VERTEX AI")
    project_id = st.text_input("PROJECT ID", placeholder="ex: melo-prompt-gen-123456")
    location = st.selectbox("REGION", ["us-central1", "europe-west1"])
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (Scénario)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1

# --- 5. CALCULS ---
b12 = ville['lieux'][auto_b5]['cue']
prompt_1 = f"{b12} Material: Marshmallow foam (matte soft). --ar 16:9"

# --- 6. ZONE DE RENDU ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][auto_b5]['nom']}")
st.subheader("Prompt Technique (Calculé)")
st.code(prompt_1)

if st.button("🚀 RENDU NANOBANANA PRO (VERTEX)"):
    if not project_id:
        st.error("⚠️ Veuillez entrer votre Project ID dans la barre latérale.")
    else:
        try:
            with st.spinner("Nanobanana Pro (Imagen 3) traite votre plan..."):
                aiplatform.init(project=project_id, location=location)
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                
                # Génération
                images = model.generate_images(
                    prompt=prompt_1,
                    number_of_images=1,
                    aspect_ratio="16:9",
                    guidance_scale=15.0 # Pour un respect strict du prompt
                )
                
                if images:
                    st.image(images[0]._pil_image, caption=f"Rendu Plan {p_id}", use_column_width=True)
                    # Sauvegarde
                    buf = io.BytesIO()
                    images[0]._pil_image.save(buf, format="PNG")
                    st.download_button("💾 Télécharger l'image", buf.getvalue(), f"melo_plan_{p_id}.png", "image/png")

        except Exception as e:
            st.error(f"Erreur technique : {e}")
            st.info("💡 Assurez-vous d'avoir cliqué sur 'Activer les API' dans la console Google Cloud.")
