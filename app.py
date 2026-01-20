import streamlit as st
import pandas as pd
import io

# =========================================================
# 1. INITIALISATION
# =========================================================
st.set_page_config(page_title="Melo Studio V71", layout="wide")

if 'melo_db' not in st.session_state:
    st.session_state.melo_db = None

# =========================================================
# 2. CHARGEMENT
# =========================================================
with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    file = st.file_uploader("Étape 1 : Charger l'Excel", type="xlsx")
    
    if file and st.session_state.melo_db is None:
        try:
            # Chargement forcé des onglets
            xl = pd.ExcelFile(file)
            df_lieux = xl.parse("BASE_LIEUX")
            df_plans = xl.parse("PLAN_DE_REALISATION")
            df_lists = xl.parse("Lists")

            st.session_state.melo_db = {
                "lieux": df_lieux,
                "plans": df_plans,
                "lists": df_lists
            }
            st.rerun()
        except Exception as e:
            st.error(f"Erreur technique : {e}")

if not st.session_state.melo_db:
    st.info("👋 En attente du fichier Excel...")
    st.stop()

# --- RÉCUPÉRATION ---
DB = st.session_state.melo_db
df_lieux = DB["lieux"]
df_plans = DB["plans"]
df_lists = DB["lists"]

# =========================================================
# 3. BARRE LATÉRALE (PILOTAGE)
# =========================================================
with st.sidebar:
    st.divider()
    e7_bool = st.toggle("🕹️ MODE MANUEL", value=False)
    
    # 1. Sélection de la Destination
    col_ville = 'LieuKey' if 'LieuKey' in df_lieux.columns else df_lieux.columns[0]
    v_id = st.selectbox("DESTINATION (B9)", df_lieux[col_ville].unique())
    
    # 2. Sélection du Plan
    p_id = st.select_slider("NUMÉRO DU PLAN", options=df_plans['Plan_ID'].unique())

    st.divider()

    # --- LOGIQUE DE DÉTECTION COLONNE H (Index 7) ---
    # On regarde ce qu'il y a dans la colonne H de la feuille Lists
    try:
        col_h_data = df_lists.iloc[:, 7].dropna().astype(str).tolist()
        
        # Filtrage ultra-souple : on cherche juste si le nom de la ville est dans le texte
        clean_names = []
        for d in col_h_data:
            if v_id.lower() in d.lower():
                # On coupe au premier tiret ou espace pour ne garder que le nom propre
                # On gère les deux types de tirets possibles (court et long)
                name_only = d.replace('–', '-').split('-')[-1].strip()
                clean_names.append(name_only)
        
        # AFFICHAGE DU SÉLECTEUR
        if clean_names:
            auto_idx = ((p_id - 1) % len(clean_names))
            e5_val = st.selectbox("📍 DÉCOR PRÉCIS (E5)", clean_names, index=auto_idx, disabled=not e7_bool)
        else:
            st.error(f"❌ Aucun décor trouvé pour '{v_id}' dans la colonne H.")
            st.write("Voici les 5 premières lignes lues dans la colonne H :")
            st.write(col_h_data[:5])
            e5_val = "Inconnu"
            
    except Exception as e:
        st.error(f"Erreur colonne H : {e}")
        e5_val = "Erreur"

# =========================================================
# 4. AFFICHAGE DU RÉSULTAT (ONGLET 1)
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ DÉCOR", "🎨 IMAGE", "🎞️ VIDÉO"])

with tab1:
    st.subheader(f"Décor sélectionné : {e5_val}")
    st.write(f"Ce décor est lié à la destination : **{v_id}**")
    
    # Construction du prompt pour vérifier que tout passe
    st.success("✅ Prompt généré :")
    st.code(f"Environment: {e5_val} located in {v_id}. Cinematic style, high detail.")

with tab2:
    # On affiche l'action pour vérifier que le scénario est lu
    plan_row = df_plans[df_plans['Plan_ID'] == p_id].iloc[0]
    st.write("Action Mélo (Variante A) :")
    st.info(plan_row.get('A_Melo_Action_EN', 'Action non trouvée'))
