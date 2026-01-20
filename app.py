import streamlit as st

# --- 1. ADN & LOCKS B22 (ANGLAIS POUR L'IA) ---
DNA_MELO = "Bunny-shaped high-end designer toy. Blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile. Iridescent multicolor reflections. Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_B22 = "Homogeneous transparent blue glass, no internal anatomy, high IOR 1.5, caustics, micro-reflections."

# --- 2. BIBLIOTHÈQUE DE MATÉRIAUX DÉCOR (AL2:AL400 - CLASSÉ PAR CATÉGORIES) ---
MAT_MAP = {
    "🍭 SUCRERIES": {
        "Gelée translucide (glossy)": "Translucent jelly candy (glossy), subsurface scattering",
        "Bonbon coloré (glossy)": "Translucent colored jelly candy (glossy), vibrant syrup tones",
        "Sucre d'orge poli": "Hard candy (polished smooth), light refraction",
        "Guimauve (matte soft)": "Marshmallow foam (matte soft), squishy appearance",
        "Pâte à sucre (fondant)": "Fondant sugar paste (matte), smooth powdery finish",
        "Cire de miel": "Honey wax (warm glow), semi-translucent gold",
        "Chocolat marbré": "Chocolate tri-blend (white, milk, dark – soft marble effect)",
        "Velours de chocolat blanc": "White chocolate velvet, fine cocoa butter texture",
        "Mousse crémeuse": "Creamy foam texture, light airy bubbles",
        "Génoise éponge": "Sponge cake texture, porous and soft looking"
    },
    "🧶 TEXTILES & MOUSSES": {
        "Laine feutrée": "Felted wool fabric, organic soft fibers",
        "Coton matelassé": "Cotton quilted padding, soft cushions, fabric seams",
        "Micro-velours": "Velvet microfabric, light-absorbing soft pile",
        "Nuage de coton": "Cotton fiber cloud, wispy and ethereal",
        "Éponge à mémoire de forme": "Memory foam sponge, slow-reacting density",
        "Éponge poreuse": "Soft porous sponge, visible foam cells"
    },
    "📜 PAPIER & BOIS": {
        "Papier fait main (grain)": "Handmade paper (soft grain), raw organic edges",
        "Papier mâché (lisse)": "Paper mâché (smooth), hardened pulp texture",
        "Origami multicouche": "Origami layered paper, sharp geometric folds",
        "Bouleau clair": "Light birch wood (soft grain), natural pale wood",
        "Bois de jouet (bords ronds)": "Toy wood (rounded edges), smooth lacquered finish",
        "Bois peint (pastel)": "Milk-painted wood (pastel), matte chalky wood finish"
    },
    "🧩 JOUETS & ARGILE": {
        "Argile souple (matte)": "Soft clay (matte), hand-molded look",
        "Porcelaine soyeuse": "Porcelain clay (silky matte), high-end ceramic",
        "LEGO (Plastique ABS)": "Lego plastic ABS, high gloss, modular brick surface",
        "Béret de Paris (Texture)": "Wool felt texture, red dye, soft fibers"
    },
    "🌍 ENVIRONNEMENT PBR": {
        "Roche Basalte": "Raw basalt rock textures, micro-displacement",
        "Eau & Reflets": "Calm water surface, ray-traced reflections, IOR 1.33",
        "Glace Cristalline": "Frosted crystalline blue ice, subsurface scattering"
    }
}

# --- 3. DONNÉES DE BASE (LIEUX & PLANS) ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris (France)", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "decors": {1: "Trocadéro", 2: "Quais de Seine", 3: "Pied de la Tour", 4: "Champ-de-Mars"}},
    "venice_italy": {"nom": "Venise (Italie)", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "decors": {1: "Grand Canal", 2: "Pont des Soupirs", 3: "Place St-Marc", 4: "Gondole"}}
}

PLANS_DATA = {i: {"angle": "Plan Moyen", "light": "Golden Hour", "B_M": f"Action Plan {i}"} for i in range(1, 21)}

# --- 4. STYLE & NAVIGATION ---
st.set_page_config(page_title="Melo Director V22", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

etape = st.radio("ÉTAPE DE TRAVAIL :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (MÉLO & PIPO)", "🎞️ 3. VIDÉO (MOUVEMENT)"], horizontal=True)
st.divider()

# --- 5. INITIALISATION (SÉCURITÉ ANTI-NAMEERROR) ---
v_id = "eiffel_paris"
ville = DESTINATIONS[v_id]
p_id = 1
plan = PLANS_DATA[p_id]
s_decor_ui = ville['decors'][1]
s_light_ui, s_light_en = "Aube", "Golden Hour"
s_mat_decor_en = "Translucent jelly candy (glossy)"
s_angle_ui, s_angle_en = "Plan Moyen", "Medium shot"
s_action_fr = plan["B_M"]
s_paws_fr, s_paws_en = "Détendu", "relaxed"
s_expr_fr, s_expr_en = "Curiosité", "curious"
s_pipo_pose_en, s_pipo_pos_en = "softly floating", "near head"
s_pipo_col_en, s_palette_en = "Iridescent Pearl", "Natural"
s_energy_en = "soft glow"
s_acc_fr = ville['obj_fr']

# --- 6. LOGIQUE BARRE LATÉRALE (DYNAMIQUE) ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("MODE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    auto_d_id = (p_id - 1) // 5 + 1

    if mode == "🕹️ MANUEL":
        st.divider()
        if "DÉCOR" in etape:
            st.subheader("🛠️ CONFIG DÉCOR")
            s_decor_ui = st.selectbox("Lieu", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x])
            s_decor_ui = ville['decors'][s_decor_ui]
            cat_mat = st.selectbox("Catégorie de Matière", list(MAT_MAP.keys()))
            s_mat_ui = st.selectbox("Matière spécifique", list(MAT_MAP[cat_mat].keys()))
            s_mat_decor_en = MAT_MAP[cat_mat][s_mat_ui]
            s_angle_ui = st.selectbox("Angle", ["Plan Large", "Plan Moyen", "Gros Plan"])
            s_light_ui = st.selectbox("Horaire", ["Aube", "Midi", "Crépuscule", "Nuit"])
            s_light_en = "Golden Hour" if s_light_ui == "Aube" else "Deep Night"

        elif "IMAGE" in etape:
            st.subheader("🛠️ CONFIG MÉLO & PIPO")
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés", "Assis"])
            s_paws_en = "relaxed" if s_paws_fr == "Détendu" else "one paw raised"
            s_expr_fr = st.selectbox("Expression Mélo", ["Curiosité", "Émerveillement", "Sourire"])
            s_pipo_pose = st.selectbox("Pose Pipo", ["Flottement doux", "Orbital", "Statique"])
            s_pipo_pos = st.selectbox("Position Pipo", ["À côté de la tête", "Sur l'épaule", "Devant le torse"])
            s_acc_fr = st.text_input("Accessoire Mélo", value=ville['obj_fr'])
            s_palette_en = st.selectbox("Palette", ["Natural", "Pastel", "High Contrast"])
            s_pipo_col_en = st.selectbox("Couleur Pipo", ["Iridescent Pearl", "Pure White", "Pearl Multi"])
            s_energy_en = st.selectbox("Énergie Pipo", ["Soft glow", "Ribbon trail", "Sparkles"])

        elif "VIDÉO" in etape:
            st.subheader("🛠️ CONFIG MOUVEMENT")
            s_action_fr = st.text_input("Mouvement (FR)", value=plan["B_M"])
            s_energy_ui = st.selectbox("Trainée d'énergie", ["Douce", "Moyenne", "Forte"])
            s_speed = st.selectbox("Vitesse", ["Ultra-Slow", "Slow-Motion"])

# --- 7. AFFICHAGE FINAL ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")



if "DÉCOR" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE / HEURE</div><div class="action-text">{s_angle_ui} | {s_light_ui}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🍭 MATIÈRE</div><div class="action-text">{s_mat_decor_en[:25]}...</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Master Plate (FOND)")
    st.code(f"Environment: {s_decor_ui}. Material: {s_mat_decor_en}. Lighting: {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 MÉLO</div><div class="action-text">{s_paws_fr} | {s_expr_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🎒 ACCESSOIRE</div><div class="action-text">{s_acc_fr}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_col_en}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Intégration (MÉLO & PIPO)")
    st.code(f"Integration: MÉLO ({DNA_MELO}). Material: {MATERIAL_B22}. PIPO ({DNA_PIPO}). Pose: {s_paws_en}. Palette: {s_palette_en}. Pipo: {s_pipo_col_en}. {TECH_LOCKS} --ar 16:9")

elif "VIDÉO" in etape:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Animation (VÉO 3)")
    st.code(f"Animation (8s): {s_action_fr} in ultra-slow motion. Pipo trail: {s_energy_en}. Perfect loop.")
