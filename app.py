import streamlit as st

# --- 1. ADN MÉLO & PIPO (BIBLE B22) ---
MELO_DNA = "45cm luxury designer toy, humanoid, round head, black dot eyes. Body: Transparent blue Glass Suit, ultra-glossy finish. Appendages: Long smooth blue ribbons."
PIPO_DNA = "Small white spirit companion, snow-potato shape, iridescent soft glow."
VERROUS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, ray-traced reflections."

# --- 2. BASE DE DONNÉES DES LIEUX & DÉCORS (Extraite de tes fichiers) ---
DESTINATIONS = {
    "eiffel_paris": {
        "name": "Paris", "struct": "B", "obj": "Béret rouge", "animal": "Caniche",
        "decors": {
            1: {"name": "Le Trocadéro", "plate": "Eiffel Tower silhouette, stone esplanade, warm streetlamps bokeh."},
            2: {"name": "Les Quais de Seine", "plate": "River banks, cobble stones, Eiffel Tower reflected in water."},
            3: {"name": "Le Pied de la Tour", "plate": "Low angle iron lattice, ground level view."},
            4: {"name": "Champ-de-Mars", "plate": "Green grass, distant tower, soft focus trees."}
        }
    },
    "venice_italy": {
        "name": "Venise", "struct": "C", "obj": "Masque de chat", "animal": "Pigeon blanc",
        "decors": {
            1: {"name": "Le Grand Canal", "plate": "Calm water, gondola silhouette, historic palaces."},
            2: {"name": "Le Pont des Soupirs", "plate": "Narrow canal, stone bridge, soft reflections."},
            3: {"name": "Place Saint-Marc", "plate": "Paved square, Byzantine arches, blue hour light."},
            4: {"name": "Intérieur Gondole", "plate": "Dark wood, velvet, ripples visible nearby."}
        }
    },
    "lapland_arctic": {
        "name": "Laponie", "struct": "A", "obj": "Chocolat chaud", "animal": "Renne",
        "decors": {
            1: {"name": "Forêt de Sapins", "plate": "Heavy snow, pine silhouettes, aurora glow."},
            2: {"name": "Extérieur Igloo", "plate": "Snow dome, warm light from entrance, starry sky."},
            3: {"name": "Le Traîneau", "plate": "Wooden sled, thick fur blankets, snowy path."},
            4: {"name": "Intérieur Igloo", "plate": "Ice walls, soft warm glow, cozy atmosphere."}
        }
    }
}

# --- 3. LES 20 PLANS RÉELS (Extraits de ton PLAN_DE_REALISATION) ---
PLANS_DATA = {
    1: {"angle": "Wide", "light": "Golden Hour", "A": "Arrival (misty)", "B": "Arrival (searching for Pipo)", "C": "Departure (on transport)"},
    2: {"angle": "Medium", "light": "Golden Hour", "A": "Rubs eyes", "B": "Rubs eyes, searching", "C": "Looks ahead steady"},
    3: {"angle": "Close-up", "light": "Sunset", "A": "Watches Pipo glow", "B": "Walks on tiptoes", "C": "Landscape drifts behind"},
    4: {"angle": "POV", "light": "Sunset", "A": "Looks at detail", "B": "Sees a clue", "C": "Follows light cue"},
    5: {"angle": "Medium", "light": "Sunset", "A": "Reaches for light", "B": "Laughs with Pipo", "C": "Drags paw in water"},
    6: {"angle": "Wide", "light": "Dusk", "A": "Watches Pipo fly", "B": "Searches the space", "C": "Passes under arch"},
    7: {"angle": "Detail", "light": "Dusk", "A": "Notices sky change", "B": "Peeks through hole", "C": "Follows small glow"},
    8: {"angle": "Medium", "light": "Dusk", "A": "Uses {obj}", "B": "Uses {obj}", "C": "Plays with {obj}"},
    9: {"angle": "Wide", "light": "Dusk", "A": "Watches monument shift", "B": "Enters calm space", "C": "Slows down observing"},
    10: {"angle": "Close-up", "light": "Blue Hour", "A": "Face in awe", "B": "Looks amazed", "C": "Eyelids heavy"},
    11: {"angle": "Wide", "light": "Night", "A": "Watches stars", "B": "Quiet break with Pipo", "C": "Landmark in distance"},
    12: {"angle": "Wide", "light": "Night", "A": "Slows, softening", "B": "Game ends calmly", "C": "Approaches slowly"},
    13: {"angle": "Close-up", "light": "Night", "A": "Sees {animal} sleeping", "B": "Sees {animal} sleeping", "C": "Sees {animal} sleeping"},
    14: {"angle": "Medium", "light": "Night", "A": "Stands calmly", "B": "Stands calmly", "C": "Relaxes"},
    15: {"angle": "Detail", "light": "Night", "A": "Landmark twinkles", "B": "Landmark sparkles", "C": "Transport stops"},
    16: {"angle": "Medium", "light": "Night", "A": "Prepares sleeping spot", "B": "Finds cozy corner", "C": "Settles to sleep"},
    17: {"angle": "Close-up", "light": "Night", "A": "Relaxes", "B": "Relaxes", "C": "Relaxes"},
    18: {"angle": "Close-up", "light": "Night", "A": "Huge slow yawn", "B": "Huge slow yawn", "C": "Huge slow yawn"},
    19: {"angle": "Wide", "light": "Night", "A": "Peaceful landscape", "B": "Peaceful landscape", "C": "Peaceful landscape"},
    20: {"angle": "Wide", "light": "Night", "A": "Sleep / black", "B": "Sleep / black", "C": "Sleep / black"}
}

# --- 4. INTERFACE ---
st.set_page_config(page_title="Mélo 160s Studio", layout="wide")
st.title("🎭 Mélo & Pipo : Production Automatique 20 Plans")

with st.sidebar:
    st.header("⚙️ Pilotage")
    ville_id = st.selectbox("Destination", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['name'])
    p_id = st.select_slider("Numéro du Plan (1-20)", options=list(PLANS_DATA.keys()))
    
    st.divider()
    
    ville = DESTINATIONS[ville_id]
    plan_info = PLANS_DATA[p_id]
    struct = ville['struct']
    
    # Détermination AUTO du décor (tous les 5 plans)
    decor_id = (p_id - 1) // 5 + 1
    decor = ville['decors'][decor_id]
    
    # Action auto basée sur la Structure (A, B ou C)
    action_melo = plan_info[struct].format(obj=ville['obj'], animal=ville['animal'])

    st.success(f"Mode AUTO : Plan {p_id} détecté.")
    st.info(f"Structure {struct} | Décor {decor_id} ({decor['name']})")

# --- 5. DASHBOARD DE PRODUCTION ---
st.header(f"Plan {p_id} : {ville['name']} — {decor['name']}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("ACTION MÉLO", action_melo)
with col2:
    st.metric("HORAIRE", plan_info['light'])
with col3:
    st.metric("ANGLE", plan_info['angle'])

st.divider()

# --- 6. PROMPTS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (PLATE)", "🎨 2. IMAGE (INTEGRATION)", "🎞️ 3. VIDÉO (MOUVEMENT)"])

with tab1:
    st.write("### Prompt Décor")
    p1 = f"Environment Plate: {decor['plate']} Time: {plan_info['light']}. POETIC, MINIMALIST. --ar 16:9"
    st.code(p1, language="text")

with tab2:
    st.write("### Prompt Nanobanana")
    p2 = f"Integration: {MELO_DNA}. Action: {action_melo}. Decor: {decor['name']}. Location: {ville['name']}. {plan_info['light']}. [VERROUS]: {VERROUS}. --ar 16:9"
    st.code(p2, language="text")

with tab3:
    st.write("### Prompt Veo 3")
    p3 = f"Animation (8s): {action_melo} in ultra-slow motion. Melo in {decor['name']}. Pipo companion nearby. {plan_info['light']}. Perfect loop, cinematic PBR."
    st.code(p3, language="text")
