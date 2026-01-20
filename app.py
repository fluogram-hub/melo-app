import streamlit as st
import pandas as pd
import io

# =========================================================
# 1. INITIALISATION & CONFIGURATION
# =========================================================
st.set_page_config(page_title="Melo Production V71", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = None

# =========================================================
# 2. CHARGEMENT DE L'EXCEL
# =========================================================
with st.sidebar:
    st.title("🎬 STUDIO MÉLO V71")
    uploaded_file = st.file_uploader("Charger l'Excel Maître", type="xlsx")
    
    if uploaded_file and st.session_state.db is None:
        try:
            # Lecture des onglets
            df_lieux = pd.read_excel(uploaded_file, sheet_name="BASE_LIEUX")
            df_plans = pd.read_excel(uploaded_file, sheet_name="PLAN_DE_REALISATION")
            df_lists = pd.read_excel(uploaded_file, sheet_name="Lists")

            st.session_state.db = {
                "lieux": df_lieux.set_index('LieuKey').to_dict(orient='index'),
                "plans": df_plans.set_index('Plan_ID').to_dict(orient='index'),
                "lists": df_lists
            }
            st.rerun()
        except Exception as e:
            st.error(f"Erreur de lecture : {e}")

if not st.session_state.db:
    st.info("👋 Veuillez charger votre fichier Excel pour commencer.")
    st.stop()

# --- RÉCUPÉRATION DES DONNÉES ---
DB = st.session_state.db
L_DF = DB["lists"]
PLAN_MAP = DB["plans"]
LIEU_MAP = DB["lieux"]

# =========================================================
# 3. BARRE LATÉRALE (PILOTAGE)
# =========================================================
with st.sidebar:
    st.divider()
    e7_bool = st.toggle("🕹️ MODE MANUEL (E7)", value=False)
    
    # Choix de la Destination (LieuKey)
    v_id = st.selectbox("DESTINATION (B9)", list(LIEU_MAP.keys()), 
                        format_func=lambda x: f"{x} - {LIEU_MAP[x].get('CITY_NAME_FR', x)}")
    
    # Choix du Plan (1-20)
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(PLAN_MAP.keys()))
    
    # Choix de la variante (A, B ou C)
    sc_ver = st.radio("VARIANTE SCÉNARIO", ["A", "B", "C"])

    # --- LOGIQUE DÉCOR PRÉCIS (E5) ---
    # On filtre la colonne H de Lists (Decor_EN) qui commence par v_id
    all_decors = L_DF['Decor_EN'].dropna().astype(str).tolist()
    filtered_decors = [d for d in all_decors if d.lower().startswith(v_id.lower())]
    
    # On affiche le nom propre (après le tiret)
    clean_names = [d.split('–')[-1].strip() for d in filtered_decors]
    
    # Sélection automatique (cycle de 4)
    auto_idx = ((p_id - 1) % 4)
    if not clean_names: clean_names = ["Aucun décor trouvé"]
    
    # LE SÉLECTEUR E5 (DANS LA SIDEBAR)
    e5_val = st.selectbox("DÉCOR PRÉCIS (E5)", clean_names, 
                          index=auto_idx if auto_idx < len(clean_names) else 0,
                          disabled=not e7_bool)

    st.divider()
    # Bouton d'export
    df_exp = pd.DataFrame.from_dict(PLAN_MAP, orient='index')
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_exp.to_excel(writer, sheet_name='PLAN_DE_REALISATION')
    st.download_button("💾 Exporter Scénario", output.getvalue(), "scenario_melo.xlsx")

# --- VARIABLES ACTUELLES ---
current_plan = PLAN_MAP[p_id]
current_lieu = LIEU_MAP[v_id]
L = {col: L_DF[col].dropna().unique().tolist() for col in L_DF.columns}

# =========================================================
# 4. ONGLETS DE PRODUCTION
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR", "🎨 2. IMAGE", "🎞️ 3. VIDÉO"])

with tab1:
    st.subheader("⚙️ Paramètres du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        b6_val = st.selectbox("ANGLE (B6)", L.get('Angles_EN', []), disabled=not e7_bool)
        b9_val = st.selectbox("SAISON (B9)", L.get('Season_EN', []), disabled=not e7_bool)
    with c2:
        b7_val = st.selectbox("TIME OF DAY (B7)", L.get('Time_of_day_EN', []), disabled=not e7_bool)
        b8_val = st.selectbox("WEATHER (B8)", L.get('Weather_EN', []), disabled=not e7_bool)
    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", L.get('MATERIAL_MAIN_EN', []), disabled=not e7_bool)
        d9_val = st.selectbox("MATÉRIEL D9", L.get('MATERIAL_ACCENT_EN', []), disabled=not e7_bool)
    
    b10_val = st.selectbox("ÉTAT DU SOL (B10)", L.get('Ground_state_EN', []), disabled=not e7_bool)
    b11_val = st.text_input("1ER PLAN (B11)", value="none", disabled=not e7_bool)

    st.code(f"PROMPT DÉCOR: {e5_val} at {v_id}. {b9_val}, {b7_val}, {b8_val}. Materials: {d8_val}, {d9_val}. Ground: {b10_val}.")

with tab2:
    st.subheader(f"🎨 Éditeur Image - Plan {p_id}")
    col_melo = f"{sc_ver}_Melo_Action_EN"
    col_pipo = f"{sc_ver}_Pipo_Action_EN"
    
    r1, r2 = st.columns(2)
    with r1:
        current_plan[col_melo] = st.text_area("Pose Mélo", value=str(current_plan.get(col_melo, "")))
        s_pal = st.selectbox("Color Palette", L.get('Color_Palette_EN', []))
    with r2:
        current_plan[col_pipo] = st.text_area("Pose Pipo", value=str(current_plan.get(col_pipo, "")))
        s_pcol = st.selectbox("Pipo Color", L.get('Pipo_Color_EN', []))
        s_trail = st.selectbox("Pipo Energy Trail", L.get('Pipo_Energy_Trail_EN', []))

    st.code(f"PROMPT IMAGE: Melo: {current_plan[col_melo]} | Pipo: {current_plan[col_pipo]} | Palette: {s_pal}")

with tab3:
    st.subheader("🎞️ Paramètres Vidéo")
    v1, v2, v3 = st.columns(3)
    with v1:
        v_m = st.selectbox("Mode vidéo", L.get('VIDEO_Mode_EN', []))
        v_a = st.selectbox("Type d’action", L.get('VIDEO_ActionType_EN', []))
    with v2:
        v_mm = st.selectbox("Mouvement Mélo", L.get('VIDEO_MeloMotion_EN', []))
        v_pm = st.selectbox("Mouvement Pipo", L.get('VIDEO_PipoMotion_EN', []))
    with v3:
        v_cam = st.selectbox("Caméra", L.get('VIDEO_Camera_EN', []))
        v_env = st.selectbox("Environnement", L.get('VIDEO_Env_EN', []))

    st.code(f"PROMPT VIDÉO: {v_m}. Action: {v_a}. Melo: {v_mm}. Pipo: {v_pm}. Cam: {v_cam}.")

st.divider()
if st.button("🚀 RENDU VERTEX ULTRA"):
    st.success(f"Plan {p_id} envoyé pour génération.")
