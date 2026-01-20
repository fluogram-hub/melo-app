import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE MÉLO (LOCKS) ---
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra glossy, white round belly, white paws."
DNA_PIPO = "Microscopic snow-potato companion, iridescent, soft glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera."

# --- 2. RESTAURATION DES MATÉRIAUX (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "jelly candy": "Translucent jelly candy (glossy), subsurface scattering",
        "marshmallow": "Marshmallow foam (matte soft), squishy appearance",
        "chocolate": "Chocolate tri-blend (milk, dark, white - marble effect)",
        "fondant": "Smooth sugar fondant (matte)",
        "candy cane": "Striped polished candy cane"
    },
    "🧶 TEXTILES": {
        "felted wool": "Felted wool fabric, soft fibers",
        "velvet": "Velvet microfabric, deep sheen",
        "crochet": "Hand-knitted wool crochet pattern",
        "corduroy": "Ridged corduroy fabric texture"
    },
    "🧩 JOUETS": {
        "lego": "Lego plastic ABS, high gloss",
        "clay": "Soft hand-modeled clay (matte)",
        "tin metal": "Vintage painted tin toy metal",
        "toy wood": "Polished toy wood, rounded edges"
    }
}

# --- 3. RESTAURATION DES DESTINATIONS (80 LIEUX) ---
# (Extrait représentatif, la structure permet d'en ajouter 80)
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable. Setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower recognizable. Setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower recognizable. Setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower recognizable. Setting: Pelouse du Champ-de-Mars."}}},
    "santorin": {"nom": "Santorin (Grèce)", "landmark": "Blue Domes", "lieux": {
        1: {"nom": "Ruelles d'Oia", "cue": "White-washed walls, blue domes. Setting: Oia."},
        2: {"nom": "Vue sur la Caldeira", "cue": "Volcanic bay, deep blue sea. Setting: Caldera."},
        3: {"nom": "L'Église au dôme", "cue": "Famous blue dome church. Setting: Church."},
        4: {"nom": "Terrasse au coucher", "cue": "Classic Santorini sunset view. Setting: Terrace."}}}
}

# --- 4. LOGIQUE MIROIR (AUTO vs MANUEL) ---
def get_auto_data(p_id):
    # Logique de sélection automatique basée sur le Plan ID
    b5_idx = (p_id - 1) // 5 
    angles = ["wide-angle lens", "macro-cinematography", "ground level camera", "eye-level perspective"]
    lights = ["Golden Hour", "Blue Hour", "Cinematic Sunset", "Soft Moonlight"]
    vibes = ["calm and poetic", "mysterious", "joyful", "nostalgic"]
    
    return {
        "b5": b5_idx + 1,
        "b6": angles[p_id % 4],
        "b7": lights[p_id % 4],
        "b8": vibes[p_id % 4]
    }

# --- 5. INTERFACE ---
st.set_page_config(page_title="Melo Mirror V52", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO ULTRA")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    prod = get_auto_data(p_id)
    ville = DESTINATIONS[v_id]

st.title(f"📍 {ville['nom']} — Plan {p_id}")
mode_color = "#FF4B4B" if e7_bool else "#007BFF"
mode_text = "🔴 MODE DIRECTEUR (ÉDITION)" if e7_bool else "🔵 MODE PRODUCTION (AUTO-LOCK)"
st.markdown(f'<p style="color:{mode_color}; font-weight:bold;">{mode_text}</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- TAB 1 : DÉCOR ---
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        # RÉPARATION B5 : Affiche maintenant les noms au lieu des numéros
        b5_final = st.selectbox("LIEU PRÉCIS (B5)", [1,2,3,4], 
                                index=prod['b5']-1, 
                                format_func=lambda x: ville['lieux'][x]['nom'],
                                disabled=not e7_bool)
        
        angles_list = ["wide-angle lens", "macro-cinematography", "ground level camera", "eye-level perspective", "bird's eye view"]
        b6_final = st.selectbox("ANGLE (B6)", angles_list, index=angles_list.index(prod['b6']), disabled=not e7_bool)
    
    with c2:
        lights_list = ["Golden Hour", "Blue Hour", "Cinematic Sunset", "Soft Moonlight", "Deep Night"]
        b7_final = st.selectbox("LUMIÈRE (B7)", lights_list, index=lights_list.index(prod['b7']), disabled=not e7_bool)
        
        vibes_list = ["calm and poetic", "mysterious", "joyful", "nostalgic", "dramatic"]
        b8_final = st.selectbox("AMBIANCE (B8)", vibes_list, index=vibes_list.index(prod['b8']), disabled=not e7_bool)
    
    with c3:
        # RESTAURATION MATIÈRES D8/D9
        cat = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8_final = st.selectbox("MATIÈRE PRINCIPALE (D8)", list(MAT_MAP[cat].keys()), disabled=not e7_bool)
        d9_final = st.selectbox("MATIÈRE SECONDAIRE (D9)", ["none", "frosted glass", "gold dust", "sugar coating"], disabled=not e7_bool)

    b12_cue = ville['lieux'][b5_final]['cue']
    prompt_d = f"Environment: {b12_cue}. Style: {TECH_LOCKS}. Light: {b7_final}. Angle: {b6_final}. Vibe: {b8_final}. Primary Material: {d8_final}. Secondary: {d9_final} --ar 16:9"
    st.code(prompt_d)

# --- TAB 2 : IMAGE (PERSOS) ---
with tab2:
    st.subheader("Les 8 Sélecteurs de Précision")
    ic1, ic2, ic3, ic4 = st.columns(4)
    with ic1:
        s_paws = st.selectbox("1. Paws/Pose", ["relaxed", "sitting", "walking", "dancing", "curled up"], disabled=not e7_bool)
        s_expr = st.selectbox("2. Expression", ["curious", "amazed", "smiling", "sleepy", "thoughtful"], disabled=not e7_bool)
    with ic2:
        s_ppose = st.selectbox("3. Pipo Pose", ["floating", "orbiting", "sitting", "hiding"], disabled=not e7_bool)
        s_ppos = st.selectbox("4. Pipo Position", ["near head", "on shoulder", "on paw", "behind"], disabled=not e7_bool)
    with ic3:
        s_acc = st.text_input("5. Accessoire", "Red Beret", disabled=not e7_bool)
        s_pal = st.selectbox("6. Palette", ["Natural cinematic", "Pastel tones", "Vibrant colors", "Monochrome blue"], disabled=not e7_bool)
    with ic4:
        s_pcol = st.selectbox("7. Pipo Color", ["Iridescent White", "Pure Pearl", "Golden Glow", "Soft Blue"], disabled=not e7_bool)
        s_en = st.selectbox("8. Energy Trail", ["Soft glow", "Ribbon of light", "Sparkles", "None"], disabled=not e7_bool)

    prompt_i = f"MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws}. Expression: {s_expr}. Accessory: {s_acc}. Palette: {s_pal}. Energy: {s_en}. {TECH_LOCKS}"
    st.code(prompt_i)

# --- TAB 3 : VIDÉO (MVT) ---
with tab3:
    st.subheader("Sélecteurs de Mouvement")
    vc1, vc2, vc3 = st.columns(3)
    with vc1:
        v_act = st.selectbox("Action principale", ["Slow breathing", "Looking around", "Soft floating", "Gentle swaying", "Blinking eyes"], disabled=not e7_bool)
    with vc2:
        v_trail = st.selectbox("Dynamique Énergie", ["Continuous ribbon", "Intermittent sparkles", "Static glow"], disabled=not e7_bool)
    with vc3:
        v_speed = st.selectbox("Vitesse temporelle", ["Ultra-slow (10% speed)", "Slow motion (50%)", "Real-time"], disabled=not e7_bool)

    prompt_v = f"Video Animation: {v_act}. Pipo effect: {v_trail}. Speed: {v_speed}. Loop: True. Cinematic 4k."
    st.code(prompt_v)

# --- BOUTONS DE GÉNÉRATION ---
st.divider()
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 LANCER LE RENDU UNIQUE"):
        st.info("Vertex AI Nanobanana Pro: Traitement du plan...")
with col_btn2:
    if st.button("🔥 LANCER LE BATCH PRODUCTION (x4)"):
        st.info("Vertex AI Nanobanana Pro: Traitement de la série...")
