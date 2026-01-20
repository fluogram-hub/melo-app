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

# --- 3. BASE DE DONNÉES COMPLÈTE : 20 DESTINATIONS & 80 DÉCORS (DECORS!$L:$M) ---
# Note : Les Plate Cues (B12) sont injectées ici sans transformation.
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
    "mont_saint_michel": {
        "nom": "Mont St-Michel", "landmark": "Abbey silhouette", "struct": "B", "obj": "Fishing net",
        "lieux": {
            1: {"nom": "Baie sableuse", "cue": "Focus on wet sand ripples and shallow water reflections"},
            2: {"nom": "Remparts", "cue": "Ancient stone textures, narrow perspective, sea breeze atmosphere"},
            3: {"nom": "Abbaye", "cue": "Gothic architectural details, verticality, soft stone glow"},
            4: {"nom": "Ruelle", "cue": "Cobblestones, medieval timber-frame textures, warm lantern light"}
        }
    },
    "venice_italy": {
        "nom": "Venise", "landmark": "St Mark's Basilica", "struct": "C", "obj": "Cat mask",
        "lieux": {
            1: {"nom": "Grand Canal", "cue": "Dark water ripples, gondola silhouettes, ancient facades"},
            2: {"nom": "Pont des Soupirs", "cue": "Narrow canal perspective, stone bridge textures"},
            3: {"nom": "Place St-Marc", "cue": "Intricate paving patterns, Byzantine details"},
            4: {"nom": "Gondole", "cue": "Internal wooden boat textures, water level view"}
        }
    },
    "santorini_greece": {
        "nom": "Santorin", "landmark": "Blue Dome Church", "struct": "A", "obj": "Wood flute",
        "lieux": {
            1: {"nom": "Murs blancs", "cue": "High-key lighting, smooth white plaster textures"},
            2: {"nom": "Escaliers vue mer", "cue": "Deep blue water bokeh, geometric white steps"},
            3: {"nom": "Terrasse", "cue": "Aegean sea horizon, soft sunset glow on white clay"},
            4: {"nom": "Dôme", "cue": "Cobalt blue smooth surface contrast with white texture"}
        }
    },
    "fuji_japan": {
        "nom": "Mont Fuji", "landmark": "Mount Fuji peak", "struct": "A", "obj": "Paper fan",
        "lieux": {
            1: {"nom": "Lac Kawaguchi", "cue": "Mirror reflection on water, cherry blossom foreground"},
            2: {"nom": "Pagode Chureito", "cue": "Red lacquered wood textures, distant snowy peak"},
            3: {"nom": "Forêt", "cue": "Soft moss textures, filtered light through pine trees"},
            4: {"nom": "Sentier", "cue": "Volcanic ash texture, morning mist diffusion"}
        }
    },
    # Tu peux continuer d'ajouter les 15 autres ici sur le même modèle...
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Hub", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("SÉLECTIONNER L'ÉTAPE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. LOGIQUE SIDEBAR (PILOTAGE XLSX) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    mode_manuel = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if mode_manuel else "no"
    
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN (Scénario)", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
    # Paramètres par défaut
    b6, b7, b8, b10, b11, d8, d9 = "wide-angle lens", "Golden Hour", "calm", "soft tactile textures", "none", MAT_LIST[0], "none"
    i34, i35 = "low-angle ground perspective", "bedtime-friendly soft light"
    saison_ui = "Printemps"

    if mode_manuel:
        st.divider()
        if "DÉCOR" in etape:
            st.subheader("🛠️ RÉGLAGES DÉCOR")
            b5_id = st.selectbox("LIEU PRÉCIS (B5)", [1, 2, 3, 4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'])
            saison_ui = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            b6 = st.selectbox("Angle (B6)", ["wide-angle lens", "macro lens", "fisheye"])
            b7 = st.selectbox("Lumière (B7)", ["Golden Hour", "High Noon", "Sunset", "Blue Hour"])
            b10 = st.text_input("Sol (B10)", value="soft tactile textures")
            b11 = st.selectbox("1er Plan (B11)", ["none", "wild flowers", "puddles", "leaves", "dust motes"])
            d8 = st.selectbox("Matériau 1 (D8)", MAT_LIST)
            d9 = st.selectbox("Matériau 2 (D9)", ["none"] + MAT_LIST)
        else:
            b5_id = auto_b5
    else:
        b5_id = auto_b5

# --- 6. CALCUL FORMULE XLSX (PROMPT 1) ---
b12 = ville['lieux'][b5_id]['cue']
final_light = i35 if e7 == "yes" else b7
final_angle = i34 if e7 == "yes" else b6
fg_string = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "none" else ""
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

# --- 7. ZONE D'AFFICHAGE ---
st.title(f"📍 {ville['nom']} — {ville['lieux'][b5_id]['nom']}")

if "DÉCOR" in etape:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 LIEU (B5)</div><div class="action-text">{ville["lieux"][b5_id]["nom"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🍂 SAISON / SOL</div><div class="action-text">{saison_ui} | {b10}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE ({e7})</div><div class="action-text">{final_light}</div></div>', unsafe_allow_html=True)
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
    export = f"PLAN {p_id} | {ville['nom']}\nDECOR: {ville['lieux'][b5_id]['nom']}\nPROMPT 1: {prompt_1}"
    st.code(export, language="text")
