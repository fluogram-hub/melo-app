import streamlit as st

# --- 1. ADN & BIBLE B22 (LOCKS STRICTS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX DÉCOR (D8 / D9 - CATÉGORIES) ---
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

# --- 3. BASE DE DONNÉES COMPLÈTE : 20 DESTINATIONS / 80 LIEUX (B9 / E / F) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro. Keep framing stable, no characters, no animals, no text."},
        2: {"nom": "Les Quais de Seine", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine. Keep framing stable, no characters, no animals, no text."},
        3: {"nom": "Au pied de la Tour", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tour. Keep framing stable, no characters, no animals, no text."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars. Keep framing stable, no characters, no animals, no text."}}},
    "mont_st_michel": {"nom": "Le Mont Saint-Michel (France)", "landmark": "Mont-Saint-Michel", "lieux": {
        1: {"nom": "La Baie", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Baie."},
        2: {"nom": "La Porte d'Entrée", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Porte d'Entrée."},
        3: {"nom": "Le Cloître", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: Le Cloître."},
        4: {"nom": "Les Dunes", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: Les Dunes."}}},
    "santorini": {"nom": "Santorin (Grèce)", "landmark": "Santorini architecture", "lieux": {
        1: {"nom": "La Vue Haute", "cue": "Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset."},
        2: {"nom": "La Ruelle Blanche", "cue": "Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset."},
        3: {"nom": "La Terrasse", "cue": "Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset."},
        4: {"nom": "Le Muret", "cue": "Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset."}}},
    "venice": {"nom": "Venise (Italie)", "landmark": "Venice canals", "lieux": {
        1: {"nom": "Le Grand Canal", "cue": "Venice canals, calm water reflections, historic facades, soft lantern bokeh."},
        2: {"nom": "La Petite Ruelle", "cue": "Venice canals, calm water reflections, historic facades, soft lantern bokeh."},
        3: {"nom": "La Place Saint-Marc", "cue": "Venice canals, calm water reflections, historic facades, soft lantern bokeh."},
        4: {"nom": "L'Intérieur de la Gondole", "cue": "Venice canals, calm water reflections, historic facades, soft lantern bokeh."}}},
    # ... (Structure prête pour les 20 autres)
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Master", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("ÉTAPE ACTUELLE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. LOGIQUE SIDEBAR (PILOTAGE XLSX) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    mode_manuel = st.toggle("ACTIVER LE CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (Scénario)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    # Paramètres par défaut
    b6, b7, b8, b10, b11 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", "none"
    d8_val, d9_val = "Marshmallow foam", "none"
    i34, i35 = "low-angle ground perspective", "bedtime-friendly soft light"

    if mode_manuel:
        st.divider()
        if "DÉCOR" in etape:
            b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1, 2, 3, 4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
            b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
            cat_d8 = st.selectbox("CATEGORIE D8", list(MAT_MAP.keys()))
            d8_ui = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()))
            d8_val = MAT_MAP[cat_d8][d8_ui]
            cat_d9 = st.selectbox("CATEGORIE D9", ["none"] + list(MAT_MAP.keys()))
            if cat_d9 != "none":
                d9_ui = st.selectbox("MATÉRIEL D9", list(MAT_MAP[cat_d9].keys()))
                d9_val = MAT_MAP[cat_d9][d9_ui]
            else: d9_val = "none"
            b10 = st.text_input("SOL (B10)", value="soft tactile textures")
            b11 = st.selectbox("1er PLAN (B11)", ["none", "wild flowers", "puddles", "leaves"])
            i35 = st.text_input("MANUAL LIGHT (I35)", value="bedtime-friendly soft light")
        else: b5_id = auto_b5
    else: b5_id = auto_b5

# --- 6. CALCUL FORMULE XLSX (PROMPT 1) ---
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
b12 = ville['lieux'][b5_id]['cue']

fg_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "none" else ""
mat_sec = f" and {d9_val}" if d9_val != "none" else ""
sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

prompt_1 = (
    f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
    f"The scene is set in {ville['nom']} during the {final_light}, with a {b8} atmosphere. "
    f"The camera uses a {final_angle} with a low-angle ground perspective. {fg_str}"
    f"MATERIAL WORLD & SHADING: All surfaces reimagined in {d8_val}{mat_sec}. "
    f"Surfaces feature realistic subsurface scattering and {sugar}. "
    f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant silhouette. "
    f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays. GROUND: {b10}. "
    f"PLATE CUES (STRICT): {b12}. "
    f"RULES: No characters, no people, no text. Pure background plate."
)

# --- 7. ZONE D'AFFICHAGE ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")

if "DÉCOR" in etape:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 LIEU PRÉCIS (B5)</div><div class="action-text">{ville["lieux"][b5_id]["nom"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE / SOL</div><div class="action-text">{final_angle} | {b10}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE (B7/I35)</div><div class="action-text">{final_light}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🍭 MATÉRIEL (D8)</div><div class="action-text">{d8_val[:15]}...</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt 1 (Fond de décor - Formule XLSX)")
    st.code(prompt_1, language="text")

elif "IMAGE" in etape:
    st.subheader("Prompt 2 (Intégration B22)")
    p2 = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Material: {MATERIAL_MAIN_DNA}. [LOCKS]: {TECH_LOCKS}."
    st.code(p2, language="text")

elif "VIDÉO" in etape:
    st.subheader("Prompt 3 (Mouvement)")
    p3 = f"Animation (8s): Mélo in {ville['nom']} in ultra-slow motion. Perfect loop."
    st.code(p3, language="text")
