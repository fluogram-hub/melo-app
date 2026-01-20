import streamlit as st

# --- 1. BIBLE B22 (CONSTANTES) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes, no nose. Body: Transparent blue Glass Suit, ultra-glossy resin finish. Appendages: Long smooth blue ribbons (non-biological)."
PIPO_DNA = "Small spirit companion (15% size), white snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. DONNÉES LIEUX (BASE_LIEUX) ---
LIEUX = {
    "eiffel_paris": {"name": "Paris", "struct": "B", "obj": "Red beret", "animal": "Poodle", "plate": "Empty stone esplanade, vast sky, blurry distant Eiffel Tower silhouette."},
    "mont_saint_michel": {"name": "Mont Saint Michel", "struct": "B", "obj": "Fishing net", "animal": "Sheep", "plate": "Vast wet sand, mirror reflections, distant blurry island silhouette."},
    "santorini_greece": {"name": "Santorin", "struct": "A", "obj": "Wood flute", "animal": "White cat", "plate": "Simple white curved wall, dark sea, blurry blue dome."},
    "venice_italy": {"name": "Venise", "struct": "C", "obj": "Cat mask", "animal": "White pigeon", "plate": "Dark calm water, soft ripples, blurry distant palaces."},
    "fuji_japan": {"name": "Mont Fuji", "struct": "A", "obj": "Paper fan", "animal": "Snow monkey", "plate": "Still water, vast sky, distant blurry triangular mountain silhouette."},
    "taj_mahal_india": {"name": "Taj Mahal", "struct": "A", "obj": "Oil lantern", "animal": "Blue peacock", "plate": "Symmetrical white marble, reflecting pool, warm dusk glow."},
    "lapland_arctic": {"name": "Laponie", "struct": "A", "obj": "Steaming mug", "animal": "Reindeer", "plate": "Vast white snowfield, simple snowy pine silhouettes, aurora glow."}
}

# --- 3. LES 20 PLANS COMPLETS (PLAN_DE_REALISATION) ---
PLANS = {
    "1": {"angle": "Wide", "light": "Golden Hour", "A_M": "Arrival (grey/misty landscape)", "A_P": "Floats next to Melo", "B_M": "Arrival (Melo looks for Pipo)", "B_P": "Hides nearby", "C_M": "Departure (Melo on transport)", "C_P": "At the front acting as a guide"},
    "2": {"angle": "Medium", "light": "Golden Hour", "A_M": "Rubs eyes, looking for color", "A_P": "Peeks playfully", "B_M": "Rubs eyes, searching", "B_P": "Peeks from behind a corner", "C_M": "Looks ahead, steady", "C_P": "Guides gently"},
    "3": {"angle": "Close-up", "light": "Sunset", "A_M": "Watches Pipo glow", "A_P": "Glows softly, ready to help", "B_M": "Walks on tiptoes, curious", "B_P": "Teases at a distance", "C_M": "Landscape drifts behind Melo", "C_P": "Hovers as a guide"},
    "4": {"angle": "POV/Detail", "light": "Sunset", "A_M": "Looks at a small detail", "A_P": "Touches the detail (magic)", "B_M": "Sees a clue in the decor", "B_P": "Pops out from the decor", "C_M": "Follows a light cue", "C_P": "Creates gentle light trails"},
    "5": {"angle": "Medium", "light": "Sunset", "A_M": "Smiles, reaching for light", "A_P": "Offers a soft glow", "B_M": "Laughs, trying to catch Pipo", "B_P": "Dodges playfully", "C_M": "Drags paw through air/water", "C_P": "Leaves a soft ribbon trail"},
    "8": {"angle": "Medium", "light": "Dusk", "A_M": "Uses the local {obj}", "A_P": "Reacts, hovering close", "B_M": "Uses the local {obj}", "B_P": "Circles the object", "C_M": "Plays with the local {obj}", "C_P": "Orbits calmly"},
    "10": {"angle": "Close-up", "light": "Blue Hour", "A_M": "Face in awe, lit by color", "A_P": "Glows near Melo", "B_M": "Looks amazed, then calmer", "B_P": "Levitates a small item", "C_M": "Eyelids getting heavy", "C_P": "Lowers its glow"},
    "13": {"angle": "Close-up", "light": "Night", "A_M": "Notices a small animal ({animal}) asleep", "A_P": "Stays quiet and dim", "B_M": "Notices a small animal ({animal}) asleep", "B_P": "Stays quiet and dim", "C_M": "Notices a small animal ({animal}) asleep", "C_P": "Stays quiet and dim"},
    "18": {"angle": "Close-up", "light": "Night", "A_M": "Makes a huge, slow yawn", "A_P": "Stays very close", "B_M": "Makes a huge, slow yawn", "B_P": "Stays very close", "C_M": "Makes a huge, slow yawn", "C_P": "Stays very close"},
    "20": {"angle": "Wide", "light": "Night", "A_M": "Sleep / fade to black", "A_P": "Dims to near-off", "B_M": "Sleep / fade to black", "B_P": "Dims to near-off", "C_M": "Sleep / fade to black", "C_P": "Dims to near-off"}
}

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo Master Director", layout="wide")
st.title("🎬 Mélo & Pipo : Direction d'Acteurs")

with st.sidebar:
    st.header("📍 Plateau de tournage")
    l_id = st.selectbox("Lieu", list(LIEUX.keys()), format_func=lambda x: LIEUX[x]['name'])
    p_id = st.select_slider("Séquence (Plan)", options=list(PLANS.keys()))
    
    st.header("☁️ Ambiance")
    meteo = st.selectbox("Météo", ["Clear Sky", "Heavy Rain", "Soft Snow", "Misty"])

# Logique de récupération
lieu = LIEUX[l_id]
plan = PLANS[p_id]
s = lieu['struct']
melo_act = plan[f"{s}_M"].format(obj=lieu['obj'], animal=lieu['animal'])
pipo_act = plan[f"{s}_P"]

# --- 5. TABLEAU DE BORD ---
st.subheader(f"Plan {p_id} : {lieu['name']} (Structure {s})")

# Affichage des actions pour l'utilisateur
c1, c2 = st.columns(2)
with c1:
    st.metric("Action de MÉLO", melo_act)
with c2:
    st.metric("Action de PIPO", pipo_act)

st.divider()

# --- 6. PROMPTS ---
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.write("**1. Le Fond (Plate)**")
    p1 = f"Environment: {lieu['plate']} {plan['light']}, {meteo}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1)

with col_b:
    st.write("**2. Les Acteurs (Image)**")
    p2 = f"Character Integration: {MELO_DNA} and {PIPO_DNA}. Melo is {melo_act}. Pipo is {pipo_act}. {plan['angle']}. {plan['light']}. [VERROUS]: {VERROUS}. --ar 16:9"
    st.code(p2)

with col_c:
    st.write("**3. Le Mouvement (Vidéo)**")
    p3 = f"Animation (8s): Melo {melo_act} and Pipo {pipo_act}. Ultra-slow motion. Inertia on Melo's ribbons. Soft light trails. Cinematic PBR."
    st.code(p3)

st.info(f"💡 **Note de mise en scène :** Dans ce plan, l'angle est un **{plan['angle']}**. Mélo interagit avec l'élément local : **{lieu['obj']}**.")
