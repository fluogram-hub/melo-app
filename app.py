import streamlit as st

# --- 1. BIBLE B22 : VERROUS DE MATÉRIAUX & ÉNERGIE (ANGLAIS) ---
DNA_MELO = """Bunny-shaped high-end designer toy. Wearing a blue glass suit (transparent blue glass effect), ultra-glossy resin finish. 
White round belly with yellow notes, white mitten-like paws. Rounded child proportions. Subtle pink translucency inside bunny ears."""

MATERIAL_MAIN = "Homogeneous transparent blue jelly/glass, no internal anatomy, high light refraction (IOR 1.5), realistic caustics, micro-reflections."

DNA_PIPO = "Microscopic snow-potato companion (5-10% scale). Dot eyes and small smile."
PIPO_COLOR = "Solid white base with subtle iridescent multicolor pearl reflections (opalescent)."
PIPO_ENERGY_TRAIL = "Soft constant glow, minimal bedtime-friendly energy trail, no flickering, ethereal light ribbon."

TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES : DÉCORS & PLANS ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
            2: {"ui": "Les Quais de Seine", "en": "Wet cobblestone banks, soft river ripples, Eiffel Tower behind."},
            3: {"ui": "Le Pied de la Tour", "en": "Macro view of iron lattice structure, low angle perspective."},
            4: {"ui": "Le Champ-de-Mars", "en": "Minimalist green grass field, distant blurry tower."}
        }
    }
}

PLANS_DATA = {i: {"angle": "Medium shot", "light_ui": "Aube", "light_en": "Golden Hour", "B_M_FR": f"Action Plan {i}", "B_M_EN": f"Action {i}"} for i in range(1, 21)}
PLANS_DATA[18].update({"B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge, slow, cinematic yawn"})
PLANS_DATA[20].update({"B_M_FR": "S'endort paisiblement", "B_M_EN": "Deep peaceful sleep"})

# --- 3. STYLE & INTERFACE ---
st.set_page_config(page_title="Mélo Studio B22 Full", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🎬 CONFIGURATION")
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    decor = ville['decors'][(p_id - 1) // 5 + 1]

# --- 4. ZONE DE TRAVAIL CONTEXTUELLE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR</div><div class="action-text">{decor["ui"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{plan["light_ui"]}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Décor")
    st.code(f"Environment Plate: {decor['en']} {plan['light_en']}. Cinematic photography. --ar 16:9")

with tab2:
    # AFFICHAGE DES PARAMÈTRES TECHNIQUES B22
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">💎 MATIÈRE MÉLO</div><div class="action-text">Glass Suit (IOR 1.5)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">✨ COULEUR PIPO</div><div class="action-text">Iridescent Pearl</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><div class="action-title">🎒 ACCESSOIRE</div><div class="action-text">{ville["obj_fr"]}</div></div>', unsafe_allow_html=True)

    st.subheader("Prompt Intégration (B22 Full Specs)")
    p2 = f"Character Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Material Specs: {MATERIAL_MAIN}. Pipo Specs: {PIPO_COLOR}. Pose: {plan['B_M_EN']}. Decor: {decor['en']}. [LOCKS]: {TECHNICAL_LOCKS}. --ar 16:9"
    st.code(p2)

with tab3:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ ÉNERGIE & TRAINÉE</div><div class="action-text">Energy Trail : {PIPO_ENERGY_TRAIL}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Vidéo (Mouvement & Fluides)")
    p3 = f"Animation (8s): {plan['B_M_EN']} in ultra-slow motion. Pipo leaves {PIPO_ENERGY_TRAIL}. Realistic glass caustics on surroundings. Perfect loop."
    st.code(p3)
