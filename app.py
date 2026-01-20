import streamlit as st

# --- 1. ADN & BIBLE B22 (LOCKS STRICTS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. MATÉRIAUX (D8 / D9) ---
MAT_LIST = ["Translucent jelly candy (glossy)", "Marshmallow foam (matte soft)", "Fondant sugar paste (matte)", "Honey wax (warm glow)", "Chocolate tri-blend", "Felted wool fabric", "Cotton quilted padding", "Light birch wood", "Toy wood", "lego"]

# --- 3. BASE DE DONNÉES COMPLÈTE : 20 DESTINATIONS (COLONNE A, E, F) ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Trocadéro", "cue": "Architectural symmetry of the esplanade, stone textures dominant"},
        2: {"nom": "Quais de Seine", "cue": "Water reflections and cobblestone wetness, low horizon"},
        3: {"nom": "Pied de la Tour", "cue": "Detailed iron lattice work, upward perspective"},
        4: {"nom": "Champ-de-Mars", "cue": "Grass textures and soft sunset diffusion"}}},
    "mont_saint_michel": {"nom": "Mont St-Michel", "landmark": "Abbey silhouette", "lieux": {
        1: {"nom": "Baie sableuse", "cue": "Focus on wet sand ripples and shallow water reflections"},
        2: {"nom": "Remparts", "cue": "Ancient stone textures, sea breeze atmosphere"},
        3: {"nom": "Abbaye", "cue": "Gothic architectural details, soft stone glow"},
        4: {"nom": "Ruelle médiévale", "cue": "Medieval timber-frame textures, warm lantern light"}}},
    "santorini": {"nom": "Santorin", "landmark": "Blue Dome Church", "lieux": {
        1: {"nom": "Murs blancs", "cue": "High-key lighting, smooth white plaster"},
        2: {"nom": "Escaliers", "cue": "Deep blue water bokeh, geometric white steps"},
        3: {"nom": "Terrasse", "cue": "Aegean sea horizon, soft sunset glow"},
        4: {"nom": "Dôme bleu", "cue": "Cobalt blue surface contrast with white walls"}}},
    "venice": {"nom": "Venise", "landmark": "St Mark's Basilica", "lieux": {
        1: {"nom": "Grand Canal", "cue": "Water ripples, gondola silhouettes, ancient facades"},
        2: {"nom": "Pont des Soupirs", "cue": "Narrow canal perspective, stone bridge textures"},
        3: {"nom": "Place St-Marc", "cue": "Intricate paving patterns, Byzantine details"},
        4: {"nom": "Gondole", "cue": "Internal wooden boat textures, water level view"}}},
    "taj_mahal": {"nom": "Taj Mahal", "landmark": "Taj Mahal dome", "lieux": {
        1: {"nom": "Bassin miroir", "cue": "Perfect symmetry, white marble reflections"},
        2: {"nom": "Porte principale", "cue": "Red sandstone framing the white monument"},
        3: {"nom": "Jardin", "cue": "Cypress trees, symmetrical paths, soft morning mist"},
        4: {"nom": "Bord Yamuna", "cue": "Distant silhouette across the river, glowing mist"}}},
    "giza": {"nom": "Gizeh", "landmark": "Great Pyramid", "lieux": {
        1: {"nom": "Dunes", "cue": "Fine sand ripples, vast desert horizon"},
        2: {"nom": "Pied Pyramide", "cue": "Macro stone block textures, immense scale"},
        3: {"nom": "Sphinx", "cue": "Ancient weathered limestone textures, profile view"},
        4: {"nom": "Désert nuit", "cue": "Starry sky, silhouette of pyramids, deep shadows"}}},
    "petra": {"nom": "Petra", "landmark": "Al-Khazneh (The Treasury)", "lieux": {
        1: {"nom": "Le Siq", "cue": "Narrow canyon walls, high verticality, sandstone textures"},
        2: {"nom": "Le Trésor", "cue": "Intricate rock-cut architecture, rosy sandstone glow"},
        3: {"nom": "Haut-Lieu", "cue": "Panoramic desert view, sacrificial stone textures"},
        4: {"nom": "Grottes", "cue": "Internal cave textures, play of light and shadow"}}},
    "lapland": {"nom": "Laponie", "landmark": "Arctic Cabin", "lieux": {
        1: {"nom": "Forêt neige", "cue": "Crystalline snow on pine branches, soft bokeh"},
        2: {"nom": "Igloo", "cue": "Translucent ice blocks, internal warm glow"},
        3: {"nom": "Traîneau", "cue": "Wooden textures, fur rugs, snowy path"},
        4: {"nom": "Ciel Aurores", "cue": "Green glowing light trails, snowy silhouettes"}}},
    "fuji": {"nom": "Mont Fuji", "landmark": "Fuji-san Peak", "lieux": {
        1: {"nom": "Lac Kawaguchi", "cue": "Still water reflection, cherry blossoms"},
        2: {"nom": "Pagode", "cue": "Red lacquered wood, distant snowy peak"},
        3: {"nom": "Forêt pins", "cue": "Soft moss, sunlight filtering through needles"},
        4: {"nom": "Village", "cue": "Traditional thatched roofs, morning mist"}}},
    "ny_times_square": {"nom": "New York", "landmark": "Times Square billboards", "lieux": {
        1: {"nom": "Times Square", "cue": "Neon light reflections, asphalt textures, urban density"},
        2: {"nom": "Central Park", "cue": "Contrast of nature and skyscrapers, soft pond reflections"},
        3: {"nom": "Brooklyn Bridge", "cue": "Steel cable textures, wooden planks, city silhouette"},
        4: {"nom": "Subway", "cue": "Tiled walls, metallic train surfaces, cinematic depth"}}},
    "great_wall": {"nom": "Grande Muraille", "landmark": "Watchtower", "lieux": {
        1: {"nom": "Tour de guet", "cue": "Ancient brick textures, window framing the landscape"},
        2: {"nom": "Crête", "cue": "Infinite path receding into the mist, stone textures"},
        3: {"nom": "Escaliers", "cue": "Steep perspective, weathered stone steps"},
        4: {"nom": "Brouillard", "cue": "Atmospheric depth, silhouette of mountains"}}},
    "machu_picchu": {"nom": "Machu Picchu", "landmark": "Inca Ruins", "lieux": {
        1: {"nom": "Terrasses", "cue": "Green grass layers, precise stone masonry"},
        2: {"nom": "Sommet", "cue": "Looking down on ruins, dramatic cloud bokeh"},
        3: {"nom": "Temple", "cue": "Massive granite blocks, geometric shadows"},
        4: {"nom": "Porte Soleil", "cue": "Distant view through an archway, morning glow"}}},
    "bali_ubud": {"nom": "Bali", "landmark": "Rice Terrace", "lieux": {
        1: {"nom": "Tegalalang", "cue": "Lush green layers, tropical palm silhouettes"},
        2: {"nom": "Temple Eau", "cue": "Mossy stone carvings, clear water reflections"},
        3: {"nom": "Forêt Singes", "cue": "Banyan tree roots, filtered sunlight, stone idols"},
        4: {"nom": "Cascade", "cue": "Volumetric water spray, wet rock textures"}}},
    "safari_kenya": {"nom": "Masai Mara", "landmark": "Acacia Tree", "lieux": {
        1: {"nom": "Savane", "cue": "Golden dry grass textures, flat horizon"},
        2: {"nom": "Acacia", "cue": "Silhouetted tree against sunset, vast negative space"},
        3: {"nom": "Rivière", "cue": "Muddy water textures, hippo silhouettes"},
        4: {"nom": "Campement", "cue": "Canvas textures, wooden poles, evening fire glow"}}},
    "london_big_ben": {"nom": "Londres", "landmark": "Big Ben Clock", "lieux": {
        1: {"nom": "Big Ben", "cue": "Gothic stone carvings, gold clock face details"},
        2: {"nom": "Cabine Rouge", "cue": "Reflective red paint, glass textures, rain bokeh"},
        3: {"nom": "Tower Bridge", "cue": "Blue steel structure, stone pillars, river mist"},
        4: {"nom": "Parc Royal", "cue": "Manicured grass, distant city silhouette"}}},
    "rio_christ": {"nom": "Rio", "landmark": "Christ the Redeemer", "lieux": {
        1: {"nom": "Corcovado", "cue": "Soapstone texture of the statue, clouds below"},
        2: {"nom": "Copacabana", "cue": "Patterned pavement, white sand, ocean bokeh"},
        3: {"nom": "Pain de Sucre", "cue": "Granite rock textures, bay view from above"},
        4: {"nom": "Escaliers", "cue": "Colorful mosaic tile textures, urban depth"}}},
    "kyoto_fushimi": {"nom": "Kyoto", "landmark": "Fushimi Inari Torii", "lieux": {
        1: {"nom": "Torii Path", "cue": "Infinite red lacquered gates, rhythmic perspective"},
        2: {"nom": "Bambouseraie", "cue": "Vertical green stalk textures, filtered light"},
        3: {"nom": "Temple d'Or", "cue": "Gold leaf reflections on water, pine tree bokeh"},
        4: {"nom": "Ruelle Gion", "cue": "Wooden machiya facades, paper lanterns"}}},
    "sydney_opera": {"nom": "Sydney", "landmark": "Opera House Sails", "lieux": {
        1: {"nom": "Opéra", "cue": "Ceramic tile textures of the sails, harbor water"},
        2: {"nom": "Bridge", "cue": "Massive steel bolt textures, bridge perspective"},
        3: {"nom": "Bondi", "cue": "Ocean spray, white sand, turquoise water depth"},
        4: {"nom": "Ferry", "cue": "Metallic deck textures, city view from the water"}}},
    "moscow_red_square": {"nom": "Moscou", "landmark": "St. Basil's Cathedral", "lieux": {
        1: {"nom": "Place Rouge", "cue": "Cobblestone expanse, red brick Kremlin walls"},
        2: {"nom": "St Basile", "cue": "Intricate colorful dome patterns, stone textures"},
        3: {"nom": "Métro", "cue": "Ornate marble pillars, bronze statues, glowing light"},
        4: {"nom": "Bord de l'eau", "cue": "River reflections of the city lights, winter mist"}}},
    "antelope_canyon": {"nom": "Antelope Canyon", "landmark": "Sandstone Slot Canyon", "lieux": {
        1: {"nom": "Slot Canyon", "cue": "Flowing rock wave textures, orange/purple glow"},
        2: {"nom": "Light Beam", "cue": "Volumetric sunbeam hitting the canyon floor"},
        3: {"nom": "Vagues", "cue": "Macro focus on layered sandstone sediment"},
        4: {"nom": "Entrée", "cue": "Narrow desert entrance, sharp contrast of light"}}}
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production World Tour", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)

# --- 5. SIDEBAR (LOGIQUE XLSX) ---
with st.sidebar:
    st.title("🎬 STUDIO WORLD TOUR")
    mode_manuel = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (Scénario)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    # Paramètres par défaut (XLSX)
    b6, b7, b8, b10, b11 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", "none"
    d8, d9 = MAT_LIST[0], "none"
    i34, i35 = "low-angle ground perspective", "bedtime-friendly soft light"

    if mode_manuel:
        st.divider()
        if "DÉCOR" in etape:
            b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1, 2, 3, 4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
            b6 = st.selectbox("ANGLE (B6)", ["wide-angle lens", "macro lens", "fisheye"])
            b7 = st.selectbox("LUMIÈRE (B7)", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
            i34 = st.text_input("MANUAL ANGLE (I34)", value="cinematic ground level view")
            i35 = st.text_input("MANUAL LIGHT (I35)", value="bedtime-friendly soft light")
            b10 = st.text_input("SOL (B10)", value="soft tactile textures")
            b11 = st.selectbox("1er PLAN (B11)", ["none", "wild flowers", "puddles", "leaves"])
            d8 = st.selectbox("MATÉRIAU 1 (D8)", MAT_LIST)
            d9 = st.selectbox("MATÉRIAU 2 (D9)", ["none"] + MAT_LIST)
        else: b5_id = auto_b5
    else: b5_id = auto_b5

# --- 6. CALCUL FORMULE XLSX (PROMPT 1) ---
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
b12 = ville['lieux'][b5_id]['cue']

fg_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "none" else ""
mat_sec = f" and {d9}" if d9 != "none" else ""
sugar = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"

prompt_1 = (
    f"An ultra-detailed cinematic environment photography of {ville['landmark']}. "
    f"The scene is set in {ville['nom']} during the {final_light}, with a {b8} atmosphere. "
    f"The camera uses a {final_angle} with a low-angle ground perspective. {fg_str}"
    f"MATERIAL WORLD & SHADING: All surfaces reimagined in {d8}{mat_sec}. "
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
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE (B6/I34)</div><div class="action-text">{final_angle}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE (B7/I35)</div><div class="action-text">{final_light}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🍭 MATÉRIEL (D8)</div><div class="action-text">{d8[:15]}...</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt 1 (Fond de décor)")
    st.code(prompt_1, language="text")

elif "IMAGE" in etape:
    st.subheader("Prompt 2 (Intégration B22)")
    p2 = f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Material: {MATERIAL_MAIN_DNA}. [LOCKS]: {TECH_LOCKS}."
    st.code(p2, language="text")

elif "VIDÉO" in etape:
    st.subheader("Prompt 3 (Mouvement)")
    p3 = f"Animation (8s): Mélo in {ville['nom']} in ultra-slow motion. Perfect loop, cinematic PBR."
    st.code(p3, language="text")

# --- 8. EXPORT ---
st.divider()
if st.button("💾 EXPORTER TOUS LES PROMPTS DU PLAN"):
    export = f"PLAN {p_id} | {ville['nom']}\nPROMPT 1: {prompt_1}"
    st.code(export, language="text")
