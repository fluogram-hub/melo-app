import streamlit as st

# --- 1. ADN & LOCKS B22 ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX (D8 / D9) ---
MAT_LIST = [
    "Translucent jelly candy (glossy)", "Translucent colored jelly candy (glossy)", 
    "Hard candy (polished smooth)", "Marshmallow foam (matte soft)", 
    "Fondant sugar paste (matte)", "Honey wax (warm glow)", 
    "Chocolate tri-blend (white, milk, dark – soft marble)", "White chocolate velvet",
    "Creamy foam texture", "Sponge cake texture", "Felted wool fabric", 
    "Cotton quilted padding", "Velvet microfabric", "Cotton fiber cloud", 
    "Memory foam sponge", "Soft porous sponge", "Handmade paper (soft grain)",
    "Paper mâché (smooth)", "Origami layered paper", "Light birch wood (soft grain)",
    "Toy wood (rounded edges)", "Milk-painted wood (pastel)", "Soft clay (matte)", 
    "Porcelain clay (silky matte)", "lego"
]

# --- 3. DONNÉES DE BASE (B9 / E5) ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris", "landmark": "Eiffel Tower", "struct": "B", "obj": "Red beret"},
    "venice_italy": {"nom": "Venice", "landmark": "St Mark's Basilica", "struct": "C", "obj": "Cat mask"},
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Studio V23", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Navigation par étape
etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTÉGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. LOGIQUE SIDEBAR (MAPPAGE XLSX) ---
with st.sidebar:
    st.title("🎬 PILOTAGE XLSX")
    mode_manuel = st.toggle("ACTIVER LE CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    ville = DESTINATIONS[v_id]
    
    # Paramètres par défaut (Auto)
    b6 = "wide-angle lens" # Camera Angle
    b7 = "Golden Hour"     # Lighting
    b8 = "calm"            # Atmosphere
    b10 = "soft textured sand" # Ground Texture
    b11 = ""               # Foreground
    b12 = ""               # Plate Cues
    d8 = MAT_LIST[0]       # Matériau 1
    d9 = "none"            # Matériau 2
    i34 = "low-angle macro lens" # Override Angle
    i35 = "midnight blue hour"   # Override Light

    if mode_manuel:
        st.divider()
        if "DÉCOR" in etape:
            st.subheader("🛠️ REGLAGES DÉCOR")
            b6 = st.selectbox("Angle de vue (B6)", ["wide-angle lens", "fisheye lens", "35mm lens"])
            b7 = st.selectbox("Horaire/Lumière (B7)", ["Golden Hour", "High Noon", "Sunset"])
            b8 = st.selectbox("Météo/Atmosphère (B8)", ["calm", "misty", "stormy", "dreamy"])
            b10 = st.text_input("Texture du sol (B10)", value="soft tactile velvet")
            b11 = st.selectbox("Premier plan (B11)", ["", "wild flowers", "puddles", "leaves"])
            b12 = st.text_input("Plate Cues (B12)", value="Focus on horizon")
            d8 = st.selectbox("Matériau Principal (D8)", MAT_LIST)
            d9 = st.selectbox("Matériau Secondaire (D9)", ["none"] + MAT_LIST)
            i34 = st.text_input("Override Angle (I34)", value="low-angle ground perspective")
            i35 = st.text_input("Override Lighting (I35)", value="bedtime-friendly soft light")

        elif "IMAGE" in etape:
            st.subheader("🛠️ REGLAGES IMAGE")
            s_paws = st.selectbox("Pose Mélo", ["relaxed", "one paw raised", "sitting"])
            s_expr = st.selectbox("Expression", ["curious", "amazed", "smiling"])
            s_pipo_pos = st.selectbox("Position Pipo", ["near head", "on shoulder", "orbiting"])
            s_palette = st.selectbox("Palette", ["natural", "pastel", "vibrant"])

# --- 6. CALCUL DU PROMPT 1 (FORMULE EXACTE XLSX) ---
# Mapping conditions IF
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
fg_string = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
mat_secondary = f" and {d9}" if d9 != "none" else ""
sugar_finish = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"
plate_cues = f"PLATE CUES (STRICT): {b12}. " if b12 != "" else ""

prompt_1 = (
    f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
    f"The scene is set in {ville['nom']} during the {final_light}, with a {b8} atmosphere. "
    f"The camera uses a {final_angle} with a low-angle ground perspective. "
    f"{fg_string}"
    f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8}{mat_secondary}. "
    f"Surfaces feature realistic subsurface scattering and {sugar_finish}. "
    f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant, soft-focus silhouette, suggested only by blurred shapes and glowing light. "
    f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays, bedtime-friendly calm palette. "
    f"GROUND DETAIL: The ground is {b10} with high-tactile micro-textures. "
    f"{plate_cues}"
    f"RULES: No characters, no people, no text, no logos, no watermarks. Pure background plate."
)

# --- 7. AFFICHAGE DES ONGLETS ---
st.title(f"📍 {ville['nom']} — {ville['landmark']}")

if "DÉCOR" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 LIEU (B9/E5)</div><div class="action-text">{ville["nom"]} | {ville["landmark"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE ({e7})</div><div class="action-text">{final_light}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt 1 (Exact Excel Formula)")
    st.code(prompt_1, language="text")

elif "IMAGE" in etape:
    st.subheader("Prompt 2 (Intégration B22)")
    prompt_2 = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws}. Palette: {s_palette}. Material: {MATERIAL_MAIN_DNA}. [LOCKS]: {TECH_LOCKS}."
    st.code(prompt_2, language="text")

elif "VIDÉO" in etape:
    st.subheader("Prompt 3 (VÉO 3)")
    prompt_3 = f"Animation (8s): Mélo moves in ultra-slow motion in {ville['nom']}. Perfect loop, cinematic PBR."
    st.code(prompt_3, language="text")
