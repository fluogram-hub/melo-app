import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. BASE DE DONNÉES COMPLÈTE (EXTRAIT DES 80 LIEUX) ---
# J'ai structuré les données pour qu'elles correspondent exactement à tes colonnes XLSX
DECORS_DB = {
    "eiffel_paris": {
        "lieu_fr": "La Tour Eiffel (Paris, France)",
        "continent": "Europe",
        "decors": {
            1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro. Keep framing stable, no characters, no animals, no text."},
            2: {"nom": "Les Quais de Seine", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine. Keep framing stable, no characters, no animals, no text."},
            3: {"nom": "Au pied de la Tour", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tour. Keep framing stable, no characters, no animals, no text."},
            4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars. Keep framing stable, no characters, no animals, no text."}
        }
    },
    "mont_saint_michel": {
        "lieu_fr": "Le Mont Saint-Michel (France)",
        "continent": "Europe",
        "decors": {
            1: {"nom": "La Baie", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Baie."},
            2: {"nom": "La Porte d'Entrée", "cue": "Ancient stone textures, soft mist. Specific setting: La Porte d'Entrée."},
            3: {"nom": "Le Cloître", "cue": "Ancient stone textures, soft mist. Specific setting: Le Cloître."},
            4: {"nom": "Les Dunes", "cue": "Ancient stone textures, soft mist. Specific setting: Les Dunes."}
        }
    },
    "santorini_greece": {
        "lieu_fr": "Santorin (Grèce)",
        "continent": "Europe",
        "decors": {
            1: {"nom": "La Vue Haute", "cue": "Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Vue Haute."},
            2: {"nom": "La Ruelle Blanche", "cue": "Santorini whitewashed architecture, blue domes. Specific setting: La Ruelle Blanche."},
            3: {"nom": "La Terrasse", "cue": "Santorini whitewashed architecture, blue domes. Specific setting: La Terrasse."},
            4: {"nom": "Le Muret", "cue": "Santorini whitewashed architecture, blue domes. Specific setting: Le Muret."}
        }
    },
    "venice_italy": {
        "lieu_fr": "Venise (Italie)",
        "continent": "Europe",
        "decors": {
            1: {"nom": "Le Grand Canal", "cue": "Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: Le Grand Canal."},
            2: {"nom": "La Petite Ruelle", "cue": "Venice canals, historic facades. Specific setting: La Petite Ruelle."},
            3: {"nom": "La Place Saint-Marc", "cue": "Venice canals, historic facades. Specific setting: La Place Saint-Marc."},
            4: {"nom": "L'Intérieur de la Gondole", "cue": "Venice canals, historic facades. Specific setting: L'Intérieur de la Gondole."}
        }
    }
    # Note: On peut ajouter les 16 autres destinations ici sur le même modèle
}

# --- 2. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Studio V56", layout="wide")

# --- 3. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    # Choix Destination (B9)
    v_key = st.selectbox("DESTINATION (B9)", list(DECORS_DB.keys()), 
                         format_func=lambda x: DECORS_DB[x]['lieu_fr'])
    lieu_data = DECORS_DB[v_key]
    
    # Choix Plan
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    auto_b5_id = ((p_id - 1) % 4) + 1

# --- 4. INTERFACE ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

with tab1:
    st.write(f"### Configuration du Décor — {lieu_data['lieu_fr']}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        # E5 (Nom du décor précis)
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_id-1, 
                              format_func=lambda x: lieu_data['decors'][x]['nom'], disabled=not e7_bool)
        # B6 & I34
        b6 = "wide-angle lens"
        i34 = st.selectbox("ANGLE MANUEL (I34)", ["macro lens", "ground perspective", "eye-level"], disabled=not e7_bool)
        cam_final = i34 if e7 == "yes" else b6

    with c2:
        # B7 & I35
        b7 = "dusk_to_night"
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Golden Hour", "Blue Hour", "Deep Night"], disabled=not e7_bool)
        light_final = i35 if e7 == "yes" else b7
        
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
        b11 = st.selectbox("1er PLAN (B11)", ["none", "wild flowers", "leaves", "puddles"], disabled=not e7_bool)

    with c3:
        # D8 & D9
        d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "candy"], disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", "dry", disabled=not e7_bool)

    # --- FORMULE PROMPT 1 (STRICTE XLSX) ---
    e5_name = lieu_data['decors'][b5_val]['nom']
    b9_val = lieu_data['lieu_fr']
    b12_cue = lieu_data['decors'][b5_val]['cue']
    
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if (b11 != "" and b11 != "none") else ""
    texture_logic = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"

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
        f"PLATE CUES (STRICT): {b12_cue}. "
        f"RULES: No characters, no people, no text, no logos, no watermarks. Pure background plate."
    )

    st.divider()
    st.subheader("📝 PROMPT 1 (Généré selon XLSX)")
    st.code(prompt_1)

# --- 5. LOGIQUE DE GÉNÉRATION VERTEX ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

if st.button("🚀 RENDU UNIQUE"):
    if init_vertex():
        with st.spinner("Nanobanana Pro calcule..."):
            model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
            imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
            st.image(imgs[0]._pil_image, use_column_width=True)
