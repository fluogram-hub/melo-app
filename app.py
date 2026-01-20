import streamlit as st

# --- 1. ADN & BIBLE B22 (LOCKS STRICTS) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX (D8 / D9) ---
MAT_LIST = [
    "Translucent jelly candy (glossy)", "Translucent colored jelly candy (glossy)", "Hard candy (polished smooth)", 
    "Marshmallow foam (matte soft)", "Fondant sugar paste (matte)", "Honey wax (warm glow)", 
    "Chocolate tri-blend", "White chocolate velvet", "Felted wool fabric", "Cotton quilted padding", 
    "Velvet microfabric", "Cotton fiber cloud", "Memory foam sponge", "Soft porous sponge", 
    "Handmade paper (soft grain)", "Paper mâché (smooth)", "Origami layered paper", 
    "Light birch wood", "Toy wood", "Milk-painted wood (pastel)", "Soft clay (matte)", 
    "Porcelain clay (silky matte)", "lego"
]

# --- 3. BASE DE DONNÉES COMPLÈTE (20 DESTINATIONS / 80 LIEUX) ---
DESTINATIONS = {
    "paris": {"nom": "La Tour Eiffel (Paris, France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro. Keep framing stable, no characters, no animals, no text."},
        2: {"nom": "Les Quais de Seine", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine. Keep framing stable, no characters, no animals, no text."},
        3: {"nom": "Au pied de la Tour", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tour. Keep framing stable, no characters, no animals, no text."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars. Keep framing stable, no characters, no animals, no text."}}},
    "mont_st_michel": {"nom": "Le Mont Saint-Michel (France)", "landmark": "Mont-Saint-Michel", "lieux": {
        1: {"nom": "La Baie", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Baie. Keep framing stable, no characters, no animals, no text."},
        2: {"nom": "La Porte d'Entrée", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Porte d'Entrée. Keep framing stable, no characters, no animals, no text."},
        3: {"nom": "Le Cloître", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: Le Cloître. Keep framing stable, no characters, no animals, no text."},
        4: {"nom": "Les Dunes", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: Les Dunes. Keep framing stable, no characters, no animals, no text."}}},
    "santorini": {"nom": "Santorin (Grèce)", "landmark": "Santorini architecture", "lieux": {
        1: {"nom": "La Vue Haute", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Vue Haute. Keep framing stable, no characters, no animals, no text."},
        2: {"nom": "La Ruelle Blanche", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Ruelle Blanche. Keep framing stable, no characters, no animals, no text."},
        3: {"nom": "La Terrasse", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Terrasse. Keep framing stable, no characters, no animals, no text."},
        4: {"nom": "Le Muret", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: Le Muret. Keep framing stable, no characters, no animals, no text."}}},
    "venice": {"nom": "Venise (Italie)", "landmark": "Venice canals", "lieux": {
        1: {"nom": "Le Grand Canal", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: Le Grand Canal. Keep framing stable, no characters, no animals, no text."},
        2: {"nom": "La Petite Ruelle", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: La Petite Ruelle. Keep framing stable, no characters, no animals, no text."},
        3: {"nom": "La Place Saint-Marc", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: La Place Saint-Marc. Keep framing stable, no characters, no animals, no text."},
        4: {"nom": "L'Intérieur de la Gondole", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: L'Intérieur de la Gondole. Keep framing stable, no characters, no animals, no text."}}},
    "neuschwanstein": {"nom": "Château de Neuschwanstein (Allemagne)", "landmark": "Fairytale castle", "lieux": {
        1: {"nom": "Le Pont Marie", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Fairytale castle silhouette, Bavarian alpine forest, soft snow or mist, calm. Specific setting: Le Pont Marie."},
        2: {"nom": "Le Chemin de Forêt", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Fairytale castle silhouette, Bavarian alpine forest, soft snow or mist, calm. Specific setting: Le Chemin de Forêt."},
        3: {"nom": "La Cour du Château", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Fairytale castle silhouette, Bavarian alpine forest, soft snow or mist, calm. Specific setting: La Cour du Château."},
        4: {"nom": "Le Balcon", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Fairytale castle silhouette, Bavarian alpine forest, soft snow or mist, calm. Specific setting: Le Balcon."}}},
    "london": {"nom": "Big Ben (Londres, UK)", "landmark": "Big Ben", "lieux": {
        1: {"nom": "Le Pont de Westminster", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Big Ben clock tower silhouette, London classic stone. Specific setting: Le Pont de Westminster."},
        2: {"nom": "La Cabine Téléphonique", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Big Ben clock tower silhouette, London classic stone. Specific setting: La Cabine Téléphonique."},
        3: {"nom": "Le Quai de la Tamise", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Big Ben clock tower silhouette, London classic stone. Specific setting: Le Quai de la Tamise."},
        4: {"nom": "Le Banc du Parc", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Big Ben clock tower silhouette, London classic stone. Specific setting: Le Banc du Parc."}}},
    "kinderdijk": {"nom": "Moulins de Kinderdijk (Pays-Bas)", "landmark": "Dutch windmills", "lieux": {
        1: {"nom": "Le Sentier du Canal", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Dutch windmills, flat canals, slow reflections. Specific setting: Le Sentier du Canal."},
        2: {"nom": "Le Pont de Bois", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Dutch windmills, flat canals, slow reflections. Specific setting: Le Pont de Bois."},
        3: {"nom": "Le Pied du Moulin", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Dutch windmills, flat canals, slow reflections. Specific setting: Le Pied du Moulin."},
        4: {"nom": "Le Pont de la Barque", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Dutch windmills, flat canals, slow reflections. Specific setting: Le Pont de la Barque."}}},
    "fuji": {"nom": "Le Mont Fuji (Japon)", "landmark": "Mount Fuji", "lieux": {
        1: {"nom": "Le Lac Kawaguchi", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mount Fuji recognizable, quiet lake reflections. Specific setting: Le Lac Kawaguchi."},
        2: {"nom": "Le Portail Torii", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mount Fuji recognizable, quiet lake reflections. Specific setting: Le Portail Torii."},
        3: {"nom": "Le Jardin de Cerisiers", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mount Fuji recognizable, quiet lake reflections. Specific setting: Le Jardin de Cerisiers."},
        4: {"nom": "Le Tapis de Mousse", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mount Fuji recognizable, quiet lake reflections. Specific setting: Le Tapis de Mousse."}}},
    "taj_mahal": {"nom": "Le Taj Mahal (Inde)", "landmark": "Taj Mahal", "lieux": {
        1: {"nom": "L'Allée Centrale", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Taj Mahal symmetrical white marble, long reflecting pool. Specific setting: L'Allée Centrale."},
        2: {"nom": "Le Jardin de Fleurs", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Taj Mahal symmetrical white marble, long reflecting pool. Specific setting: Le Jardin de Fleurs."},
        3: {"nom": "La Terrasse de Marbre", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Taj Mahal symmetrical white marble, long reflecting pool. Specific setting: La Terrasse de Marbre."},
        4: {"nom": "Le Banc de Pierre", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Taj Mahal symmetrical white marble, long reflecting pool. Specific setting: Le Banc de Pierre."}}},
    "china_wall": {"nom": "La Grande Muraille (Chine)", "landmark": "Great Wall", "lieux": {
        1: {"nom": "La Crête de Montagne", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Great Wall serpentine line across mountains. Specific setting: La Crête de Montagne."},
        2: {"nom": "L'Intérieur de la Tour", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Great Wall serpentine line across mountains. Specific setting: L'Intérieur de la Tour."},
        3: {"nom": "L'Escalier de Pierre", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Great Wall serpentine line across mountains. Specific setting: L'Escalier de Pierre."},
        4: {"nom": "La Tour de Guet", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Great Wall serpentine line across mountains. Specific setting: La Tour de Guet."}}},
    "ha_long": {"nom": "La Baie d'Ha Long (Vietnam)", "landmark": "Ha Long Bay", "lieux": {
        1: {"nom": "La Mer", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Ha Long Bay karst islands, calm emerald water. Specific setting: La Mer."},
        2: {"nom": "Le Village Flottant", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Ha Long Bay karst islands, calm emerald water. Specific setting: Le Village Flottant."},
        3: {"nom": "La Grotte", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Ha Long Bay karst islands, calm emerald water. Specific setting: La Grotte."},
        4: {"nom": "Le Pont de la Jonque", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Ha Long Bay karst islands, calm emerald water. Specific setting: Le Pont de la Jonque."}}},
    "liberty": {"nom": "La Statue de la Liberté (New York, USA)", "landmark": "Statue of Liberty", "lieux": {
        1: {"nom": "Le Ferry", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Statue of Liberty silhouette, calm harbor water. Specific setting: Le Ferry."},
        2: {"nom": "Le Socle de la Statue", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Statue of Liberty silhouette, calm harbor water. Specific setting: Le Socle de la Statue."},
        3: {"nom": "La Promenade de l'Île", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Statue of Liberty silhouette, calm harbor water. Specific setting: La Promenade de l'Île."},
        4: {"nom": "Le Banc de Liberty Island", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Statue of Liberty silhouette, calm harbor water. Specific setting: Le Banc de Liberty Island."}}},
    "machu_picchu": {"nom": "Machu Picchu (Pérou)", "landmark": "Machu Picchu", "lieux": {
        1: {"nom": "La Vue Haute", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Machu Picchu ruins, high clouds and mist. Specific setting: La Vue Haute."},
        2: {"nom": "Les Terrasses Agricoles", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Machu Picchu ruins, high clouds and mist. Specific setting: Les Terrasses Agricoles."},
        3: {"nom": "Le Temple du Soleil", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Machu Picchu ruins, high clouds and mist. Specific setting: Le Temple du Soleil."},
        4: {"nom": "Le Champ de Sommet", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Machu Picchu ruins, high clouds and mist. Specific setting: Le Champ de Sommet."}}},
    "golden_gate": {"nom": "Golden Gate Bridge (San Francisco, USA)", "landmark": "Golden Gate Bridge", "lieux": {
        1: {"nom": "Vista Point", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Golden Gate Bridge iconic orange-red. Specific setting: Vista Point."},
        2: {"nom": "Le Pont (Trottoir)", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Golden Gate Bridge iconic orange-red. Specific setting: Le Pont (Trottoir)."},
        3: {"nom": "Baker Beach", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Golden Gate Bridge iconic orange-red. Specific setting: Baker Beach."},
        4: {"nom": "La Pelouse de Presidio", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Golden Gate Bridge iconic orange-red. Specific setting: La Pelouse de Presidio."}}},
    "rio": {"nom": "Christ Rédempteur (Rio, Brésil)", "landmark": "Christ the Redeemer", "lieux": {
        1: {"nom": "Le Belvédère", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Christ the Redeemer silhouette, bay far below. Specific setting: Le Belvédère."},
        2: {"nom": "Le Train de Corcovado", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Christ the Redeemer silhouette, bay far below. Specific setting: Le Train de Corcovado."},
        3: {"nom": "Le Pied de la Statue", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Christ the Redeemer silhouette, bay far below. Specific setting: Le Pied de la Statue."},
        4: {"nom": "Le Jardin Botanique", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Christ the Redeemer silhouette, bay far below. Specific setting: Le Jardin Botanique."}}},
    "giza": {"nom": "Les Pyramides de Gizeh (Égypte)", "landmark": "Giza Pyramids", "lieux": {
        1: {"nom": "Le Panorama des Dunes", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Giza pyramids geometric silhouettes, smooth sand. Specific setting: Le Panorama des Dunes."},
        2: {"nom": "Le Pied de Khéops", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Giza pyramids geometric silhouettes, smooth sand. Specific setting: Le Pied de Khéops."},
        3: {"nom": "Le Sphinx", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Giza pyramids geometric silhouettes, smooth sand. Specific setting: Le Sphinx."},
        4: {"nom": "La Tente Bédouine", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Giza pyramids geometric silhouettes, smooth sand. Specific setting: La Tente Bédouine."}}},
    "petra": {"nom": "Pétra (Jordanie)", "landmark": "Petra", "lieux": {
        1: {"nom": "Le Siq", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Petra rose sandstone, carved facades. Specific setting: Le Siq."},
        2: {"nom": "Le Trésor", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Petra rose sandstone, carved facades. Specific setting: Le Trésor."},
        3: {"nom": "Le Chemin des Grottes", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Petra rose sandstone, carved facades. Specific setting: Le Chemin des Grottes."},
        4: {"nom": "Le Tapis de Sable", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Petra rose sandstone, carved facades. Specific setting: Le Tapis de Sable."}}},
    "serengeti": {"nom": "La Savane du Serengeti (Tanzanie)", "landmark": "Serengeti Savanna", "lieux": {
        1: {"nom": "La Plaine Infinie", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Serengeti savanna, acacia silhouettes. Specific setting: La Plaine Infinie."},
        2: {"nom": "Le Point d'Eau", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Serengeti savanna, acacia silhouettes. Specific setting: Le Point d'Eau."},
        3: {"nom": "Sous l'Acacia", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Serengeti savanna, acacia silhouettes. Specific setting: Sous l'Acacia."},
        4: {"nom": "Le Campement", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Serengeti savanna, acacia silhouettes. Specific setting: Le Campement."}}},
    "sydney": {"nom": "L'Opéra de Sydney (Australie)", "landmark": "Sydney Opera House", "lieux": {
        1: {"nom": "Circular Quay", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Sydney Opera House sail-like shells. Specific setting: Circular Quay."},
        2: {"nom": "Les Marches de l'Opéra", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Sydney Opera House sail-like shells. Specific setting: Les Marches de l'Opéra."},
        3: {"nom": "Le Jardin Botanique", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Sydney Opera House sail-like shells. Specific setting: Le Jardin Botanique."},
        4: {"nom": "Le Banc Face à l'Eau", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Sydney Opera House sail-like shells. Specific setting: Le Banc Face à l'Eau."}}},
    "lapland": {"nom": "La Laponie (Pôle Nord)", "landmark": "Lapland", "lieux": {
        1: {"nom": "La Forêt de Sapins", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Lapland snowy landscape, soft aurora glow. Specific setting: La Forêt de Sapins."},
        2: {"nom": "L'Extérieur de l'Igloo", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Lapland snowy landscape, soft aurora glow. Specific setting: L'Extérieur de l'Igloo."},
        3: {"nom": "Le Traîneau", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Lapland snowy landscape, soft aurora glow. Specific setting: Le Traîneau."},
        4: {"nom": "L'Intérieur de l'Igloo", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Lapland snowy landscape, soft aurora glow. Specific setting: L'Intérieur de l'Igloo."}}}
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Hub V28", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. SIDEBAR (LOGIQUE XLSX) ---
with st.sidebar:
    st.title("🎬 STUDIO GÉNÉRATEUR")
    mode_manuel = st.toggle("ACTIVER LE CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN (Scénario)", options=list(range(1, 21)))
    
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
            b10 = st.text_input("TEXTURE SOL (B10)", value="soft tactile textures")
            b11 = st.selectbox("PREMIER PLAN (B11)", ["none", "wild flowers", "puddles", "leaves"])
            d8 = st.selectbox("MATÉRIAU PRINCIPAL (D8)", MAT_LIST)
            d9 = st.selectbox("MATÉRIAU SECONDAIRE (D9)", ["none"] + MAT_LIST)
            i34 = st.text_input("OVERRIDE ANGLE (I34)", value="cinematic ground level view")
            i35 = st.text_input("OVERRIDE LUMIÈRE (I35)", value="bedtime-friendly soft light")
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
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🍭 MATÉRIAU (D8)</div><div class="action-text">{d8[:15]}...</div></div>', unsafe_allow_html=True)
    
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
