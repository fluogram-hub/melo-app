import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN MÉLO & PIPO (STRICT B22) ---
DNA_MELO = "MÉLO: Bunny-shaped high-end designer toy, blue glass suit (transparent blue glass effect), ultra-glossy. White round belly with yellow notes, white mitten-like paws. Rounded child proportions. No internal anatomy."
DNA_PIPO = "PIPO: Microscopic snow-potato companion; white iridescent reflections. Tiny scale (5-10% of Mélo). Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera perspective. Soft cinematic bokeh, Ray-traced lighting."

# --- 2. BASE DE DONNÉES LIEUX (B5 / B9 / B12) ---
DESTINATIONS = {
    "paris": {"nom": "Paris (France)", "landmark": "Eiffel Tower", "lieux": {
        1: {"nom": "Le Trocadéro", "cue": "Eiffel Tower clearly recognizable in the background. Wide stone esplanade, symmetric architecture, classic Parisian perspectives."},
        2: {"nom": "Les Quais de Seine", "cue": "River Seine reflections with ripples, old stone banks, the Eiffel Tower appearing as a distant blurred silhouette through morning mist."},
        3: {"nom": "Au pied de la Tour", "cue": "Industrial metallic lattice structure of the Eiffel Tower base, massive iron beams, looking up from the ground."},
        4: {"nom": "Pelouse du Champ-de-Mars", "cue": "Large open grass area, distant tower silhouette, park atmosphere with soft horizon."}}}
}

# --- 3. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Director V55", layout="wide")

# --- 4. SIDEBAR (PILOTAGE FR) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DESTINATIONS.keys()), format_func=lambda x: DESTINATIONS[x]['nom'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DESTINATIONS[v_id]
    auto_b5 = (p_id - 1) // 5 + 1
    
# --- 5. LOGIQUE DES ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- VARIABLES COMMUNES ---
with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_val = st.selectbox("LIEU (E5)", [1,2,3,4], index=auto_b5-1, format_func=lambda x: ville['lieux'][x]['nom'], disabled=not e7_bool)
        i34 = st.selectbox("ANGLE MANUEL (I34)", ["macro lens", "eye-level"], disabled=not e7_bool)
        b6 = "wide-angle lens" # Valeur auto
        cam_final = i34 if e7 == "yes" else b6
    with c2:
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Soft Moonlight", "Deep Night"], disabled=not e7_bool)
        b7 = "Golden Hour" # Valeur auto
        light_final = i35 if e7 == "yes" else b7
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious"], disabled=not e7_bool)
    with c3:
        d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool"], disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", "soft tactile textures", disabled=not e7_bool)
        b11 = st.selectbox("1er PLAN (B11)", ["", "flowers", "leaves"], disabled=not e7_bool)

    # --- FORMULE PROMPT 1 (DÉCOR) ---
    e5_name = ville['lieux'][b5_val]['nom']
    b12 = ville['lieux'][b5_val]['cue']
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "" else ""
    
    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_name}. "
        f"The scene is set in {ville['nom']} during the {light_final}, with a {b8} atmosphere. "
        f"The camera uses a {cam_final} with a low-angle ground perspective. {b11_str}"
        f"MATERIAL WORLD: All surfaces reimagined in {d8}{d9_str}. Realistic subsurface scattering. "
        f"COMPOSITION: Minimalist, clean. The landmark is a distant, soft-focus silhouette. "
        f"GROUND: {b10}. PLATE CUES (STRICT): {b12}. "
        f"RULES: No characters, pure background plate."
    )
    st.divider()
    st.subheader("📝 PROMPT 1 (DÉCOR)")
    st.code(prompt_1)

# --- TAB 2 : IMAGE (MÉLO & PIPO) ---
with tab2:
    st.write("### Configuration Personnages (Mélo & Pipo)")
    ic1, ic2 = st.columns(2)
    with ic1:
        # Actions issues du XLSX (Exemples)
        a_m = st.selectbox("ACTION MÉLO (A_M)", ["relaxed sitting", "standing curious", "walking gently"], disabled=not e7_bool)
        a_p = st.selectbox("ACTION PIPO (A_P)", ["floating near head", "resting on shoulder"], disabled=not e7_bool)
    with ic2:
        s_expr = st.selectbox("EXPRESSION", ["smiling", "amazed", "sleepy"], disabled=not e7_bool)
        s_acc = st.text_input("ACCESSOIRE", "none", disabled=not e7_bool)

    # --- FORMULE PROMPT 2 (IMAGE) ---
    # Cette formule combine l'ADN, les Actions et l'intégration au Décor
    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} ACTION: {a_m}. EXPRESSION: {s_expr}. ACCESSORY: {s_acc}. "
        f"{DNA_PIPO} ACTION: {a_p}. "
        f"INTEGRATION: Characters are perfectly placed within the {e5_name} environment ({light_final}). "
        f"The material of the world is {d8}. {TECH_LOCKS}. "
        f"COMPOSITION: Characters are the focus, {cam_final} framing."
    )
    st.divider()
    st.subheader("📝 PROMPT 2 (PERSONNAGES)")
    st.code(prompt_2)

# --- BOUTONS DE RENDU (VERTEX) ---
def init_vertex():
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        return True
    return False

st.divider()
c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    if st.button("🚀 RENDU UNIQUE (IMAGE ACTIVE)"):
        if init_vertex():
            with st.spinner("Nanobanana Pro calcule..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                # Détermine quel prompt envoyer selon l'onglet
                imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
                st.image(imgs[0]._pil_image, use_column_width=True)

with c_btn2:
    if st.button("🔥 BATCH PRODUCTION (DÉCOR x4)"):
        if init_vertex():
            with st.spinner("Série de 4 décors en cours..."):
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                batch = model.generate_images(prompt=prompt_1, number_of_images=4, aspect_ratio="16:9")
                cols = st.columns(2)
                for i, img in enumerate(batch):
                    with cols[i%2]: st.image(img._pil_image)
