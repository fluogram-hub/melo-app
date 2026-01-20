import streamlit as st
import os, io, urllib.parse
from google import genai
from google.genai import types
from PIL import Image

# --- 1. ADN & BIBLE B22 ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. MATÉRIAUX DÉCOR (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "Translucent jelly candy (glossy)": "Translucent jelly candy (glossy), subsurface scattering",
        "Marshmallow foam": "Marshmallow foam (matte soft), squishy appearance",
        "Fondant sugar paste": "Fondant sugar paste (matte), smooth powdery finish",
        "Chocolate tri-blend": "Chocolate tri-blend (white, milk, dark – soft marble effect)"
    },
    "🧶 TEXTILES": {"Felted wool": "Felted wool fabric", "Velvet": "Velvet microfabric"},
    "🧩 JOUETS": {"Lego ABS": "Lego plastic ABS, high gloss", "Soft clay": "Soft clay (matte)"}
}

# --- 3. BASE DE DONNÉES 20 DESTINATIONS (80 LIEUX) ---
# (Remplis avec tes données colonnes A, E, F)
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable. Specific setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower clearly recognizable. Specific setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower clearly recognizable. Specific setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower clearly recognizable. Specific setting: Pelouse du Champ-de-Mars."}}}
}

# --- 4. CONFIG UI ---
st.set_page_config(page_title="Melo Production Master", layout="wide")

# --- 5. INITIALISATION VARIABLES (ZÉRO NAMEERROR) ---
v_id, p_id = "paris", 1
mode_manuel, e7 = False, "no"
b7, b6, i34, i35 = "Golden Hour", "wide-angle lens", "low-angle ground perspective", "bedtime-friendly soft light"
d8_val, d9_val, b10, b11 = "Marshmallow foam", "none", "soft tactile textures", "none"
s_paws, s_expr, s_p_pose, s_p_pos, s_acc, s_pal, s_p_col, s_en = "relaxed", "curious", "floating", "head", "Beret", "Natural", "White", "Soft"
s_action_en = "Slow cinematic breathing"

# --- 6. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 STUDIO GÉNÉRATION")
    api_key = st.text_input("🔑 CLE API GEMINI (Nanobanana)", type="password")
    
    st.divider()
    mode_manuel = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (1-20)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    if mode_manuel:
        b5_id = st.selectbox("LIEU (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
        b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        cat_d8 = st.selectbox("CATÉGORIE D8", list(MAT_MAP.keys()))
        d8_val = MAT_MAP[cat_d8][st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()))]
    else: b5_id = auto_b5

# --- 7. CALCULS PROMPTS (FORMULE XLSX) ---
final_light = i35 if e7 == "yes" else b7
b12 = ville['lieux'][b5_id]['cue']

# Prompt 1 (Le fond de décor)
prompt_1 = (f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
            f"Scene in {ville['nom']} during {final_light}. Material: {d8_val}. "
            f"PLATE CUES (STRICT): {b12}. RULES: Pure background plate, no characters.")

# Prompt 2 (L'intégration personnage)
prompt_2 = (f"Integration: MÉLO ({DNA_MELO}). PIPO ({DNA_PIPO}). Pose: {s_paws}. "
            f"Material: {MATERIAL_MAIN_DNA}. [LOCKS]: {TECH_LOCKS}.")

# --- 8. AFFICHAGE ET GÉNÉRATION ---
etape = st.radio("ÉTAPE :", ["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"], horizontal=True)

st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")
current_p = prompt_1 if "DÉCOR" in etape else prompt_2

st.subheader("Prompt Technique")
st.code(current_p)

if st.button("🚀 GÉNÉRER AVEC NANOBANANA PRO"):
    if not api_key:
        st.warning("⚠️ Pose ta clé API à gauche pour activer Nanobanana.")
    else:
        try:
            with st.spinner("Nanobanana Pro génère ton image..."):
                client = genai.Client(api_key=api_key)
                resp = client.models.generate_content(
                    model="gemini-3-pro-image-preview",
                    contents=[current_p],
                    config=types.GenerateContentConfig(
                        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K")
                    )
                )
                # Affichage
                for part in resp.candidates[0].content.parts:
                    if part.inline_data:
                        st.image(Image.open(io.BytesIO(part.inline_data.data)), use_column_width=True)
        except Exception as e:
            st.error(f"Erreur d'accès à l'API : {e}")
