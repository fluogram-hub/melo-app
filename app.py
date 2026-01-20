import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# 1. ADN & VERROUS TECHNIQUES (B22)
# =========================================================
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy, white round belly. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; iridescent, tiny scale. Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# =========================================================
# 2. BASE DE DONNÉES : DÉCORS (STRUCTURE DYNAMIQUE)
# =========================================================
DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)", 
        "landmark_en": "Eiffel Tower",
        "decors": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Eiffel Tower, Paris atmosphere, warm streetlamps bokeh. Specific setting: Le Trocadéro."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine banks", "cue": "Eiffel Tower silhouette, river reflections. Specific setting: Les Quais de Seine."},
            3: {"fr": "Au pied de la Tour", "en": "The foot of the Tower", "cue": "Industrial metallic structure, looking up. Specific setting: Au pied de la Tour."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ-de-Mars Lawn", "cue": "Large grass area, distant tower silhouette. Specific setting: Pelouse du Champ-de-Mars."}
        }
    },
    "mont_saint_michel": {
        "nom_fr": "Le Mont Saint-Michel (France)",
        "landmark_en": "Mont-Saint-Michel",
        "decors": {
            1: {"fr": "La Baie", "en": "The Bay", "cue": "Silhouette of Mont-Saint-Michel, tidal bay. Specific setting: La Baie."},
            2: {"fr": "La Porte d'Entrée", "en": "The Entrance Gate", "cue": "Ancient stone texture. Specific setting: La Porte d'Entrée."},
            3: {"fr": "Le Cloître", "en": "The Cloister", "cue": "Arches and mist. Specific setting: Le Cloître."},
            4: {"fr": "Les Dunes", "en": "The Dunes", "cue": "Sand and grass, distant abbey. Specific setting: Les Dunes."}
        }
    }
}

PLANS_DB = {
    1: {"Angle": "wide-angle lens", "Light": "Golden Hour", "AM": "Arrival", "AP": "Floating"},
}

# =========================================================
# 3. LOGIQUE SIDEBAR
# =========================================================
st.set_page_config(page_title="Melo Cockpit V65", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ MODE MANUEL (E7)", value=False)
    
    st.divider()
    # Sélection de la ville
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    # Sélection du plan
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DB_DECORS[v_id]
    plan = PLANS_DB.get(p_id, PLANS_DB[1])
    
    # Calcul dynamique de l'ID du décor (1, 2, 3 ou 4)
    # On s'assure que si le décor n'existe pas, on reste sur le 1
    auto_b5_id = ((p_id - 1) % 4) + 1
    if auto_b5_id not in ville['decors']:
        auto_b5_id = 1

# =========================================================
# 4. INTERFACE COCKPIT
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

with tab1:
    st.subheader("⚙️ Pilotage du Décor")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # CORRECTION : On utilise list(ville['decors'].keys()) pour éviter le KeyError
        # Si la ville n'a que 2 décors, le menu n'en affichera que 2.
        b5_options = list(ville['decors'].keys())
        
        # On s'assure que l'index par défaut est valide
        default_idx = b5_options.index(auto_b5_id) if auto_b5_id in b5_options else 0
        
        b5_val = st.selectbox(
            "LIEU PRÉCIS (E5)", 
            options=b5_options, 
            index=default_idx, 
            format_func=lambda x: ville['decors'][x]['fr'], 
            disabled=not e7_bool
        )
        
        cam_final = st.selectbox("ANGLE (B6)", ["wide-angle lens", "macro lens", "eye-level"], disabled=not e7_bool)

    with c2:
        light_final = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Deep Night"], disabled=not e7_bool)
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious"], disabled=not e7_bool)
        b11 = st.selectbox("1ER PLAN (B11)", ["none", "flowers"], disabled=not e7_bool)

    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", ["Marshmallow foam", "Jelly candy"], disabled=not e7_bool)
        d9 = st.selectbox("MATÉRIEL D9", ["none", "frosted glass"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", value="dry", disabled=not e7_bool)

    # --- FORMULE PROMPT 1 (XLSX) ---
    e5_en = ville['decors'][b5_val]['en']
    b12_cue = ville['decors'][b5_val]['cue']
    
    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"Scene in {ville['nom_fr']} during {light_final}. "
        f"Material: {d8_val}. Cues: {b12_cue}. Pure background plate."
    )
    
    st.info("📝 PROMPT DÉCOR :")
    st.code(prompt_1)

# =========================================================
# 5. MOTEUR DE RENDU
# =========================================================
if st.button("🚀 RENDU UNIQUE"):
    st.success("Appel Vertex AI Imagen 3...")
    # Le code render_melo(prompt_1) viendra ici
