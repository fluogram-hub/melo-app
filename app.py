import streamlit as st

# --- 1. BIBLE B22 : DNA & LOCKS (ANGLAIS POUR L'IA) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."
TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."
MATERIAL_MAIN = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."

# --- 2. TRADUCTEURS TECHNIQUES ---
FG_MAP = {
    "Aucun": "clear ground with minimal dust",
    "Fleurs sauvages": "highly detailed PBR wild flowers with subsurface scattering, shallow depth of field",
    "Feuilles mortes": "scattered crisp PBR autumn leaves, detailed vein textures, dry and crunchy look",
    "Flaques d'eau": "realistic water puddles with ray-traced reflections and wet mud shader",
    "Cailloux PBR": "highly detailed PBR pebbles and stones with wet shader, micro-surface roughness"
}

# --- 3. LES 20 DESTINATIONS (BASE COMPLÈTE) ---
DESTINATIONS = {
    "eiffel_paris": {"nom": "Paris (France)", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret", "animal_en": "Poodle", "decors": {1: "Trocadéro", 2: "Quais de Seine", 3: "Pied de la Tour", 4: "Champ-de-Mars"}},
    "mont_saint_michel": {"nom": "Mont St-Michel (France)", "struct": "B", "obj_fr": "Filet de pêche", "obj_en": "Fishing net", "animal_en": "Sheep", "decors": {1: "Baie sableuse", 2: "Remparts", 3: "Abbaye", 4: "Ruelle médiévale"}},
    "santorini_greece": {"nom": "Santorin (Grèce)", "struct": "A", "obj_fr": "Flûte en bois", "obj_en": "Wood flute", "animal_en": "White cat", "decors": {1: "Murs blancs", 2: "Dôme bleu", 3: "Escaliers vue mer", 4: "Terrasse coucher soleil"}},
    "venice_italy": {"nom": "Venise (Italie)", "struct": "C", "obj_fr": "Masque de chat", "obj_en": "Cat mask", "animal_en": "White pigeon", "decors": {1: "Grand Canal", 2: "Pont des Soupirs", 3: "Place St-Marc", 4: "Gondole"}},
    "fuji_japan": {"nom": "Mont Fuji (Japon)", "struct": "A", "obj_fr": "Éventail", "obj_en": "Paper fan", "animal_en": "Snow monkey", "decors": {1: "Lac Kawaguchi", "2": "Pagode Chureito", 3: "Cerisiers", 4: "Forêt Aokigahara"}},
    "taj_mahal_india": {"nom": "Taj Mahal (Inde)", "struct": "A", "obj_fr": "Lanterne", "obj_en": "Oil lantern", "animal_en": "Peacock", "decors": {1: "Bassin miroir", 2: "Jardin", 3: "Porte principale", 4: "Bord de rivière"}},
    "giza_egypt": {"nom": "Gizeh (Égypte)", "struct": "A", "obj_fr": "Boussole", "obj_en": "Compass", "animal_en": "Fennec", "decors": {1: "Dunes", 2: "Pied Pyramide", 3: "Sphinx", 4: "Village désertique"}},
    "petra_jordan": {"nom": "Petra (Jordanie)", "struct": "A", "obj_fr": "Carnet", "obj_en": "Sketchbook", "animal_en": "Camel", "decors": {1: "Le Siq", 2: "Le Trésor", 3: "Haut lieu sacrifice", 4: "Grottes"}},
    "lapland_arctic": {"nom": "Laponie (Arctique)", "struct": "A", "obj_fr": "Chocolat chaud", "obj_en": "Hot cocoa", "animal_en": "Reindeer", "decors": {1: "Forêt enneigée", 2: "Igloo", 3: "Traîneau", 4: "Aurores boréales"}},
    "ny_times_square": {"nom": "New York (USA)", "struct": "B", "obj_fr": "Hot-dog", "obj_en": "Hot dog", "animal_en": "Squirrel", "decors": {1: "Times Square", 2: "Central Park", 3: "Brooklyn Bridge", 4: "Subway"}},
    "great_wall_china": {"nom": "Grande Muraille (Chine)", "struct": "B", "obj_fr": "Cerf-volant", "obj_en": "Kite", "animal_en": "Panda", "decors": {1: "Tour de guet", 2: "Crête montagneuse", 3: "Escaliers infinis", 4: "Brouillard matinal"}},
    "machu_picchu": {"nom": "Machu Picchu (Pérou)", "struct": "A", "obj_fr": "Poncho", "obj_en": "Poncho", "animal_en": "Llama", "decors": {1: "Terrasses", 2: "Temple du Soleil", 3: "Sommet Huayna", 4: "Porte du Soleil"}},
    "bali_ubud": {"nom": "Bali (Indonésie)", "struct": "B", "obj_fr": "Offrande", "obj_en": "Offering", "animal_en": "Monkey", "decors": {1: "Rizières Tegalalang", 2: "Temple de l'eau", 3: "Forêt des singes", 4: "Cascade"}},
    "safari_kenya": {"nom": "Masai Mara (Kenya)", "struct": "C", "obj_fr": "Jumelles", "obj_en": "Binoculars", "animal_en": "Lion", "decors": {1: "Savane", 2: "Acacia solitaire", 3: "Rivière Mara", 4: "Campement"}},
    "london_big_ben": {"nom": "Londres (UK)", "struct": "B", "obj_fr": "Parapluie", "obj_en": "Umbrella", "animal_en": "Fox", "decors": {1: "Big Ben", 2: "Tower Bridge", 3: "Cabine rouge", 4: "Parc Royal"}},
    "rio_christ": {"nom": "Rio (Brésil)", "struct": "A", "obj_fr": "Ballon", "obj_en": "Football", "animal_en": "Toucan", "decors": {1: "Corcovado", 2: "Copacabana", 3: "Pain de Sucre", 4: "Escaliers Selaron"}},
    "kyoto_fushimi": {"nom": "Kyoto (Japon)", "struct": "B", "obj_fr": "Ombrelle", "obj_en": "Umbrella", "animal_en": "Deer", "decors": {1: "Portails Torii", 2: "Forêt Bambous", 3: "Temple d'Or", 4: "Ruelle Gion"}},
    "sydney_opera": {"nom": "Sydney (Australie)", "struct": "C", "obj_fr": "Planche surf", "obj_en": "Surfboard", "animal_en": "Koala", "decors": {1: "Opéra", 2: "Harbour Bridge", 3: "Bondi Beach", 4: "Ferry"}},
    "moscow_red_square": {"nom": "Moscou (Russie)", "struct": "A", "obj_fr": "Matriochka", "obj_en": "Matryoshka", "animal_en": "Brown bear", "decors": {1: "Place Rouge", 2: "St Basile", 3: "Kremlin", 4: "Métro"}},
    "antelope_canyon": {"nom": "Antelope Canyon (USA)", "struct": "A", "obj_fr": "Plume", "obj_en": "Feather", "animal_en": "Coyote", "decors": {1: "Slot Canyon", 2: "Rayon lumineux", 3: "Vagues de roche", 4: "Entrée étroite"}}
}

# --- 4. LOGIQUE DES 20 PLANS ---
PLANS_DATA = {i: {"angle": "Medium", "light_ui": "Aube", "light_en": "Golden Hour", "A": f"Contemplation {i}", "B": f"Exploration {i}", "C": f"Mouvement {i}"} for i in range(1, 21)}
PLANS_DATA[1].update({"light_ui": "Aube", "light_en": "Golden Hour", "A": "Arrivée brumeuse", "B": "Arrivée curieuse", "C": "Départ transport"})
PLANS_DATA[18].update({"light_ui": "Nuit", "light_en": "Deep Night", "A": "Bâillement lent", "B": "Bâillement lent", "C": "Bâillement lent"})
PLANS_DATA[20].update({"light_ui": "Nuit", "light_en": "Deep Night", "A": "Sommeil", "B": "Sommeil", "C": "Sommeil"})

# --- 5. STYLE & UI ---
st.set_page_config(page_title="Melo Production Master", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    .stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# SÉLECTEUR D'ÉTAPE (Onglets simulés)
etape = st.radio("ÉTAPE ACTUELLE :", ["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"], horizontal=True)
st.divider()

# --- 6. INITIALISATION SIDEBAR ---
with st.sidebar:
    st.title("🎬 PILOTAGE")
    mode = st.radio("CONTRÔLE", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    v_id = st.selectbox("DESTINATION", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    auto_d_id = (p_id - 1) // 5 + 1
    
    # Valeurs par défaut
    s_decor_ui = ville['decors'][auto_d_id]
    s_light_ui, s_light_en = plan['light_ui'], plan['light_en']
    s_season_fr, s_season_en = "Printemps", "Spring"
    s_fg_fr, s_fg_en = "Aucun", FG_MAP["Aucun"]
    s_action_fr = plan[ville['struct']]
    s_paws_fr, s_paws_en = "Détendu", "relaxed"
    s_expr_fr, s_expr_en = "Curiosité", "calm curiosity"
    s_pipo_col = "Blanc Nacré"
    s_energy = "Douce"

    if mode == "🕹️ MANUEL":
        st.divider()
        st.subheader(f"🛠️ RÉGLAGES {etape.split('.')[1]}")
        if "DÉCOR" in etape:
            m_d_id = st.selectbox("Lieu précis", [1,2,3,4], index=auto_d_id-1, format_func=lambda x: ville['decors'][x])
            s_decor_ui = ville['decors'][m_d_id]
            s_season_fr = st.selectbox("Saison", ["Printemps", "Été", "Automne", "Hiver"])
            s_fg_fr = st.selectbox("Premier Plan", list(FG_MAP.keys()))
            s_fg_en = FG_MAP[s_fg_fr]
        elif "IMAGE" in etape:
            s_paws_fr = st.selectbox("Pose Mélo", ["Détendu", "Patte levée", "Bras croisés"])
            s_expr_fr = st.selectbox("Expression", ["Curiosité", "Sourire", "Sommeil"])
            s_palette = st.selectbox("Palette", ["Naturelle", "Contrastée", "Pastel"])
            s_pipo_col = st.selectbox("Couleur Pipo", ["Blanc Nacré", "Irisé"])
        elif "VIDÉO" in etape:
            s_action_fr = st.text_input("Mouvement", value=plan[ville['struct']])
            s_energy = st.selectbox("Traînée Pipo", ["Douce", "Ruban", "Scintillante"])

# --- 7. ZONE D'AFFICHAGE CONTEXTUELLE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

if "DÉCOR" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{s_decor_ui}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🍂 SAISON</div><div class="action-text">{s_season_fr}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌿 PREMIER PLAN</div><div class="action-text">{s_fg_fr}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Décor (Anglais)")
    st.code(f"Environment Plate: {ville['nom']}, {s_decor_ui}. Season: {s_season_fr}. Foreground: {s_fg_en}. Time: {s_light_en}. --ar 16:9")

elif "IMAGE" in etape:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎭 POSE MÉLO</div><div class="action-text">{s_paws_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">✨ PIPO</div><div class="action-text">{s_pipo_col}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🎒 OBJET</div><div class="action-text">{ville["obj_fr"]}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Intégration (Anglais)")
    st.code(f"Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_paws_fr}. In: {s_decor_ui}. Material: {MATERIAL_MAIN}. [LOCKS]: {TECHNICAL_LOCKS}. --ar 16:9")

elif "VIDÉO" in etape:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">🚀 ÉNERGIE</div><div class="action-text">{s_energy}</div></div>', unsafe_allow_html=True)
    st.subheader("Prompt Vidéo (Anglais)")
    st.code(f"Animation (8s): {s_action_fr} in ultra-slow motion. Pipo energy: {s_energy}. Perfect loop.")

# --- 8. EXPORT ---
st.divider()
if st.button("💾 EXPORTER TOUS LES PROMPTS DU PLAN"):
    export = f"PLAN {p_id} - {ville['nom']}\n1. Decor: {s_decor_ui}\n2. Action: {s_action_fr}\n3. DNA: {DNA_MELO}"
    st.code(export, language="text")
