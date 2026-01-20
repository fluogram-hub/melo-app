import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Melo Production V71", layout="wide")

# Initialisation
if 'melo_db_ready' not in st.session_state:
    st.session_state.melo_db_ready = False

# --- CHARGEMENT ---
with st.sidebar:
    st.title("🎬 STUDIO MÉLO V71")
    uploaded_file = st.file_uploader("Charger l'Excel", type="xlsx")
    
    if uploaded_file and not st.session_state.melo_db_ready:
        try:
            df_lieux = pd.read_excel(uploaded_file, sheet_name="BASE_LIEUX")
            df_plans = pd.read_excel(uploaded_file, sheet_name="PLAN_DE_REALISATION")
            df_lists = pd.read_excel(uploaded_file, sheet_name="Lists")

            # Sauvegarde des données
            st.session_state.lists = df_lists
            st.session_state.scenarios = df_plans.set_index('Plan_ID').to_dict(orient='index')
            st.session_state.lieux = df_lieux.set_index('LieuKey').to_dict(orient='index')
            st.session_state.melo_db_ready = True
            st.rerun()
        except Exception as e:
            st.error(f"Erreur : {e}")

if not st.session_state.melo_db_ready:
    st.stop()

# --- VARIABLES ---
L_DF = st.session_state.lists
SCENARIO = st.session_state.scenarios
LIEUX = st.session_state.lieux

with st.sidebar:
    e7_bool = st.toggle("🕹️ MODE MANUEL", value=False)
    v_id = st.selectbox("DESTINATION (B9)", list(LIEUX.keys()))
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(SCENARIO.keys()))
    sc_ver = st.radio("VARIANTE", ["A", "B", "C"])

# --- LOGIQUE FILTRE DÉCOR PRÉCIS (Colonne H de Lists) ---
# On cherche dans la colonne H (Decor_EN) les lignes qui commencent par v_id
all_decors = L_DF['Decor_EN'].dropna().tolist()
vrai_decors_v_id = [d for d in all_decors if d.startswith(v_id)]
# On nettoie le nom pour ne garder que ce qu'il y a après le "–"
clean_decors = [d.split('–')[-1].strip() for d in vrai_decors_v_id]

# Détermination automatique du décor selon le plan (cycle de 4)
auto_index = ((p_id - 1) % 4)

tab1, tab2, tab3 = st.tabs(["🖼️ DÉCOR", "🎨 IMAGE", "🎞️ VIDÉO"])

with tab1:
    st.subheader("⚙️ Paramètres du Décor")
    # Affichage du lieu précis (Colonne H)
    b5_val = st.selectbox("DÉCOR PRÉCIS (E5)", clean_decors, index=auto_index if auto_index < len(clean_decors) else 0)
    
    # Reste des menus (On utilise les colonnes de Lists)
    b7_val = st.selectbox("TIME OF DAY", L_DF['Time_of_day_EN'].dropna().unique(), disabled=not e7_bool)
    b8_val = st.selectbox("WEATHER", L_DF['Weather_EN'].dropna().unique(), disabled=not e7_bool)
    
    st.code(f"PROMPT: {b5_val} in {v_id} during {b7_val}, weather: {b8_val}")

# --- (Le reste du code pour les onglets 2 et 3 reste identique) ---
