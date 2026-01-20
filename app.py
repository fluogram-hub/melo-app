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
            xl = pd.ExcelFile(file)
            st.session_state.melo_db = {
                "lieux": xl.parse("BASE_LIEUX"),
                "plans": xl.parse("PLAN_DE_REALISATION"),
                "lists": xl.parse("Lists")
            }
            st.rerun()
        except Exception as e:
            st.error(f"Erreur d'ouverture : {e}")

if not st.session_state.melo_db:
    st.info("👋 En attente du fichier Excel...")
    st.stop()

# --- RÉCUPÉRATION ---
df_lieux = st.session_state.melo_db["lieux"]
df_plans = st.session_state.melo_db["plans"]
df_lists = st.session_state.melo_db["lists"]

# =========================================================
# 3. BARRE LATÉRALE (PILOTAGE)
# =========================================================
with st.sidebar:
    st.divider()
    e7_bool = st.toggle("🕹️ MODE MANUEL", value=False)
    
    # 1. Sélection de la Destination
    v_id = st.selectbox("DESTINATION (B9)", df_lieux['LieuKey'].unique())
    
    # 2. Sélection du Plan
    p_id = st.select_slider("NUMÉRO DU PLAN", options=df_plans['Plan_ID'].unique())

    # --- LOGIQUE DÉCOR PRÉCIS (E5) ---
    # On cherche la colonne qui contient "Decor" dans son nom
    decor_col = next((c for c in df_lists.columns if 'decor' in c.lower()), None)
    
    if decor_col:
        all_val = df_lists[decor_col].dropna().astype(str).tolist()
        # On filtre les décors qui contiennent l'ID de la ville
        clean_names = [v.split('–')[-1].split('-')[-1].strip() for v in all_val if v_id.lower() in v.lower()]
        
        if clean_names:
            auto_idx = ((p_id - 1) % len(clean_names))
            e5_val = st.selectbox("📍 DÉCOR PRÉCIS (E5)", clean_names, index=auto_idx, disabled=not e7_bool)
        else:
            st.warning(f"Pas de décor trouvé pour {v_id}")
            e5_val = "Inconnu"
    else:
        st.error("Colonne 'Decor' introuvable dans l'onglet Lists")
        e5_val = "Erreur"

    st.divider()
    sc_ver = st.radio("VARIANTE", ["A", "B", "C"])

# =========================================================
# 4. AFFICHAGE (ONGLET 1)
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ DÉCOR", "🎨 IMAGE", "🎞️ VIDÉO"])

with tab1:
    st.header(f"Lieu : {e5_val}")
    st.write(f"Destination parente : {v_id}")
    
    # On génère le prompt final pour que tu puisses voir si ça marche
    st.subheader("📝 Prompt généré :")
    prompt = f"Cinematic shot of {e5_val} in {v_id}. Ultra-realistic, 8k."
    st.code(prompt)

with tab2:
    # Récupération de l'action Mélo
    plan_data = df_plans[df_plans['Plan_ID'] == p_id].iloc[0]
    action_col = f"{sc_ver}_Melo_Action_EN"
    st.info(f"Action Mélo : {plan_data.get(action_col, 'Non trouvée')}")
