import streamlit as st
import io
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image

# =========================================================
# 1. ADN & VERROUS TECHNIQUES (STRICTS)
# =========================================================
DNA_MELO = "Bunny-shaped designer toy, blue glass suit, ultra-glossy. White round belly, white paws. Rounded child proportions."
DNA_PIPO = "Microscopic snow-potato companion; white iridescent reflections. Tiny scale. Soft constant glow."
TECH_LOCKS = "Ultra-realistic cinematic PBR, 8k, macro-cinematography, ground level camera, Ray-traced reflections."

# =========================================================
# 2. STRUCTURES DE DONNÉES (COQUES VIDES POUR INJECTION)
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

# La structure PLAN intègre maintenant les 6 variables Vidéo pour la synchro
PLANS_SEQ = {
    1: {
        "Angle": "wide-angle lens", "Light": "Golden Hour", 
        "M_Pose": "relaxed sitting", "M_Expr": "curious", "P_Pose": "floating", "P_Pos": "near head", "Acc": "none", "Palette": "Natural", "P_Col": "Iridescent White", "Trail": "Soft glow",
        "V_Mode": "Perfect loop", "V_Act": "Gentle interaction", "V_M_Mvt": "Breathing only", "V_P_Mvt": "Hovering gently", "V_Cam": "Locked camera", "V_Env": "None"
    }
}

MAT_MAP = {
    "🍭 SUCRERIES": {"Marshmallow foam": "Marshmallow foam", "Jelly candy": "Jelly candy"},
    "🧶 TEXTILES": {"Felted wool fabric": "Felted wool fabric"},
    "📜 PAPIER & BOIS": {"Toy wood": "Toy wood"},
    "🧩 JOUETS": {"Lego": "Lego"}
}

# =========================================================
# 3. CONFIGURATION UI
# =========================================================
st.set_page_config(page_title="Melo Integrated Cockpit V69", layout="wide")

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
# 4. ONGLET 1 : DÉCOR
# =========================================================
with tab1:
    st.subheader("⚙️ Pilotage du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_opts = list(ville['decors'].keys())
        b5_val = st.selectbox("LIEU PRÉCIS (E5)", b5_opts, index=b5_opts.index(auto_b5_id) if auto_b5_id in b5_opts else 0, format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        cam_opts = ["wide-angle lens", "macro lens", "eye-level"]
        b6_val = st.selectbox("ANGLE (B6)", cam_opts, index=cam_opts.index(plan['Angle']) if plan['Angle'] in cam_opts else 0, disabled=not e7_bool)
    with c2:
        light_opts = ["Golden Hour", "Sunset", "Blue Hour", "Deep Night"]
        b7_val = st.selectbox("LUMIÈRE (B7)", light_opts, index=light_opts.index(plan['Light']) if plan['Light'] in light_opts else 0, disabled=not e7_bool)
        b8_val = st.selectbox("AMBIANCE (B8)", ["calm", "mysterious", "joyful"], disabled=not e7_bool)
    with c3:
        cat_d8 = st.selectbox("CATÉGORIE MATIÈRE", list(MAT_MAP.keys()), disabled=not e7_bool)
        d8_name = st.selectbox("MATÉRIEL D8", list(MAT_MAP[cat_d8].keys()), disabled=not e7_bool)
        d9_val = st.selectbox("MATÉRIEL D9", ["none", "frosted glass", "gold dust"], disabled=not e7_bool)
    
    e5_en = ville['decors'][b5_val]['en']
    prompt_1 = f"Environment: {e5_en}. Light: {b7_val}. Angle: {b6_val}. Material: {d8_name}. Pure background plate."
    st.code(prompt_1)

# =========================================================
# 5. ONGLET 2 : IMAGE (PERSOS)
# =========================================================
with tab2:
    st.subheader("🎨 Pilotage Mélo & Pipo")
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1:
        pm_opts = ["relaxed sitting", "standing", "walking"]
        s_pose_m = st.selectbox("1. Pose Mélo (FR)", pm_opts, index=pm_opts.index(plan['M_Pose']) if plan['M_Pose'] in pm_opts else 0, disabled=not e7_bool)
        em_opts = ["curious", "smiling", "amazed"]
        s_expr_m = st.selectbox("2. Expression de Mélo", em_opts, index=em_opts.index(plan['M_Expr']) if plan['M_Expr'] in em_opts else 0, disabled=not e7_bool)
    with r2c2:
        pp_opts = ["floating", "orbiting", "static"]
        s_pose_p = st.selectbox("3. Pose Pipo (FR)", pp_opts, index=pp_opts.index(plan['P_Pose']) if plan['P_Pose'] in pp_opts else 0, disabled=not e7_bool)
        posp_opts = ["near head", "on shoulder"]
        s_pos_p = st.selectbox("4. Position Pipo (FR)", posp_opts, index=posp_opts.index(plan['P_Pos']) if plan['P_Pos'] in posp_opts else 0, disabled=not e7_bool)
    with r2c3:
        s_acc = st.text_input("5. Melo accessory", value=plan['Acc'], disabled=not e7_bool)
        pal_opts = ["Natural", "Pastel"]
        s_pal = st.selectbox("6. Color palette", pal_opts, index=pal_opts.index(plan['Palette']) if plan['Palette'] in pal_opts else 0, disabled=not e7_bool)
    with r2c4:
        pcol_opts = ["Iridescent White", "Pure Pearl"]
        s_pcol = st.selectbox("7. Pipo color", pcol_opts, index=pcol_opts.index(plan['P_Col']) if plan['P_Col'] in pcol_opts else 0, disabled=not e7_bool)
        tr_opts = ["Soft glow", "Sparkles"]
        s_trail = st.selectbox("8. Pipo energy trail", tr_opts, index=tr_opts.index(plan['Trail']) if plan['Trail'] in tr_opts else 0, disabled=not e7_bool)

    prompt_2 = f"Character integration: MÉLO ({DNA_MELO}) and PIPO ({DNA_PIPO}). Pose: {s_pose_m}. Expr: {s_expr_m}. {TECH_LOCKS}"
    st.code(prompt_2)

# =========================================================
# 6. ONGLET 3 : VIDÉO (LES 6 NOUVEAUX SÉLECTEURS)
# =========================================================
with tab3:
    st.subheader("🎞️ Paramètres de Mouvement Vidéo")
    v1, v2, v3 = st.columns(3)
    with v1:
        vmode_opts = ["Perfect loop", "Non-loop cinematic"]
        s_vmode = st.selectbox("1. Mode vidéo", vmode_opts, index=vmode_opts.index(plan['V_Mode']) if plan['V_Mode'] in vmode_opts else 0, disabled=not e7_bool)
        vact_opts = ["Gentle interaction", "Silent exploration", "Poetic break"]
        s_vact = st.selectbox("2. Type d’action", vact_opts, index=vact_opts.index(plan['V_Act']) if plan['V_Act'] in vact_opts else 0, disabled=not e7_bool)
    with v2:
        vmm_opts = ["Breathing only", "Subtle eye blink", "Slow head turn"]
        s_vmm = st.selectbox("3. Mouvement de Mélo", vmm_opts, index=vmm_opts.index(plan['V_M_Mvt']) if plan['V_M_Mvt'] in vmm_opts else 0, disabled=not e7_bool)
        vpm_opts = ["Hovering gently", "Slow circular float", "Tiny bounce"]
        s_vpm = st.selectbox("4. Mouvement de Pipo", vpm_opts, index=vpm_opts.index(plan['V_P_Mvt']) if plan['V_P_Mvt'] in vpm_opts else 0, disabled=not e7_bool)
    with v3:
        vcam_opts = ["Locked camera", "Ultra-slow push-in", "Slow pan"]
        s_vcam = st.selectbox("5. Mouvement caméra", vcam_opts, index=vcam_opts.index(plan['V_Cam']) if plan['V_Cam'] in vcam_opts else 0, disabled=not e7_bool)
        venv_opts = ["None", "Very subtle fog drift", "Light variation"]
        s_venv = st.selectbox("6. Mouvement environnement", venv_opts, index=venv_opts.index(plan['V_Env']) if plan['V_Env'] in venv_opts else 0, disabled=not e7_bool)

    prompt_3 = f"Cinematic Animation (8s): {s_vact}. Melo: {s_vmm}. Pipo: {s_vpm}. Cam: {s_vcam}. Env: {s_venv}. {s_vmode}."
    st.info("📝 PROMPT VIDÉO :")
    st.code(prompt_3)

# =========================================================
# 7. BOUTON RENDU VERTEX
# =========================================================
st.divider()
if st.button("🚀 RENDU UNIQUE (VERTEX AI)"):
    st.success("Lancement du moteur Nanobanana Pro...")
