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
    file = st.file_uploader("Charger l'Excel Maître", type="xlsx")
    
    if file and st.session_state.melo_db is None:
        try:
            df_lieux = pd.read_excel(file, sheet_name="BASE_LIEUX")
            df_plans = pd.read_excel(file, sheet_name="PLAN_DE_REALISATION")
            df_lists = pd.read_excel(file, sheet_name="Lists")

            st.session_state.melo_db = {
                "lieux": df_lieux,
                "plans": df_plans,
                "lists": df_lists
            }
            st.rerun()
        except Exception as e:
            st.error(f"Erreur : {e}")

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
    
    # 1. Destination
    v_id = st.selectbox("DESTINATION (B9)", df_lieux['LieuKey'].unique())
    
    # 2. Plan
    p_id = st.select_slider("NUMÉRO DU PLAN", options=df_plans['Plan_ID'].unique())
    
    # 3. Variante
    sc_ver = st.radio("VARIANTE", ["A", "B", "C"])

    st.divider()
    
    # --- LOGIQUE DÉCOR PRÉCIS (COLONNE H) ---
    # On identifie la colonne H par son index (7) pour être sûr à 100%
    col_h_name = df_lists.columns[7] # La 8ème colonne
    all_decors = df_lists[col_h_name].dropna().astype(str).tolist()
    
    # Filtrage : On cherche les décors qui contiennent le nom de la ville
    # On utilise "in" au lieu de "startswith" pour plus de souplesse
    clean_names = []
    for d in all_decors:
        if v_id.lower() in d.lower():
            # On nettoie pour n'avoir que le lieu (après le tiret ou l'espace)
            name_only = d.split('–')[-1].split('-')[-1].strip()
            clean_names.append(name_only)
    
    # AFFICHAGE DU SÉLECTEUR E5
    if clean_names:
        auto_idx = ((p_id - 1) % len(clean_names))
        e5_val = st.selectbox("📍 DÉCOR PRÉCIS (E5)", clean_names, index=auto_idx, disabled=not e7_bool)
    else:
        st.warning(f"⚠️ Aucun décor trouvé pour {v_id} dans la colonne {col_h_name}")
        e5_val = "Décor inconnu"

    # Export
    st.divider()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_plans.to_excel(writer, index=False)
    st.download_button("💾 Sauvegarder Scénario", output.getvalue(), "melo_export.xlsx")

# =========================================================
# 4. ONGLETS D'ÉDITION
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ DÉCOR", "🎨 IMAGE", "🎞️ VIDÉO"])

with tab1:
    st.subheader(f"Environnement : {e5_val}")
    st.info(f"Ceci est le décor spécifique pour le plan {p_id}")
    # Menus simplifiés pour test
    b7 = st.selectbox("TIME", df_lists['Time_of_day_EN'].dropna().unique())
    st.code(f"PROMPT: {e5_val} / {v_id} / {b7}")

with tab2:
    st.subheader(f"Mise en scène (Variante {sc_ver})")
    # On récupère la ligne du plan
    idx = df_plans[df_plans['Plan_ID'] == p_id].index[0]
    col_melo = f"{sc_ver}_Melo_Action_EN"
    
    # Édition directe dans le DataFrame original
    df_plans.at[idx, col_melo] = st.text_area("Pose Mélo", value=str(df_plans.at[idx, col_melo]))
    
    st.code(f"ACTION: {df_plans.at[idx, col_melo]}")
