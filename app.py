import streamlit as st
import os, io, urllib.parse
from google import genai
from google.genai import types
from PIL import Image

# --- 1. ADN & BIBLE B22 ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). White with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. MATÉRIAUX DÉCOR CLASSÉS (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "Translucent jelly candy (glossy)": "Translucent jelly candy (glossy), subsurface scattering",
        "Marshmallow foam": "Marshmallow foam (matte soft), squishy appearance",
        "Fondant sugar paste": "Fondant sugar paste (matte), smooth powdery finish",
        "Chocolate tri-blend": "Chocolate tri-blend (white, milk, dark – soft marble effect)"
    },
    "🧶 TEXTILES": {
        "Felted wool fabric": "Felted wool fabric, organic soft fibers",
        "Cotton quilted padding": "Cotton quilted padding, soft cushions",
        "Velvet microfabric": "Velvet microfabric, light-absorbing soft pile"
    },
    "🧩 JOUETS & ARGILE": {
        "Soft clay (matte)": "Soft clay (matte), hand-molded look",
        "Lego plastic ABS": "Lego plastic ABS, high gloss, modular brick surface"
    }
}

# --- 3. BASE DE DONNÉES 20 DESTINATIONS (EXTRAIT COMPLET B9/E/F) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable. Specific setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower clearly recognizable. Specific setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower clearly recognizable. Specific setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower clearly recognizable. Specific setting: Pelouse du Champ-de-Mars."}}},
    "neuschwanstein": {"nom": "Château de Neuschwanstein (Allemagne)", "landmark": "Fairytale castle", "lieux": {
        1: {"nom": "Le Pont Marie", "cue": "Fairytale castle silhouette, Bavarian alpine forest, soft snow or mist. Specific setting: Le Pont Marie."},
        2: {"nom": "Le Chemin de Forêt", "cue": "Fairytale castle silhouette, Bavarian alpine forest, soft snow or mist. Specific setting: Le Chemin de Forêt."},
        3: {"nom": "La Cour du Château", "cue": "Fairytale castle silhouette, Bavarian alpine forest. Specific setting: La Cour du Château."},
        4: {"nom": "Le Balcon", "cue": "Fairytale castle silhouette, Bavarian alpine forest. Specific setting: Le Balcon."}}},
    # Ajoute les autres ici sur le même modèle...
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director Studio V33", layout="wide")

# Initialisation des variables pour éviter les NameError
if 'api_key' not in st.session_state: st.session_state.api_key = ""

# --- 5. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    st.session_state.api_key = st.text_input("CLE API GEMINI", value=st.session_state.api_key, type="password")
    
    mode_manuel = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (1-20)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    # Defaults
    b7, b6, i34, i35 = "Golden Hour", "wide-angle lens", "low-angle ground perspective", "bedtime-friendly soft light"
    d8_val, d9_val, b10, b11 = "Marshmallow foam", "none", "soft tactile textures", "none"
    s_paws, s_expr, s_p_pose, s_p_pos, s_acc, s_pal, s_p_col, s_en = "relaxed", "curious", "floating", "head", "Beret", "Natural", "White", "Soft"
    s_action_en = "Slow cinematic breathing"

    if mode_manuel:
        st.divider()
        # Sélecteurs dynamiques selon l'étape...
        b5_id = st.selectbox("LIEU (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
        b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        cat_d8 = st.selectbox("CATÉGORIE D8", list(MAT_MAP.keys()))
        d8_ui = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()))
        d8_val = MAT_MAP[cat_d8][d8_ui]
    else: b5_id = auto_b5

# --- 6. CALCULS PROMPTS ---
final_light = i35 if e7 == "yes" else b7
b12 = ville['lieux'][b5_id]['cue']
prompt_1 = f"Environment: {ville['landmark']}. Light: {final_light}. Material: {d8_val}. Ground: {b10}. Cues: {b12}."
prompt_2 = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws}. {TECH_LOCKS}."
prompt_3 = f"Animation: {s_action_en} in ultra-slow motion. Pipo trail: {s_en}. Perfect loop."

# --- 7. AFFICHAGE ---
etape = st.radio("ÉTAPE :", ["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"], horizontal=True)

st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")
current_p = prompt_1 if "DÉCOR" in etape else (prompt_2 if "IMAGE" in etape else prompt_3)

st.code(current_p)

if st.button("🚀 GÉNÉRER AVEC NANOBANANA PRO"):
    if not st.session_state.api_key:
        st.error("Entre ta clé API Gemini à gauche !")
    else:
        try:
            client = genai.Client(api_key=st.session_state.api_key)
            resp = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[current_p],
                config=types.GenerateContentConfig(image_config=types.ImageConfig(aspect_ratio="16:9"))
            )
            for part in resp.candidates[0].content.parts:
                if part.inline_data:
                    st.image(Image.open(io.BytesIO(part.inline_data.data)))
        except Exception as e:
            st.error(f"Erreur API : {e}")
