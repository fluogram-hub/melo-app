import streamlit as st
import pandas as pd
import io

# =========================================================
# ZONE 1 : CONFIGURATION GLOBALE & IDENTITÉ (LOCK)
# =========================================================
B22_IDENTITY_LOCK = """MÉLO (LOCK): Bunny-shaped high-end designer toy, blue glossy glass suit...
PIPO (LOCK): Microscopic snow-potato companion, iridescent reflections..."""

# =========================================================
# ZONE 2 : MOTEUR DE DONNÉES & SESSION STATE
# =========================================================
def init_data():
    """Initialise les structures de données dans la mémoire Streamlit."""
    if 'melo_data' not in st.session_state:
        st.session_state.melo_data = None

def load_excel(file):
    try:
        df_lieux = pd.read_excel(file, sheet_name="BASE_LIEUX")
        df_plans = pd.read_excel(file, sheet_name="PLANS")
        df_lists = pd.read_excel(file, sheet_name="Lists")

        # Reconstruction DB_DECORS (Lieux)
        db_decors = {}
        for _, row in df_lieux.iterrows():
            vid = str(row['ID_CITY']).strip()
            db_decors[vid] = {
                "nom_fr": row['CITY_NAME_FR'],
                "decors": {
                    i: {"fr": row[f'B5_{i}_NAME_FR'], "en": row[f'B5_{i}_NAME_EN'], "cue": row[f'B12_{i}_CUE']}
                    for i in range(1, 5)
                }
            }

        # Reconstruction PLANS_SEQ (Scénario)
        plans_seq = df_plans.set_index('PLAN_ID').to_dict(orient='index')

        # Reconstruction MAT_MAP (Matières)
        mat_map = df_lists.groupby('CATEGORY')['MATERIAL_NAME'].apply(list).to_dict()

        st.session_state.melo_data = {
            "decors": db_decors,
            "plans": plans_seq,
            "matieres": mat_map
        }
        st.success("✅ Fichier chargé et synchronisé !")
    except Exception as e:
        st.error(f"Erreur de lecture : {e}. Vérifiez les noms d'onglets et de colonnes.")

# --- SIDEBAR : CONTRÔLE ET EXPORT ---
st.set_page_config(page_title="Melo Production V71", layout="wide")
init_data()

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    uploaded_file = st.file_uploader("Charger Excel Maître", type="xlsx")
    if uploaded_file and st.session_state.melo_data is None:
        load_excel(uploaded_file)
    
    if st.session_state.melo_data:
        st.divider()
        e7_bool = st.toggle("🕹️ MODE ÉDITION MANUELLE", value=False)
        v_id = st.selectbox("DESTINATION", list(st.session_state.melo_data["decors"].keys()), 
                            format_func=lambda x: st.session_state.melo_data["decors"][x]['nom_fr'])
        p_id = st.select_slider("NUMÉRO DU PLAN", options=list(st.session_state.melo_data["plans"].keys()))
        
        # Bouton d'exportation pour sauvegarder vos modifs
        st.subheader("💾 SAUVEGARDE")
        df_exp = pd.DataFrame.from_dict(st.session_state.melo_data['plans'], orient='index')
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_exp.to_excel(writer, sheet_name='PLANS')
        st.download_button("Exporter Scénario Modifié", output.getvalue(), "melo_custom.xlsx")

if not st.session_state.melo_data:
    st.info("👋 Bienvenue. Veuillez charger le fichier Excel pour activer l'interface.")
    st.stop()

# --- LOGIQUE DE SYNCHRO ---
DATA = st.session_state.melo_data
ville = DATA["decors"][v_id]
plan = DATA["plans"][p_id]
auto_b5_id = ((p_id - 1) % 4) + 1

# =========================================================
# ZONE 3 : INTERFACE (ONGLETS)
# =========================================================
tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR", "🎨 2. IMAGE (ÉDITEUR)", "🎞️ 3. VIDÉO"])

with tab1:
    st.subheader("⚙️ Paramètres du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_val = st.selectbox("DÉCOR (E5)", [1,2,3,4], index=auto_b5_id-1, format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        b6_val = st.selectbox("ANGLE", ["Establishing wide shot", "Medium shot", "Close-up"], index=0, disabled=not e7_bool)
    with c2:
        b7_val = st.selectbox("TIME", ["morning", "sunset", "night"], index=0, disabled=not e7_bool)
        b8_val = st.selectbox("WEATHER", ["heavy rain", "clear sky", "soft mist"], index=0, disabled=not e7_bool)
    with c3:
        # Utilisation des matières chargées dynamiquement
        all_mats = [m for sub in DATA["matieres"].values() for m in sub]
        d8_val = st.selectbox("MATÉRIEL D8", all_mats, disabled=not e7_bool)

    # Prompt 1 (Calculé en temps réel)
    prompt_1 = f"Environment: {ville['decors'][b5_val]['en']}. Lighting: {b7_val}. Shading: {d8_val}."
    st.code(prompt_1)

with tab2:
    st.subheader("🎨 Pose & Expression (Modifiable en direct)")
    r1, r2 = st.columns(2)
    with r1:
        # MODIFICATION DIRECTE DU SESSION STATE
        plan['M_Pose'] = st.text_area("Pose Mélo", value=plan.get('M_Pose', ""))
        plan['M_Expr'] = st.text_area("Expression Mélo", value=plan.get('M_Expr', ""))
    with r2:
        plan['P_Act'] = st.text_area("Action Pipo", value=plan.get('P_Act', ""))
        plan['P_Pos'] = st.text_input("Position Pipo", value=plan.get('P_Pos', ""))

    prompt_2 = f"IDENTITY LOCK: {B22_IDENTITY_LOCK}\nDIRECTION: {plan['M_Pose']}, {plan['M_Expr']}. PIPO: {plan['P_Act']}."
    st.code(prompt_2)

with tab3:
    st.subheader("🎞️ Paramètres Vidéo")
    st.write(f"Mode actuel pour le plan {p_id} : {plan.get('V_Mode', 'N/A')}")
    st.code(f"VIDEO PROMPT: Action {plan.get('V_Act', 'None')}, Cam: {plan.get('V_Cam', 'Locked')}")

if st.button("🚀 RENDU VERTEX ULTRA"):
    st.info("Génération en cours avec les données éditées...")
