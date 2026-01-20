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
# ZONE 2 : MOTEUR DE DONNÉES & SESSION STATE
# =========================================================

# Initialisation sécurisée au tout début
if 'melo_db' not in st.session_state:
    st.session_state.melo_db = None
if 'lists' not in st.session_state:
    st.session_state.lists = {}
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}
if 'lieux' not in st.session_state:
    st.session_state.lieux = {}

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    uploaded_file = st.file_uploader("Charger 'MELO VALIDE' (XLSX)", type="xlsx")
    
    # On utilise .get() pour vérifier sans risquer l'AttributeError
    if uploaded_file and st.session_state.get('melo_db') is None:
        try:
            # Lecture des feuilles
            df_lieux = pd.read_excel(uploaded_file, sheet_name="BASE_LIEUX")
            df_plans = pd.read_excel(uploaded_file, sheet_name="PLAN_DE_REALISATION")
            df_lists = pd.read_excel(uploaded_file, sheet_name="Lists")

            # Extraction des listes pour les menus déroulants
            st.session_state.lists = {col: df_lists[col].dropna().unique().tolist() for col in df_lists.columns}
            
            # Stockage du scénario et des lieux
            st.session_state.scenarios = df_plans.set_index('Plan_ID').to_dict(orient='index')
            st.session_state.lieux = df_lieux.set_index('LieuKey').to_dict(orient='index')
            
            st.session_state.melo_db = True
            st.success("✅ Studio synchronisé !")
            st.rerun() # On relance pour rafraîchir l'interface avec les données
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")
