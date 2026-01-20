import streamlit as st
import io
from google import genai
from google.genai import types
from PIL import Image

# --- 1. ADN MÉLO & PIPO (B22 LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
MATERIAL_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high IOR 1.5, caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# --- 2. MATÉRIAUX (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "jelly candy": "Translucent jelly candy (glossy)",
        "marshmallow": "Marshmallow foam (matte soft)",
        "fondant": "Fondant sugar paste (matte)",
        "chocolate": "Chocolate tri-blend (white, milk, dark – soft marble)"
    },
    "🧶 TEXTILES": {"felted wool": "Felted wool fabric", "velvet": "Velvet microfabric"},
    "📜 PAPIER/BOIS": {"paper mâché": "Paper mâché (smooth)", "toy wood": "Toy wood (rounded edges)"},
    "🧩 JOUETS": {"lego": "Lego plastic ABS, high gloss", "clay": "Soft clay (matte)"}
}

# --- 3. BASE DE DONNÉES : 20 DESTINATIONS / 80 LIEUX (B9/E/F) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere. Specific setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower clearly recognizable. Specific setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower clearly recognizable. Specific setting: Pelouse du Champ-de-Mars."}}},
    "mont_st_michel": {"nom": "Le Mont Saint-Michel (France)", "landmark": "Mont Saint-Michel", "lieux": {
        1: {"nom": "La Baie", "cue": "Mont-Saint-Michel silhouette, tidal bay, ancient stone textures. Specific setting: La Baie."},
        2: {"nom": "La Porte d'Entrée", "cue": "Mont-Saint-Michel silhouette. Specific setting: La Porte d'Entrée."},
        3: {"nom": "Le Cloître", "cue": "Mont-Saint-Michel silhouette. Specific setting: Le Cloître."},
        4: {"nom": "Les Dunes", "cue": "Mont-Saint-Michel silhouette. Specific setting: Les Dunes."}}},
    # (Note : La structure supporte les 20 villes avec leurs cues respectives du XLSX)
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Studio", layout="wide")

# --- 5. INITIALISATION (FORMULE EXCEL) ---
# Valeurs par défaut (B6, B7, B8, B10, B11, I34, I35)
b6, b7, b8, b10, b11 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", ""
i34, i35 = "low-angle ground perspective", "bedtime-friendly soft light"
d8, d9 = "marshmallow", "none"
# Image vars
s_paws, s_expr, s_p_pose, s_p_pos, s_acc, s_pal, s_p_col, s_en = "relaxed", "curious", "floating", "head", "Beret", "Natural", "White", "Soft"

# --- 6. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 STUDIO GÉNÉRATION")
    api_key = st.text_input("🔑 COLLE TA CLÉ GEMINI ICI", type="password", help="Colle la clé AIza... ici")
    
    st.divider()
    e7_bool = st.toggle("🕹️ MODE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    if e7_bool:
        b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
        cat_d8 = st.selectbox("MATÉRIAU D8", list(MAT_MAP.keys()))
        d8 = st.selectbox("CHOIX D8", list(MAT_MAP[cat_d8].keys()))
        b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour"])
        b11 = st.selectbox("1er PLAN (B11)", ["", "wild flowers", "puddles", "leaves"])
    else: b5_id = auto_b5

# --- 7. CONSTRUCTION DU PROMPT 1 (FORMULE EXACTE XLSX) ---
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
b12 = ville['lieux'][b5_id]['cue']
fg_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
mat_sec = f" and {d9}" if d9 != "none" else ""
sugar = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"

prompt_1 = (
    f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
    f"The scene is set in {ville['nom']} during the {final_light}, with a {b8} atmosphere. "
    f"The camera uses a {final_angle} with a low-angle ground perspective. {fg_str}"
    f"MATERIAL WORLD & SHADING: All surfaces reimagined in {d8}{mat_sec}. "
    f"Surfaces feature realistic subsurface scattering and {sugar}. "
    f"COMPOSITION: Minimalist, clean, with large negative space. Distant soft-focus silhouette. "
    f"LIGHTING: Soft cinematic bokeh, bedtime-friendly calm palette. GROUND DETAIL: {b10}. "
    f"PLATE CUES (STRICT): {b12}. RULES: Pure background plate."
)

# --- 8. AFFICHAGE ET GÉNÉRATION ---
etape = st.radio("ÉTAPE :", ["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"], horizontal=True)

st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")
current_p = prompt_1 # Par défaut

if "IMAGE" in etape:
    current_p = f"Integration: MÉLO ({DNA_MELO}). PIPO ({DNA_PIPO}). Pose: {s_paws}. Material: {MATERIAL_DNA}. [LOCKS]: {TECH_LOCKS}."

st.subheader("Prompt Technique")
st.code(current_p)

if st.button("🚀 GÉNÉRER SUR NANOBANANA PRO"):
    if not api_key: st.error("Colle ta clé API Gemini à gauche !")
    else:
        try:
            with st.spinner("Nanobanana Pro calcule..."):
                client = genai.Client(api_key=api_key)
                resp = client.models.generate_content(
                    model="gemini-3-pro-image-preview",
                    contents=[current_p],
                    config=types.GenerateContentConfig(image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"))
                )
                for part in resp.candidates[0].content.parts:
                    if part.inline_data:
                        img = Image.open(io.BytesIO(part.inline_data.data))
                        st.image(img, use_column_width=True)
                        # Option de téléchargement
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        st.download_button("💾 Télécharger l'image", buf.getvalue(), f"melo_plan_{p_id}.png", "image/png")
        except Exception as e: st.error(f"Erreur API : {e}")
