import streamlit as st

# --- 1. ADN & BIBLE B22 (LOCKS STRICTS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX DÉCOR (D8 / D9) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "Translucent jelly candy (glossy)": "Translucent jelly candy (glossy), subsurface scattering",
        "Translucent colored jelly": "Translucent colored jelly candy (glossy), vibrant syrup tones",
        "Hard candy (polished)": "Hard candy (polished smooth), light refraction",
        "Marshmallow foam": "Marshmallow foam (matte soft), squishy appearance",
        "Fondant sugar paste": "Fondant sugar paste (matte), smooth powdery finish",
        "Honey wax": "Honey wax (warm glow), semi-translucent gold",
        "Chocolate tri-blend": "Chocolate tri-blend (white, milk, dark – soft marble effect)",
        "White chocolate velvet": "White chocolate velvet, fine cocoa butter texture"
    },
    "🧶 TEXTILES & MOUSSES": {
        "Felted wool fabric": "Felted wool fabric, organic soft fibers",
        "Cotton quilted padding": "Cotton quilted padding, soft cushions, fabric seams",
        "Velvet microfabric": "Velvet microfabric, light-absorbing soft pile",
        "Cotton fiber cloud": "Cotton fiber cloud, wispy and ethereal",
        "Memory foam sponge": "Memory foam sponge, slow-reacting density",
        "Soft porous sponge": "Soft porous sponge, visible foam cells"
    },
    "📜 PAPIER & BOIS": {
        "Handmade paper (grain)": "Handmade paper (soft grain), raw organic edges",
        "Paper mâché (smooth)": "Paper mâché (smooth), hardened pulp texture",
        "Origami layered paper": "Origami layered paper, sharp geometric folds",
        "Light birch wood": "Light birch wood (soft grain), natural pale wood",
        "Toy wood (rounded edges)": "Toy wood (rounded edges), smooth lacquered finish",
        "Milk-painted wood": "Milk-painted wood (pastel), matte chalky wood finish"
    },
    "🧩 JOUETS & ARGILE": {
        "Soft clay (matte)": "Soft clay (matte), hand-molded look",
        "Porcelain clay": "Porcelain clay (silky matte), high-end ceramic",
        "lego": "Lego plastic ABS, high gloss, modular brick surface"
    }
}

# --- 3. BASE DE DONNÉES DESTINATIONS (EXTRAIT) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro."},
        2: {"nom": "Les Quais de Seine", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine."},
        3: {"nom": "Au pied de la Tour", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tour."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars."}}}
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director V30", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("ÉTAPE ACTUELLE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. LOGIQUE SIDEBAR ---
with st.sidebar:
    st.title("🎬 PILOTAGE PRODUCTION")
    mode_manuel = st.toggle("ACTIVER LE CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (Scénario)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    # Variables Initialisation
    b7, b6 = "Golden Hour", "wide-angle lens"
    i34, i35 = "low-angle ground perspective", "bedtime-friendly soft light"
    d8_val, d9_val = "Marshmallow foam", "none"
    b10, b11 = "soft tactile textures", "none"

    if mode_manuel:
        st.divider()
        if "DÉCOR" in etape:
            b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
            b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
            cat_d8 = st.selectbox("CATEGORIE D8", list(MAT_MAP.keys()))
            d8_ui = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()))
            d8_val = MAT_MAP[cat_d8][d8_ui]
            b10 = st.text_input("SOL (B10)", value="soft tactile textures")
            b11 = st.selectbox("1er PLAN (B11)", ["none", "wild flowers", "puddles", "leaves"])
        
        elif "IMAGE" in etape:
            st.subheader("🧬 CONFIGURATION IMAGE")
            s_paws_en = st.selectbox("1. Pose Mélo", ["relaxed", "one paw raised", "sitting", "walking", "clinging"])
            s_expr_en = st.selectbox("2. Expression Mélo", ["curious", "amazed", "smiling", "sleepy", "concentrating"])
            s_pipo_pose_en = st.selectbox("3. Pose Pipo", ["softly floating", "orbiting", "static", "playful dash"])
            s_pipo_pos_en = st.selectbox("4. Position Pipo", ["near head", "on shoulder", "in front of chest", "behind Mélo"])
            s_acc_en = st.text_input("5. Mélo Accessory (EN)", value="Red Beret")
            s_palette_en = st.selectbox("6. Color Palette", ["Natural cinematic", "Pastel tones", "High contrast dream", "Monochrome blue accent"])
            s_pipo_col_en = st.selectbox("7. Pipo Color", ["Iridescent white", "Pure pearl white", "Soft multicolor glow"])
            s_energy_en = st.selectbox("8. Pipo Energy Trail", ["Soft glow", "Ribbon of light", "Sparkling dust", "None"])
        
        elif "VIDÉO" in etape:
            st.subheader("🎞️ CONFIGURATION VIDÉO")
            s_action_en = st.text_input("Mouvement Mélo (EN)", value="Slow cinematic breathing")
            s_video_energy = st.selectbox("Intensité Énergie", ["Subtle", "Medium", "High"])
        
        b5_id = b5_id if "DÉCOR" in etape else auto_b5
    else:
        b5_id = auto_b5

# --- 6. CALCUL PROMPT 1 (XLSX) ---
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
b12 = ville['lieux'][b5_id]['cue']
mat_sec = f" and {d9_val}" if d9_val != "none" else ""
sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

prompt_1 = (
    f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
    f"The scene is set in {ville['nom']} during the {final_light}. Camera: {final_angle}. "
    f"MATERIAL: {d8_val}{mat_sec}. Surfaces: {sugar}. GROUND: {b10}. "
    f"PLATE CUES (STRICT): {b12}. RULES: Pure background plate."
)

# --- 7. ZONE PRINCIPALE ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")

if "DÉCOR" in etape:
    st.subheader("Prompt 1 (DÉCOR)")
    st.code(prompt_1, language="text")

elif "IMAGE" in etape:
    st.subheader("Prompt 2 (IMAGE)")
    # Construction du prompt 2 avec les 8 paramètres
    prompt_2 = (
        f"Character Integration: MÉLO ({DNA_MELO}). PIPO ({DNA_PIPO}). "
        f"Melo Pose: {s_paws_en}. Melo Expression: {s_expr_en}. Melo Accessory: {s_acc_en}. "
        f"Pipo Pose: {s_pipo_pose_en} at position {s_pipo_pos_en}. "
        f"Color Palette: {s_palette_en}. Pipo Color: {s_pipo_col_en}. "
        f"Energy Trail: {s_energy_en}. Material: {MATERIAL_MAIN_DNA}. [LOCKS]: {TECH_LOCKS}."
    )
    st.code(prompt_2, language="text")
    st.button("🚀 Envoyer vers Nanobanana Pro (Simulation API)")

elif "VIDÉO" in etape:
    st.subheader("Prompt 3 (VIDÉO)")
    prompt_3 = f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo trail: {s_energy_en}. Perfect loop."
    st.code(prompt_3, language="text")
