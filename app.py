import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# --- 1. ADN & BIBLE B22 (STRICT V29) ---
DNA_MELO = "Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws. Blue glass suit (transparent blue glass effect), ultra glossy. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white with subtle iridescent reflections. Dot eyes and small smile. Tiny scale (5-10% of Mélo). Soft constant glow."
MATERIAL_MAIN_DNA = "Homogeneous transparent blue glass/jelly, no internal anatomy, high light refraction (IOR 1.5), realistic caustics."
TECH_LOCKS = "Ultra-realistic cinematic PBR, natural optics, ray-traced reflections, 8k, macro-cinematography, ground level camera."

# --- 2. BASE DE DONNÉES : LES 80 PLATE CUES (B12) ---
# Format : { "id_destination": { "nom_fr": "...", "landmark_en": "...", "decors": { id: {fr, en, cue} } } }
DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)", "landmark_en": "Eiffel Tower",
        "decors": {
            1: {"fr": "Le Trocadéro", "en": "Le Trocadéro", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Le Trocadéro. Keep framing stable, no characters, no animals, no text."},
            2: {"fr": "Les Quais de Seine", "en": "Les Quais de Seine", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Les Quais de Seine. Keep framing stable, no characters, no animals, no text."},
            3: {"fr": "Au pied de la Tour", "en": "Au pied de la Tour", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Au pied de la Tour. Keep framing stable, no characters, no animals, no text."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Pelouse du Champ-de-Mars", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Eiffel Tower clearly recognizable, Paris atmosphere, warm distant streetlamps bokeh. Specific setting: Pelouse du Champ-de-Mars. Keep framing stable, no characters, no animals, no text."}
        }
    },
    "mont_saint_michel": {
        "nom_fr": "Le Mont Saint-Michel (France)", "landmark_en": "Mont-Saint-Michel",
        "decors": {
            1: {"fr": "La Baie", "en": "La Baie", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Baie. Keep framing stable, no characters, no animals, no text."},
            2: {"fr": "La Porte d'Entrée", "en": "La Porte d'Entrée", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: La Porte d'Entrée. Keep framing stable, no characters, no animals, no text."},
            3: {"fr": "Le Cloître", "en": "Le Cloître", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: Le Cloître. Keep framing stable, no characters, no animals, no text."},
            4: {"fr": "Les Dunes", "en": "Les Dunes", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Mont-Saint-Michel silhouette recognizable, tidal bay, ancient stone textures, soft mist. Specific setting: Les Dunes. Keep framing stable, no characters, no animals, no text."}
        }
    },
    "santorini_greece": {
        "nom_fr": "Santorin (Grèce)", "landmark_en": "Santorini architecture",
        "decors": {
            1: {"fr": "La Vue Haute", "en": "La Vue Haute", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Vue Haute. Keep framing stable, no characters, no animals, no text."},
            2: {"fr": "La Ruelle Blanche", "en": "La Ruelle Blanche", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Ruelle Blanche. Keep framing stable, no characters, no animals, no text."},
            3: {"fr": "La Terrasse", "en": "La Terrasse", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: La Terrasse. Keep framing stable, no characters, no animals, no text."},
            4: {"fr": "Le Muret", "en": "Le Muret", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Santorini whitewashed architecture, blue domes, Aegean sea horizon, pastel sunset. Specific setting: Le Muret. Keep framing stable, no characters, no animals, no text."}
        }
    },
    "venice_italy": {
        "nom_fr": "Venise (Italie)", "landmark_en": "Venice canals",
        "decors": {
            1: {"fr": "Le Grand Canal", "en": "Le Grand Canal", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: Le Grand Canal. Keep framing stable, no characters, no animals, no text."},
            2: {"fr": "La Petite Ruelle", "en": "La Petite Ruelle", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: La Petite Ruelle. Keep framing stable, no characters, no animals, no text."},
            3: {"fr": "La Place Saint-Marc", "en": "La Place Saint-Marc", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: La Place Saint-Marc. Keep framing stable, no characters, no animals, no text."},
            4: {"fr": "L'Intérieur de la Gondole", "en": "L'Intérieur de la Gondole", "cue": "Ultra-realistic cinematic PBR environment plate, calm, poetic, bedtime-friendly, empty scene. Venice canals, calm water reflections, historic facades, soft lantern bokeh. Specific setting: L'Intérieur de la Gondole. Keep framing stable, no characters, no animals, no text."}
        }
    }
}
# Note : Les 16 autres destinations sont structurées de la même manière dans le code complet.

# --- 3. PLAN DE RÉALISATION (ACTION SYNC) ---
PLANS_DB = {
    1: {"Angle": "Wide / establishing", "Light": "Golden Hour", "AM": "Arrival (grey/misty landscape)", "AP": "Pipo floats next to Melo"},
    2: {"Angle": "Medium / approach", "Light": "Golden Hour", "AM": "Melo rubs his eyes, looking for color", "AP": "Pipo peeks playfully"},
    3: {"Angle": "Close-up", "Light": "Sunset", "AM": "Pipo glows softly, ready to help", "AP": "Melo watches Pipo glow"},
    10: {"Angle": "Close-up", "Light": "Blue Hour", "AM": "Melo face in awe, lit by color", "AP": "Pipo glows near Melo"},
    20: {"Angle": "Wide", "Light": "Night", "AM": "Sleep / fade to black", "AP": "Pipo dims to near-off"}
}

# --- 4. CONFIGURATION UI ---
st.set_page_config(page_title="Melo Production Master V62", layout="wide")
st.markdown("""
    <style>
    .info-card { background-color: #ffffff; border-left: 5px solid #007BFF; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .action-title { color: #007BFF; font-weight: bold; font-size: 0.85em; text-transform: uppercase; }
    .action-text { color: #333333; font-size: 1.1em; font-weight: 500; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIQUE SIDEBAR (PILOTAGE GLOBAL) ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("ACTIVER LE CONTRÔLE MANUEL (E7)", value=False)
    e7 = "yes" if e7_bool else "no"
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Données Plan & Destination
    ville = DB_DECORS[v_id]
    plan = PLANS_DB.get(p_id, PLANS_DB[1])
    auto_b5_id = ((p_id - 1) // 5) + 1

# --- 6. INTERFACE ONGLETS ---
etape = st.radio("ÉTAPE ACTUELLE :", ["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSONNAGES)", "🎞️ 3. VIDÉO"], horizontal=True)
st.divider()

# --- ONGLET 1 : DÉCOR ---
if "DÉCOR" in etape:
    col_u1, col_u2, col_u3 = st.columns(3)
    with col_u1:
        # E5 (Nom FR pour l'user, EN pour le prompt)
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", [1,2,3,4], index=auto_b5_id-1, format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        i34 = st.selectbox("ANGLE MANUEL (I34)", ["macro lens", "eye-level", "low-angle ground perspective"], disabled=not e7_bool)
        cam_final = i34 if e7 == "yes" else plan['Angle']
    
    with col_u2:
        i35 = st.selectbox("LUMIÈRE MANUELLE (I35)", ["Golden Hour", "Blue Hour", "Deep Night"], disabled=not e7_bool)
        light_final = i35 if e7 == "yes" else plan['Light']
        b8 = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], index=0, disabled=not e7_bool)
        b11 = st.selectbox("1ER PLAN (B11)", ["none", "wild flowers", "autumn leaves"], disabled=not e7_bool)
    
    with col_u3:
        d8 = st.selectbox("MATIÈRE D8", ["marshmallow", "jelly candy", "felted wool", "candy"], disabled=not e7_bool)
        d9 = st.selectbox("MATIÈRE D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
        b10 = st.text_input("SOL (B10)", value="dry", disabled=not e7_bool)

    # --- FORMULE PROMPT 1 (STRICTE XLSX) ---
    e5_en = ville['decors'][b5_val]['en']
    b9_fr = ville['nom_fr']
    b12_cue = ville['decors'][b5_val]['cue']
    
    d9_str = f" and {d9}" if (d9 != "" and d9 != "none") else ""
    b11_str = f"In the immediate foreground, a subtle {b11} adds volumetric depth; " if b11 != "none" else ""
    texture_logic = "sugar-coated crystalline textures" if d8 == "candy" else "polished finishes"

    prompt_1 = (
        f"An ultra-detailed cinematic environment photography of {e5_en}. "
        f"The scene is set in {b9_fr} during the {light_final}, with a {b8} atmosphere. "
        f"The camera uses a {cam_final} with a low-angle ground perspective. {b11_str}"
        f"MATERIAL WORLD & SHADING: All surfaces and architecture are physically reimagined in {d8}{d9_str}. "
        f"Surfaces feature realistic subsurface scattering and {texture_logic}. "
        f"COMPOSITION: Minimalist, clean, with large negative space. The landmark is a distant silhouette. "
        f"LIGHTING: Soft cinematic bokeh, gentle volumetric god-rays. GROUND: {b10}. "
        f"PLATE CUES (STRICT): {b12_cue}. "
        f"RULES: No characters, no people, no text. Pure background plate."
    )
    
    # Affichage des cartes bleues (V29)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="info-card"><div class="action-title">📍 LIEU (E5)</div><div class="action-text">{ville["decors"][b5_val]["fr"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="info-card"><div class="action-title">📸 ANGLE</div><div class="action-text">{cam_final}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="info-card"><div class="action-title">🌅 LUMIÈRE</div><div class="action-text">{light_final}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="info-card"><div class="action-title">🍭 MATIÈRE</div><div class="action-text">{d8}</div></div>', unsafe_allow_html=True)
    
    st.code(prompt_1)
    if st.button("🚀 RENDU VERTEX ULTRA"):
        creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        aiplatform.init(project="melo-prompt-generator", location="us-central1", credentials=creds)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        with st.spinner("Nanobanana Pro calcule..."):
            imgs = model.generate_images(prompt=prompt_1, number_of_images=1, aspect_ratio="16:9")
            st.image(imgs[0]._pil_image, use_column_width=True)

# --- ONGLET 2 : PERSONNAGES ---
elif "IMAGE" in etape:
    st.subheader("Pilotage Mélo & Pipo")
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        a_m_final = st.text_input("ACTION MÉLO (A_M)", value=plan['AM'], disabled=not e7_bool)
    with c_m2:
        a_p_final = st.text_input("ACTION PIPO (A_P)", value=plan['AP'], disabled=not e7_bool)

    prompt_2 = f"Character Study: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). MELO ACTION: {a_m_final}. PIPO ACTION: {a_p_final}. Integration in {ville['decors'][b5_val]['en']}. {TECH_LOCKS}"
    st.code(prompt_2)
