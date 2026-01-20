import streamlit as st

# --- 1. ADN MÉLO & PIPO (LOCK B22 - VERSION OFFICIELLE) ---
DNA_MELO = """Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. 
Wearing a blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions. Subtle pink translucency inside bunny ears."""

DNA_PIPO = """Microscopic snow-potato companion; white with subtle iridescent multicolor reflections. 
Dot eyes and small smile; not an animal. Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo. Soft constant glow."""

TECHNICAL_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES LIEUX & DÉCORS ---
DESTINATIONS = {
    "eiffel_paris": {
        "nom": "Paris - Tour Eiffel", "struct": "B", "obj_fr": "Béret rouge", "obj_en": "Red beret",
        "decors": {
            1: {"ui": "Le Trocadéro", "en": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette, architectural negative space."},
            2: {"ui": "Les Quais de Seine", "en": "Wet cobblestone banks, soft river ripples, Eiffel Tower blurry in background bokeh."},
            3: {"ui": "Le Pied de la Tour", "en": "Macro view of iron lattice structure, sharp focus on metal textures, low angle perspective."},
            4: {"ui": "Le Champ-de-Mars", "en": "Minimalist green grass field, distant blurry tower, soft golden sunset glow."}
        }
    }
}

# --- 3. LOGIQUE DES 20 PLANS (SÉQUENCES UNIQUES) ---
PLANS_DATA = {}
for i in range(1, 21):
    if i <= 5: ang, light_ui, light_en = "Wide shot", "Aube dorée", "Golden Hour"
    elif i <= 10: ang, light_ui, light_en = "Medium shot", "Coucher du Soleil", "Sunset"
    elif i <= 15: ang, light_ui, light_en = "Close-up", "Heure Bleue", "Blue Hour"
    else: ang, light_ui, light_en = "Wide shot", "Nuit Profonde", "Deep Night"
    
    PLANS_DATA[i] = {
        "angle": ang, "light_ui": light_ui, "light_en": light_en,
        "B_M_FR": f"Plan {i} : Mélo explore le décor avec curiosité.",
        "B_M_EN": f"Action plan {i}: Mélo exploring the environment with calm curiosity, gentle movements."
    }
# Note : Les actions 18 et 20 restent spécifiques
PLANS_DATA[18].update({"B_M_FR": "Énorme bâillement lent", "B_M_EN": "Huge, slow, cinematic yawn, bunny ears twitching slightly"})
PLANS_DATA[20].update({"B_M_FR": "S'endort paisiblement", "B_M_EN": "Deep peaceful sleep, static pose, microscopic Pipo glowing softly nearby"})

# --- 4. STYLE & UI ---
st.set_page_config(page_title="Mélo Studio B22", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.15em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🎬 CONFIGURATION")
    v_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("Numéro du Plan", options=list(PLANS_DATA.keys()))
    
    ville = DESTINATIONS[v_id]
    plan = PLANS_DATA[p_id]
    d_id = (p_id - 1) // 5 + 1
    s_decor = ville['decors'][d_id]
    s_action_fr = plan[f"{ville['struct']}_M_FR"]
    s_action_en = plan[f"{ville['struct']}_M_EN"]

# --- 5. ZONE DE TRAVAIL CONTEXTUELLE ---
st.title(f"📍 {ville['nom']} — Plan {p_id}")

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">📍 DÉCOR ACTUEL</div><div class="action-text">{s_decor["ui"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">🌅 AMBIANCE</div><div class="action-text">{plan["light_ui"]}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Décor (Solid Plate)")
    st.code(f"Environment Plate: {s_decor['en']} {plan['light_en']}. Cinematic photography, vast negative space. --ar 16:9")

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="info-card"><div class="action-title">🎭 ACTION MÉLO</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="info-card"><div class="action-title">👁️ LOOK MÉLO</div><div class="action-text">Bunny Ears | Glass Suit</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><div class="action-title">🎒 ACCESSOIRE</div><div class="action-text">{ville["obj_fr"]}</div></div>', unsafe_allow_html=True)

    st.subheader("Prompt Intégration (Solid B22)")
    p2 = f"Character Integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_action_en}. {plan['angle']}. Decor: {s_decor['en']}. {plan['light_en']}. [LOCKS]: {TECHNICAL_LOCKS}. --ar 16:9"
    st.code(p2)

with tab3:
    st.markdown(f'<div class="info-card"><div class="action-title">🎞️ MOUVEMENT VIDÉO</div><div class="action-text">{s_action_fr}</div></div>', unsafe_allow_html=True)
    
    st.subheader("Prompt Vidéo (Solid Motion)")
    p3 = f"Animation (8s): {s_action_en} in ultra-slow motion. Pipo glows softly (5-10% scale). Glass suit reflections. Perfect loop."
    st.code(p3)
