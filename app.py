import streamlit as st
import pandas as pd
import io

# =========================================================
# ZONE 1 : CONFIGURATION GLOBALE (IDENTITY LOCK)
# =========================================================
B22_IDENTITY_LOCK = """MÉLO (LOCK — DO NOT CHANGE):
- MÉLO: Bunny-shaped high-end designer toy wearing a blue glossy suit.
- Same face, proportions, materials.
- PIOPO: microscopic snow-potato companion; white with subtle iridescent reflections."""

# =========================================================
# ZONE 2 : INITIALISATION & CHARGEMENT SÉCURISÉ
# =========================================================
st.set_page_config(page_title="Melo Production V71", layout="wide")

# Initialisation des variables de session (évite les AttributeError)
if 'melo_db_ready' not in st.session_state:
    st.session_state.melo_db_ready = False
if 'lists' not in st.session_state:
    st.session_state.lists = {}
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}
if 'lieux' not in st.session_state:
    st.session_state.lieux = {}

with st.sidebar:
    st.title("🎬 STUDIO MÉLO V71")
    uploaded_file = st.file_uploader("Étape 1 : Charger l'Excel Maître", type="xlsx")
    
    if uploaded_file and not st.session_state.melo_db_ready:
        try:
            # Lecture des feuilles spécifiques de ton fichier
            df_lieux = pd.read_excel(uploaded_file, sheet_name="BASE_LIEUX")
            df_plans = pd.read_excel(uploaded_file, sheet_name="PLAN_DE_REALISATION")
            df_lists = pd.read_excel(uploaded_file, sheet_name="Lists")

            # Extraction des listes pour les menus déroulants
            st.session_state.lists = {col: df_lists[col].dropna().unique().tolist() for col in df_lists.columns}
            
            # Stockage du scénario et des lieux (on indexe par Plan_ID et LieuKey)
            st.session_state.scenarios = df_plans.set_index('Plan_ID').to_dict(orient='index')
            st.session_state.lieux = df_lieux.set_index('LieuKey').to_dict(orient='index')
            
            st.session_state.melo_db_ready = True
            st.success("✅ Studio synchronisé !")
            st.rerun()
        except Exception as e:
            st.error(f"Erreur de lecture : {e}")

# Si le fichier n'est pas encore chargé, on arrête l'affichage ici
if not st.session_state.melo_db_ready:
    st.info("👋 Bienvenue dans le Studio Mélo. Veuillez charger le fichier Excel dans la barre latérale pour commencer.")
    st.stop()

# =========================================================
# ZONE 3 : LOGIQUE DE PILOTAGE (SIDEBAR)
# =========================================================
L = st.session_state.lists
SCENARIO = st.session_state.scenarios
LIEUX = st.session_state.lieux

with st.sidebar:
    st.divider()
    e7_bool = st.toggle("🕹️ MODE ÉDITION MANUELLE (E7)", value=False)
    
    # Sélections principales
    v_id = st.selectbox("DESTINATION (B9)", list(LIEUX.keys()), 
                        format_func=lambda x: f"{x} - {LIEUX[x].get('Lieu_FR', 'Inconnu')}")
    
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(SCENARIO.keys()))
    
    sc_ver = st.radio("VARIANTE DE SCÉNARIO", ["A", "B", "C"], help="Pilote les colonnes A, B ou C de l'Excel")

    st.divider()
    # Exportation des modifications
    st.subheader("💾 SAUVEGARDE")
    df_export = pd.DataFrame.from_dict(SCENARIO, orient='index')
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_export.to_excel(writer, sheet_name='PLAN_DE_REALISATION')
    st.download_button("Exporter Scénario Modifié", output.getvalue(), "melo_scenario_custom.xlsx")

# Variables de travail pour le plan en cours
plan = SCENARIO[p_id]
lieu = LIEUX[v_id]
auto_b5_id = ((p_id - 1) % 4) + 1

# =========================================================
# ZONE 4 : INTERFACE (ONGLETS)
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (ENV)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# --- ONGLET 1 : DÉCOR ---
with tab1:
    st.subheader("⚙️ Paramètres du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        # On utilise les listes de l'onglet 'Lists' de ton Excel
        b6_val = st.selectbox("ANGLE (B6)", L.get('Angles_EN', []), disabled=not e7_bool)
        b9_val = st.selectbox("SAISON (B9)", L.get('Season_EN', []), disabled=not e7_bool)
    with c2:
        b7_val = st.selectbox("TIME OF DAY (B7)", L.get('Time_of_day_EN', []), disabled=not e7_bool)
        b8_val = st.selectbox("WEATHER (B8)", L.get('Weather_EN', []), disabled=not e7_bool)
    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", L.get('MATERIAL_MAIN_EN', []), disabled=not e7_bool)
        d9_val = st.selectbox("MATÉRIEL D9", L.get('MATERIAL_ACCENT_EN', []), disabled=not e7_bool)

    b10_val = st.selectbox("ÉTAT DU SOL (B10)", L.get('Ground_state_EN', []), disabled=not e7_bool)

    # FORMULE PROMPT 1
    prompt_1 = (f"Cinematic environment: {lieu.get('Decor_Prompt_Simplified_EN', 'N/A')}. "
                f"Lighting: {b7_val}, Weather: {b8_val}. Materials: {d8_val} and {d9_val}. "
                f"Ground: {b10_val}. Angle: {b6_val}.")
    st.code(prompt_1)

# --- ONGLET 2 : IMAGE (ÉDITEUR EN DIRECT) ---
with tab2:
    st.subheader(f"🎨 Éditeur de Scénario - Plan {p_id} (Variante {sc_ver})")
    
    # Mapping dynamique vers les colonnes A, B ou C de ton Excel
    col_melo = f"{sc_ver}_Melo_Action_EN"
    col_pipo = f"{sc_ver}_Pipo_Action_EN"

    r1, r2 = st.columns(2)
    with r1:
        # La modification ici met à jour SCENARIO[p_id] en temps réel
        plan[col_melo] = st.text_area("Pose Mélo (Modifier ici)", value=str(plan.get(col_melo, "")))
        s_pal = st.selectbox("Color Palette", L.get('Color_Palette_EN', []))
    with r2:
        plan[col_pipo] = st.text_area("Pose Pipo (Modifier ici)", value=str(plan.get(col_pipo, "")))
        s_pcol = st.selectbox("Pipo Color", L.get('Pipo_Color_EN', []))
        s_trail = st.selectbox("Pipo Energy Trail", L.get('Pipo_Energy_Trail_EN', []))

    prompt_2 = (f"IMAGE COMPOSITING: {B22_IDENTITY_LOCK}\n"
                f"DIRECTION: Melo is {plan[col_melo]}. Pipo is {plan[col_pipo]}.\n"
                f"STYLE: Palette {s_pal}, Trail {s_trail}.")
    st.code(prompt_2)

# --- ONGLET 3 : VIDÉO ---
with tab3:
    st.subheader("🎞️ Paramètres d'Animation Vidéo")
    v1, v2, v3 = st.columns(3)
    with v1:
        v_mode = st.selectbox("Mode vidéo", L.get('VIDEO_Mode_EN', []))
        v_act = st.selectbox("Type d’action", L.get('VIDEO_ActionType_EN', []))
    with v2:
        v_m_mvt = st.selectbox("Mouvement de Mélo", L.get('VIDEO_MeloMotion_EN', []))
        v_p_mvt = st.selectbox("Mouvement de Pipo", L.get('VIDEO_PipoMotion_EN', []))
    with v3:
        v_cam = st.selectbox("Mouvement caméra", L.get('VIDEO_Camera_EN', []))
        v_env = st.selectbox("Mouvement environnement", L.get('VIDEO_Env_EN', []))

    prompt_3 = (f"VIDEO GENERATION: Mode {v_mode}, Action {v_act}. "
                f"Melo: {v_m_mvt}, Pipo: {v_p_mvt}. Camera: {v_cam}. Env: {v_env}.")
    st.code(prompt_3)

# =========================================================
# ZONE 7 : MOTEUR RENDU
# =========================================================
st.divider()
if st.button("🚀 LANCER LE RENDU DU PLAN"):
    st.info(f"Envoi du Plan {p_id} (Lieu: {v_id}) vers Vertex AI...")
