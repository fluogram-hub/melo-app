import streamlit as st
import pandas as pd
import io

# =========================================================
# 1. CONFIGURATION & SESSION STATE
# =========================================================
st.set_page_config(page_title="Melo Production V71", layout="wide")

def init_app_state():
    if 'melo_db' not in st.session_state:
        st.session_state.melo_db = None

# =========================================================
# 2. CHARGEMENT DYNAMIQUE DEPUIS EXCEL
# =========================================================
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    uploaded_file = st.file_uploader("Charger 'MELO VALIDE' (XLSX)", type="xlsx")
    
    if uploaded_file and st.session_state.melo_db is None:
        try:
            # Lecture des feuilles clés
            df_lieux = pd.read_excel(uploaded_file, sheet_name="BASE_LIEUX")
            df_plans = pd.read_excel(uploaded_file, sheet_name="PLAN_DE_REALISATION")
            df_lists = pd.read_excel(uploaded_file, sheet_name="Lists")

            # Stockage des listes pour les menus déroulants
            st.session_state.lists = {col: df_lists[col].dropna().unique().tolist() for col in df_lists.columns}
            
            # Stockage du scénario (20 plans)
            st.session_state.scenarios = df_plans.set_index('Plan_ID').to_dict(orient='index')
            
            # Stockage des lieux
            st.session_state.lieux = df_lieux.set_index('LieuKey').to_dict(orient='index')
            
            st.session_state.melo_db = True
            st.success("✅ Studio prêt !")
        except Exception as e:
            st.error(f"Erreur : {e}")

if not st.session_state.get('melo_db'):
    st.info("👋 Veuillez charger votre fichier Excel pour activer les commandes.")
    st.stop()

# --- RÉCUPÉRATION DES DONNÉES EN MÉMOIRE ---
L = st.session_state.lists
SCENARIO = st.session_state.scenarios
LIEUX = st.session_state.lieux

# --- PILOTAGE BARRE LATÉRALE ---
with st.sidebar:
    st.divider()
    e7_bool = st.toggle("🕹️ ACTIVER MODE MANUEL (E7)", value=False)
    v_id = st.selectbox("DÉCOR (E5)", list(LIEUX.keys()), format_func=lambda x: f"{x} - {LIEUX[x].get('Lieu_FR', '')}")
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(SCENARIO.keys()))
    
    # Sélection du Scénario (A, B ou C)
    sc_ver = st.radio("VARIANTE DE SCÉNARIO", ["A", "B", "C"])
    
    st.divider()
    # Bouton d'exportation
    df_exp = pd.DataFrame.from_dict(SCENARIO, orient='index')
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_exp.to_excel(writer, sheet_name='PLANS_MODIFIES')
    st.download_button("💾 Exporter Scénario", output.getvalue(), "scenario_final.xlsx")

# Plan et Lieu actuels
plan = SCENARIO[p_id]
lieu = LIEUX[v_id]

# =========================================================
# 3. INTERFACE PAR ONGLETS
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (ENV)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR ---
with tab1:
    st.subheader("⚙️ Paramètres de l'Environnement")
    c1, c2, c3 = st.columns(3)
    with c1:
        b6_val = st.selectbox("ANGLE (B6/I34)", L['Angles_EN'], disabled=not e7_bool)
        b9_val = st.selectbox("SAISON (B9)", L['Season_EN'], disabled=not e7_bool)
    with c2:
        b7_val = st.selectbox("TIME OF DAY (B7/I35)", L['Time_of_day_EN'], disabled=not e7_bool)
        b8_val = st.selectbox("WEATHER (B8)", L['Weather_EN'], disabled=not e7_bool)
    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", L['MATERIAL_MAIN_EN'], disabled=not e7_bool)
        d9_val = st.selectbox("MATÉRIEL D9", L['MATERIAL_ACCENT_EN'], disabled=not e7_bool)
    
    b10_val = st.selectbox("ÉTAT DU SOL (B10)", L['Ground_state_EN'], disabled=not e7_bool)
    
    st.code(f"PROMPT DÉCOR: {lieu.get('Decor_Prompt_Simplified_EN', '')} in {b9_val}, {b7_val} light. Texture: {d8_val}.")

# --- ONGLET 2 : IMAGE (ÉDITEUR) ---
with tab2:
    st.subheader("🎨 Mise en scène & Personnages")
    r1, r2 = st.columns(2)
    
    # Récupération dynamique des colonnes selon la version (A, B ou C)
    col_melo = f"{sc_ver}_Melo_Action_EN"
    col_pipo = f"{sc_ver}_Pipo_Action_EN"

    with r1:
        plan[col_melo] = st.text_area("Pose Mélo (Modifiable)", value=plan.get(col_melo, ""))
        s_pal = st.selectbox("Color Palette", L['Color_Palette_EN'])
    with r2:
        plan[col_pipo] = st.text_area("Pose Pipo (Modifiable)", value=plan.get(col_pipo, ""))
        s_pcol = st.selectbox("Pipo Color", L['Pipo_Color_EN'])
        s_trail = st.selectbox("Pipo Energy Trail", L['Pipo_Energy_Trail_EN'])

    st.code(f"PROMPT IMAGE: Mélo: {plan[col_melo]} | Pipo: {plan[col_pipo]} | Palette: {s_pal}")

# --- ONGLET 3 : VIDÉO ---
with tab3:
    st.subheader("🎞️ Paramètres d'Animation")
    v1, v2 = st.columns(2)
    with v1:
        v_mode = st.selectbox("Mode vidéo", L['VIDEO_Mode_EN'])
        v_act = st.selectbox("Type d’action", L['VIDEO_ActionType_EN'])
        v_m_mvt = st.selectbox("Mouvement de Mélo", L['VIDEO_MeloMotion_EN'])
    with v2:
        v_p_mvt = st.selectbox("Mouvement de Pipo", L['VIDEO_PipoMotion_EN'])
        v_cam = st.selectbox("Mouvement caméra", L['VIDEO_Camera_EN'])
        v_env = st.selectbox("Mouvement environnement", L['VIDEO_Env_EN'])

    st.code(f"PROMPT VIDÉO: {v_mode}, {v_act}. Motion: Mélo {v_m_mvt}, Pipo {v_p_mvt}. Cam: {v_cam}")
