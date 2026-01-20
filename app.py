import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# 1. ADN & VERROUS TECHNIQUES (B22)
# =========================================================
DNA_MELO = "Bunny-shaped high-end designer toy, blue glass suit, ultra-glossy. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; iridescent reflections. Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera perspective."

# =========================================================
# 2. STRUCTURES DE DONNÉES (COQUES VIDES)
# =========================================================
DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)", "landmark_en": "Eiffel Tower",
        "decors": {
            1: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Eiffel Tower in background..."},
            2: {"fr": "Les Quais de Seine", "en": "The Seine banks", "cue": "..."},
            3: {"fr": "Au pied de la Tour", "en": "At the foot of the Tower", "cue": "..."},
            4: {"fr": "Pelouse du Champ-de-Mars", "en": "Champ-de-Mars Lawn", "cue": "..."}
        }
    }
}

# La structure PLAN intègre maintenant les 8 variables Image pour la synchro Auto
PLANS_SEQ = {
    1: {
        "Angle": "wide-angle lens", "Light": "Golden Hour", 
        "M_Pose": "relaxed sitting", "M_Expr": "curious", 
        "P_Pose": "floating", "P_Pos": "near head",
        "Acc": "none", "Palette": "Natural", "P_Col": "Iridescent White", "Trail": "Soft glow"
    }
}

# =========================================================
# 3. CONFIGURATION UI
# =========================================================
st.set_page_config(page_title="Melo integrated Cockpit V68", layout="wide")

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ ACTIVER MODE MANUEL (E7)", value=False)
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    ville = DB_DECORS[v_id]
    plan = PLANS_SEQ.get(p_id, PLANS_SEQ[1])
    auto_b5_id = ((p_id - 1) % 4) + 1

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (FOND)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# =========================================================
# 4. ONGLET 1 : DÉCOR (STABLE)
# =========================================================
with tab1:
    st.subheader("⚙️ Pilotage du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_opts = list(ville['decors'].keys())
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", b5_opts, index=b5_opts.index(auto_b5_id) if auto_b5_id in b5_opts else 0, 
                              format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        cam_opts = ["wide-angle lens", "macro lens", "ground perspective", "eye-level"]
        b6_val = st.selectbox("ANGLE (B6/I34)", cam_opts, index=cam_opts.index(plan['Angle']) if plan['Angle'] in cam_opts else 0, disabled=not e7_bool)
    with c2:
        light_opts = ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"]
        b7_val = st.selectbox("LUMIÈRE (B7/I35)", light_opts, index=light_opts.index(plan['Light']) if plan['Light'] in light_opts else 0, disabled=not e7_bool)
        b8_val = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", ["Marshmallow foam", "Jelly candy", "Candy"], disabled=not e7_bool)
        d9_val = st.selectbox("MATÉRIEL D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
    
    # Formula Prompt 1
    e5_en = ville['decors'][b5_val]['en']
    prompt_1 = f"Environment: {e5_en}. Light: {b7_val}. Angle: {b6_val}. Material: {d8_val}. Pure background plate."
    st.code(prompt_1)

# =========================================================
# 5. ONGLET 2 : IMAGE (LES 8 SÉLECTEURS)
# =========================================================
with tab2:
    st.subheader("🎨 Pilotage Mélo & Pipo")
    
    # Organisation en 4 colonnes pour les 8 sélecteurs
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    
    with r1c1:
        pose_m_opts = ["relaxed sitting", "standing curious", "walking", "dancing"]
        s_pose_m = st.selectbox("1. Pose Mélo (FR)", pose_m_opts, 
                                index=pose_m_opts.index(plan['M_Pose']) if plan['M_Pose'] in pose_m_opts else 0, disabled=not e7_bool)
        
        expr_m_opts = ["curious", "smiling", "amazed", "sleepy"]
        s_expr_m = st.selectbox("2. Expression de Mélo", expr_m_opts, 
                                index=expr_m_opts.index(plan['M_Expr']) if plan['M_Expr'] in expr_m_opts else 0, disabled=not e7_bool)

    with r1c2:
        pose_p_opts = ["floating", "orbiting", "static", "hiding"]
        s_pose_p = st.selectbox("3. Pose Pipo (FR)", pose_p_opts, 
                                index=pose_p_opts.index(plan['P_Pose']) if plan['P_Pose'] in pose_p_opts else 0, disabled=not e7_bool)
        
        pos_p_opts = ["near head", "on shoulder", "in front", "behind"]
        s_pos_p = st.selectbox("4. Position Pipo (FR)", pos_p_opts, 
                               index=pos_p_opts.index(plan['P_Pos']) if plan['P_Pos'] in pos_p_opts else 0, disabled=not e7_bool)

    with r1c3:
        s_acc = st.text_input("5. Melo Accessory", value=plan['Acc'], disabled=not e7_bool)
        
        pal_opts = ["Natural", "Pastel", "Vibrant", "Monochrome"]
        s_pal = st.selectbox("6. Color Palette", pal_opts, 
                             index=pal_opts.index(plan['Palette']) if plan['Palette'] in pal_opts else 0, disabled=not e7_bool)

    with r1c4:
        pcol_opts = ["Iridescent White", "Pure Pearl", "Golden Glow"]
        s_pcol = st.selectbox("7. Pipo Color", pcol_opts, 
                              index=pcol_opts.index(plan['P_Col']) if plan['P_Col'] in pcol_opts else 0, disabled=not e7_bool)
        
        trail_opts = ["Soft glow", "Ribbon of light", "Sparkles", "none"]
        s_trail = st.selectbox("8. Pipo energy trail", trail_opts, 
                               index=trail_opts.index(plan['Trail']) if plan['Trail'] in trail_opts else 0, disabled=not e7_bool)

    # --- FORMULE MAÎTRESSE PROMPT 2 ---
    prompt_2 = (
        f"A high-end cinematic character photography of MÉLO and PIPO. "
        f"{DNA_MELO} POSE: {s_pose_m}. EXPRESSION: {s_expr_m}. ACCESSORY: {s_acc}. "
        f"{DNA_PIPO} POSE: {s_pose_p}. POSITION: {s_pos_p}. "
        f"STYLE: Palette {s_pal}. Pipo Color: {s_pcol}. Trail: {s_trail}. "
        f"INTEGRATION: Placed in {e5_en} ({ville['nom_fr']}). {TECH_LOCKS}"
    )
    st.info("📝 PROMPT PERSONNAGES :")
    st.code(prompt_2)

# =========================================================
# 6. ONGLET 3 : VIDÉO (STABLE)
# =========================================================
with tab3:
    st.subheader("🎞️ Paramètres d'Animation")
    v_mode = st.selectbox("MODE VIDÉO", ["Perfect loop", "Cinematic non-loop"], disabled=not e7_bool)
    st.code(f"Animation: Melo {s_pose_m} in {e5_en}. Mode: {v_mode}.")

# =========================================================
# 7. MOTEUR RENDU
# =========================================================
if st.button("🚀 RENDU UNIQUE (ONGLET ACTIF)"):
    st.success("Appel Vertex AI...")
