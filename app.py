import streamlit as st

# --- 1. ADN & LOCKS B22 ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. MATÉRIAUX (D8/D9) & FOREGROUND (B11) ---
MAT_LIST = ["Translucent jelly candy (glossy)", "Translucent colored jelly candy (glossy)", "Hard candy (polished smooth)", "Marshmallow foam (matte soft)", "Fondant sugar paste (matte)", "Honey wax (warm glow)", "Chocolate tri-blend", "White chocolate velvet", "Felted wool fabric", "Cotton quilted padding", "Velvet microfabric", "Light birch wood", "Toy wood", "lego"]

# --- 3. BASE DE DONNÉES COMPLÈTE (Équivalent Onglet DECORS!$L:$M) ---
# Chaque lieu (1-4) possède maintenant sa propre Plate Cue (L:M)
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris", "landmark": "Eiffel Tower", "struct": "B", "obj": "Red beret",
        "lieux": {
            1: {"nom": "Trocadéro", "cue": "Focus on the architectural symmetry of the esplanade, stone textures dominant"},
            2: {"nom": "Quais de Seine", "cue": "Emphasize water reflections and cobblestone wetness, low horizon"},
            3: {"nom": "Pied de la Tour", "cue": "Detailed iron lattice work, upward perspective, metallic shading"},
            4: {"nom": "Champ-de-Mars", "cue": "Focus on grass textures and soft sunset diffusion, minimalist depth"}
        }
    },
    "venice_italy": {
        "nom": "Venice", "landmark": "St Mark's Basilica", "struct": "C", "obj": "Cat mask",
        "lieux": {
            1: {"nom": "Grand Canal", "cue": "Dark water ripples, gondola silhouettes, ancient palace facades"},
            2: {"nom": "Pont des Soupirs", "cue": "Narrow canal perspective, stone bridge textures, soft shadows"},
            3: {"nom": "Place St-Marc", "cue": "Intricate paving patterns, Byzantine architectural details"},
            4: {"nom": "Gondole", "cue": "Internal wooden textures of the boat, water level view"}
        }
    }
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Studio V24", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. SIDEBAR (PILOTAGE XLSX) ---
with st.sidebar:
    st.title("🎬 PILOTAGE PRODUCTION")
    mode_manuel = st.toggle("ACTIVER LE CONTRÔLE MANUEL (E7)", value=False)
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN (1-20)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # Paramètres par défaut (XLSX)
    b6, b7, b8, b10, b11 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", ""
    d8, d9 = MAT_LIST[0], "none"
    i34, i35 = "low-angle ground perspective", "bedtime-friendly soft light"

    if mode_manuel:
        st.divider()
        if "DÉCOR" in etape:
            st.subheader("🛠️ CONFIG DÉCOR")
            # Le sélecteur B5 (Lieu précis)
            b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1, 2, 3, 4], index=auto_d_id-1, format_func=lambda x: ville['lieux'][x]['nom'])
            b6 = st.selectbox("ANGLE (B6)", ["wide-angle lens", "macro lens", "fisheye"])
            b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour"])
            b10 = st.text_input("SOL (B10)", value="soft tactile textures")
            b11 = st.selectbox("1er PLAN (B11)", ["", "wild flowers", "puddles", "leaves"])
            d8 = st.selectbox("MATÉRIAU 1 (D8)", MAT_LIST)
            d9 = st.selectbox("MATÉRIAU 2 (D9)", ["none"] + MAT_LIST)
        else:
            b5_id = auto_d_id # Mode auto par défaut pour les autres onglets
    else:
        b5_id = auto_d_id

# --- 6. CALCUL DU PROMPT 1 (FORMULE EXACTE) ---
# VLOOKUP local (Recherche de la Plate Cue B12)
b12 = ville['lieux'][b5_id]['cue']

# Logique de calcul
e7 = "yes" if mode_manuel else "no"
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
fg_string = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
mat_sec = f" and {d9}" if d9 != "none" else ""
sugar = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"
plate_cues = f"PLATE CUES (STRICT): {b12}. " if b12 != "" else ""

prompt_1 = (
    f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
    f"The scene is set in {ville['nom']} during the {final_light}, with a {b8} atmosphere. "
    f"The camera uses a {final_angle} with a low-angle ground perspective. "
    f"{fg_string}"
    f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8}{mat_sec}. "
    f"Surfaces feature realistic subsurface scattering and {sugar}. "
    f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant, soft-focus silhouette, suggested only by blurred shapes and glowing light. "
    f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays, bedtime-friendly calm palette. "
    f"GROUND DETAIL: The ground is {b10} with high-tactile micro-textures. "
    f"{plate_cues}"
    f"RULES: No characters, no people, no text, no logos, no watermarks. Pure background plate."
)

# --- 7. AFFICHAGE DES ONGLETS ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")

if "DÉCOR" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 LIEU PRÉCIS (B5)</div><div class="action-text">{ville["lieux"][b5_id]["nom"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🎬 PLATE CUE (B12)</div><div class="action-text">{b12[:40]}...</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{final_light}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt 1 (FOND)")
    st.code(prompt_1, language="text")
    if st.button("📋 Copier le Prompt 1"):
        st.write("Prompt copié dans le presse-papier (Simulé)")

elif "IMAGE" in etape:
    st.subheader("Prompt 2 (INTÉGRATION)")
    p2 = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Material: {MATERIAL_MAIN_DNA}. [LOCKS]: {TECH_LOCKS}."
    st.code(p2, language="text")

elif "VIDÉO" in etape:
    st.subheader("Prompt 3 (MOUVEMENT)")
    p3 = f"Animation (8s): Mélo in {ville['nom']} in ultra-slow motion. Perfect loop."
    st.code(p3, language="text")
