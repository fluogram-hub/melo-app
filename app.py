import streamlit as st

# --- 1. ADN MÉLO & PIPO (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES COMPLÈTE (Extraite de ton Excel) ---
LIEUX_DATA = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
    "mont_saint_michel": {"name": "Mont Saint Michel", "struct": "B", "obj": "Fishing net", "animal": "Sheep", "plate": "Vast wet sand, mirror reflections, distant blurry island silhouette."},
    "santorini_greece": {"name": "Santorin", "struct": "A", "obj": "Wood flute", "animal": "White cat", "plate": "Simple white curved wall, dark sea, one distant blurry blue dome."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark water, soft ripples, blurry silhouettes of distant palaces."},
    "fuji_japan": {"name": "Mont Fuji", "struct": "A", "obj": "Paper fan", "animal": "Snow monkey", "plate": "Still water, vast sky, distant blurry triangular mountain silhouette."},
    "taj_mahal_india": {"name": "Taj Mahal", "struct": "A", "obj": "Oil lantern", "animal": "Blue peacock", "plate": "Long still water strip, symmetry, distant white dome in mist."},
    "giza_pyramids_egypt": {"name": "Pyramides", "struct": "A", "obj": "Golden compass", "animal": "Fennec fox", "plate": "Vast sand dunes, minimalist horizon, distant blurry pyramid."},
    "petra_jordan": {"name": "Petra", "struct": "A", "obj": "Sketchbook", "animal": "Camel", "plate": "Narrow red rock corridor, sliver of starry sky, deep shadows."},
    "lapland_arctic": {"name": "Laponie", "struct": "A", "obj": "Steaming mug", "animal": "Reindeer", "plate": "Vast white snowfield, pine silhouettes, aurora glow."}
}

PLANS_DATA = {
    1: {"angle": "Wide", "light": "Golden Hour", "A_M": "Arrival", "A_P": "Floats next to Melo", "B_M": "Arrival (looks for Pipo)", "B_P": "Hides nearby", "C_M": "Departure on transport", "C_P": "At the front as a guide"},
    2: {"angle": "Medium", "light": "Golden Hour", "A_M": "Melo rubs eyes", "A_P": "Pipo peeks playfully", "B_M": "Melo rubs eyes, searching", "B_P": "Pipo peeks from corner", "C_M": "Melo looks ahead", "C_P": "Pipo guides gently"},
    3: {"angle": "Close-up", "light": "Sunset", "A_M": "Pipo glows softly", "A_P": "Melo watches Pipo", "B_M": "Melo walks on tiptoes", "B_P": "Pipo teases", "C_M": "Landscape drifts", "C_P": "Pipo hovers"},
    5: {"angle": "Medium", "light": "Sunset", "A_M": "Melo smiles, reaching", "A_P": "Pipo offers glow", "B_M": "Melo laughs", "B_P": "Pipo dodges", "C_M": "Melo drags paw in water", "C_P": "Pipo leaves ribbon trail"},
    8: {"angle": "Medium", "light": "Dusk", "A_M": "Uses {obj}", "A_P": "Pipo reacts", "B_M": "Uses {obj}", "B_P": "Pipo circles", "C_M": "Plays with {obj}", "C_P": "Pipo orbits"},
    10: {"angle": "Close-up", "light": "Blue Hour", "A_M": "Face in awe", "A_P": "Pipo glows near", "B_M": "Amazed, then calmer", "B_P": "Pipo levitates item", "C_M": "Eyelids heavy", "C_P": "Pipo lowers glow"},
    13: {"angle": "Close-up", "light": "Night", "A_M": "Notices animal ({animal})", "A_P": "Animal sleeps", "B_M": "Notices animal ({animal})", "B_P": "Animal sleeps", "C_M": "Notices animal ({animal})", "C_P": "Animal sleeps"},
    18: {"angle": "Close-up", "light": "Night", "A_M": "Huge slow yawn", "A_P": "Pipo stays close", "B_M": "Huge slow yawn", "B_P": "Pipo stays close", "C_M": "Huge slow yawn", "C_P": "Pipo stays close"},
    20: {"angle": "Wide", "light": "Night", "A_M": "Sleep", "A_P": "Pipo dims", "B_M": "Sleep", "B_P": "Pipo dims", "C_M": "Sleep", "C_P": "Pipo dims"}
}

# --- 3. INTERFACE ---
st.set_page_config(page_title="Mélo Studio", layout="wide")
st.title("🎬 Studio Mélo : Production 160s")

with st.sidebar:
    st.header("🎯 Pilotage")
    mode = st.radio("Contrôle", ["🤖 AUTOMATIQUE", "🕹️ MANUEL"])
    lieu_id = st.selectbox("Lieu", list(LIEUX_DATA.keys()), format_func=lambda x: LIEUX_DATA[x]['name'])
    plan_id = st.select_slider("Plan de Scénario", options=list(PLANS_DATA.keys()))
    
    st.divider()
    
    # Logique de sélection
    lieu = LIEUX_DATA[lieu_id]
    plan = PLANS_DATA[plan_id]
    s = lieu['struct']
    
    if mode == "🤖 AUTOMATIQUE":
        s_light, s_weather = plan["light"], "Clear Sky"
        s_expr, s_gaze, s_paws = "Curiosité", "Vers l'horizon", "Détendu"
        s_melo_act = plan[f"{s}_M"].format(obj=lieu['obj'], animal=lieu['animal'])
        s_pipo_act = plan[f"{s}_P"]
        s_acc = lieu["obj"]
        st.success(f"Mode Auto : Plan {plan_id} chargé.")
    else:
        st.warning("Mode Manuel Activé")
        s_light = st.selectbox("Lumière", ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"])
        s_weather = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])
        s_expr = st.selectbox("Expression", ["Émerveillement", "Sourire", "Somnolence"])
        s_gaze = st.selectbox("Regard", ["Droit devant", "Vers Pipo", "Vers l'horizon"])
        s_paws = st.selectbox("Pattes", ["Détendu", "Patte levée", "Bras croisés", "Derrière le dos"])
        s_acc = st.text_input("Accessoire", value=lieu['obj'])
        s_melo_act = st.text_input("Action Vidéo Mélo", value="Respiration lente")
        s_pipo_act = "Flotte doucement"

# --- 4. AFFICHAGE (LISIBILITÉ MAXIMALE) ---
st.markdown(f"### 📍 {lieu['name']} — Plan {plan_id} ({plan['angle']})")

# Dashboard clair
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"**Action MÉLO**\n\n{s_melo_act}")
with c2:
    st.info(f"**Action PIPO**\n\n{s_pipo_act}")
with c3:
    st.info(f"**Ambiance**\n\n{s_light} | {s_weather}")

st.divider()

# Prompts dans des onglets larges
t1, t2, t3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with t1:
    p1 = f"Environment: {lieu['plate']} {s_light}, {s_weather}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with t2:
    m_anatomy = f"Pose: {s_paws}. Gaze: {s_gaze}. Expression: {s_expr}. Accessory: {s_acc}."
    p2 = f"Integration: {MELO_DNA}. {m_anatomy} Action: {s_melo_act}. Companion: {PIPO_DNA} doing {s_pipo_act}. {s_light}. {VERROUS}. --ar 16:9"
    st.code(p2, language="text")

with t3:
    p3 = f"Animation (8s): Melo {s_melo_act} and Pipo {s_pipo_act}. Ultra-slow motion. {s_weather} effects. Perfect loop, cinematic PBR."
    st.code(p3, language="text")

st.markdown(f"**Note Technique :** Structure **{s}** détectée pour ce lieu. L'action de Mélo a été ajustée en conséquence.")
