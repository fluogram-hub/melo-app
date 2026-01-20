
import streamlit as st
import streamlit as st
import os, json, hashlib, re, html
import requests

# =========================================================
# TRANSLATION ENGINE (FR -> EN) + CACHE (REST)
# =========================================================

TRANSLATION_CACHE_PATH = "translation_cache_fr_en.json"

def load_translation_cache(path=TRANSLATION_CACHE_PATH) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_translation_cache(cache: dict, path=TRANSLATION_CACHE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def _sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()

def fr_to_en(text_fr: str, cache: dict) -> str:
    if not text_fr:
        return ""
    t = str(text_fr).strip()
    if not t:
        return ""

    key = _sha1(t)
    if key in cache:
        return cache[key]

    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing GOOGLE_TRANSLATE_API_KEY env var")

    url = "https://translation.googleapis.com/language/translate/v2"
    payload = {"q": t, "source": "fr", "target": "en", "format": "text", "key": api_key}

    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    out = r.json()["data"]["translations"][0]["translatedText"]
    out = html.unescape(out)
    out = re.sub(r"\s+", " ", out).strip()

    cache[key] = out
    save_translation_cache(cache)
    return out

def looks_french(s: str) -> bool:
    if not s:
        return False
    if re.search(r"[éèàùçêâîôûÉÈÀÙÇÊÂÎÔÛœŒ]", s):
        return True
    low = " " + s.lower() + " "
    markers = [" le ", " la ", " les ", " des ", " une ", " un ", " avec ", " sans ", " météo ", " décor ", " plan "]
    return any(m in low for m in markers)

def enforce_english_only(*prompts: str):
    for p in prompts:
        if looks_french(p):
            raise ValueError("French detected in prompt output")



# =========================================================
# ZONE 1 : CONFIGURATION GLOBALE (B22)
# =========================================================
B22_IDENTITY_LOCK = """MÉLO (LOCK — DO NOT CHANGE):
- MÉLO: Bunny-shaped high-end designer toy wearing a blue glossy suit with White round belly with yellow notes, white mitten-like paws.
- Same face, proportions, materials
- Wearing a blue glass suit (transparent blue glass effect), ultra glossy.
- Rounded child proportions.
- Keep ears visibility consistent.

PIPO (LOCK — DO NOT CHANGE):
- microscopic snow-potato companion; white with subtle iridescent multicolor reflections.
- Dot eyes and small smile; not an animal.
- Very tiny scale (≈5–10% of Mélo head height) and always close to Mélo.
- Soft constant glow; bedtime-friendly, minimal."""

# =========================================================
# ZONE 2 : DATA (À REMPLIR PLUS TARD - NE PAS SUPPRIMER)
# =========================================================
# Placeholder pour les 80 lieux
DB_DECORS = {
    "eiffel_paris": {
        "nom_fr": "La Tour Eiffel (Paris, France)",
        "decors": {
            1: {"fr": "Les Quais de Seine", "en": "Seine riverbanks", "cue": "Eiffel Tower clearly recognizable..."},
            2: {"fr": "Le Trocadéro", "en": "The Trocadéro", "cue": "Ultra-realistic cinematic PBR..."},
        }
    }
}

# Placeholder pour les 20 plans
PLANS_SEQ = {
    1: {
        "Angle": "Establishing wide shot", "Time": "morning", "Weather": "heavy rain", "Season": "summer",
        "M_Pose": "Melo sat on ground facing the camera", "M_Expr": "gentle connection",
        "P_Act": "Pipo floats gently", "P_Pos": "Pipo very close to Melo",
        "Acc": "flower", "Palette": "Dreamy Pastel", "P_Col": "Warm glow", "Trail": "sparkling dust trail",
        "V_Mode": "Non-loop cinematic", "V_Act": "Simple gesture", "V_M_Mvt": "Slow walk",
        "V_P_Mvt": "Slow circular float", "V_Cam": "Slow orbit", "V_Env": "Tiny dust particles", "V_Trans": "None"
    }
}

# Placeholder pour les 22 matières
MAT_MAP = {
    "🍭 SUCRERIES": ["Translucent colored jelly candy (glossy)", "Marshmallow foam"],
    "🧶 TEXTILES": ["Felted wool fabric", "Velvet microfabric"],
    "🧩 JOUETS": ["Lego", "Soft clay (matte)"]
}

# =========================================================
# ZONE 3 : LOGIQUE DE L'INTERFACE
# =========================================================
st.set_page_config(page_title="Melo Production V71", layout="wide")
translation_cache = load_translation_cache()

with st.sidebar:
    st.title("🎬 STUDIO MÉLO")
    e7_bool = st.toggle("🕹️ ACTIVER MODE MANUEL (E7)", value=False)
    
    st.divider()
    v_id = st.selectbox("DESTINATION (B9)", list(DB_DECORS.keys()), format_func=lambda x: DB_DECORS[x]['nom_fr'])
    p_id = st.select_slider("NUMÉRO DU PLAN", options=list(range(1, 21)))
    
    # Synchro Auto
    ville = DB_DECORS[v_id]
    plan = PLANS_SEQ.get(p_id, PLANS_SEQ[1])
    auto_b5_id = ((p_id - 1) % 4) + 1

tab1, tab2, tab3 = st.tabs(["🖼️ 1. DÉCOR (ENV)", "🎨 2. IMAGE (PERSOS)", "🎞️ 3. VIDÉO"])

# =========================================================
# ZONE 4 : ONGLET 1 - DÉCOR (Prompt 1 XLSX)
# =========================================================
with tab1:
    st.subheader("⚙️ Paramètres du Décor")
    c1, c2, c3 = st.columns(3)
    with c1:
        b5_val = st.selectbox("DÉCOR (E5)", list(ville['decors'].keys()), index=0, format_func=lambda x: ville['decors'][x]['fr'], disabled=not e7_bool)
        b6_val = st.selectbox("ANGLE (B6/I34)", ["Establishing wide shot", "Medium shot", "Close-up"], index=0, disabled=not e7_bool)
        b9_val = st.selectbox("SAISON (B9)", ["summer", "winter", "spring", "autumn"], index=0, disabled=not e7_bool)
    with c2:
        b7_val = st.selectbox("TIME OF DAY (B7/I35)", ["morning", "sunset", "night"], index=0, disabled=not e7_bool)
        b8_val = st.selectbox("WEATHER (B8)", ["heavy rain", "clear sky", "soft mist"], index=0, disabled=not e7_bool)
        b11_val = st.selectbox("1ER PLAN (B11)", ["none", "wild flowers", "leaves"], disabled=not e7_bool)
    with c3:
        d8_val = st.selectbox("MATÉRIEL D8", [m for sub in MAT_MAP.values() for m in sub], disabled=not e7_bool)
        d9_val = st.selectbox("MATÉRIEL D9", ["none", "Crystal sugar glow"], disabled=not e7_bool)
        b10_val = st.text_input("ÉTAT DU SOL (B10)", value="paved", disabled=not e7_bool)

    # FORMULE PROMPT 1
    e5_en = ville['decors'][b5_val]['en']
    b12_cue = ville['decors'][b5_val]['cue']
    d9_str = f" and {d9_val}" if d9_val != "none" else ""
    b11_str = f"In the immediate foreground, a subtle {b11_val} adds volumetric depth; " if b11_val != "none" else ""
    sugar = "sugar-coated crystalline textures" if "candy" in d8_val.lower() else "polished finishes"

    prompt_1 = (f"An ultra-detailed cinematic environment photography of {e5_en}. "
                f"The scene is set in {b9_val} during the {b7_val}, with a {b8_val} atmosphere. "
                f"The camera uses a {b6_val} with a low-angle ground perspective. {b11_str}"
                f"MATERIAL WORLD & SHADING: All surfaces reimagined in {d8_val}{d9_str}. "
                f"Surfaces feature realistic subsurface scattering and {sugar}. COMPOSITION: Minimalist. "
                f"GROUND DETAIL: {b10_val}. PLATE CUES (STRICT): {b12_cue}. RULES: Pure background plate.")
    st.code(prompt_1)

# =========================================================
# ZONE 5 : ONGLET 2 - IMAGE (Prompt 2 XLSX)
# =========================================================
with tab2:
    st.subheader("🎨 Intégration Personnages")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        s_pose = st.text_area("1. Pose Mélo (FR)", value=plan['M_Pose'], disabled=not e7_bool)
        s_expr = st.text_area("2. Expression de Mélo", value=plan['M_Expr'], disabled=not e7_bool)
    with r2:
        s_p_act = st.text_area("3. Pose Pipo (FR)", value=plan['P_Act'], disabled=not e7_bool)
        s_p_pos = st.text_input("4. Position Pipo (FR)", value=plan['P_Pos'], disabled=not e7_bool)
    with r3:
        s_acc = st.text_input("5. Melo Accessory", value=plan['Acc'], disabled=not e7_bool)
        s_pal = st.selectbox("6. Color Palette", ["Dreamy Pastel", "Natural"], disabled=not e7_bool)
    with r4:
        s_pcol = st.selectbox("7. Pipo Color", ["Warm glow", "Iridescent"], disabled=not e7_bool)
        s_trail = st.selectbox("8. Pipo Energy Trail", ["sparkling dust trail", "none"], disabled=not e7_bool)

    # Logique Météo
    weather_interaction = ""
    if any(word in b8_val.lower() for word in ["rain", "snow", "mist", "frost"]):
        weather_interaction = f"Add realistic water droplets or frost streaks on Mélo's glossy glass suit that reflect the {b7_val} light."

    prompt_2 = (f"IMAGE COMPOSITING TASK: Using Image 3 background, integrate Mélo and Pipo.\n\n"
                f"1. IDENTITY LOCK: {B22_IDENTITY_LOCK}. Accessory: {s_acc}.\n"
                f"2. LIGHTING: Palette: {s_pal}. Light must bounce onto Mélo’s glass suit. Material: {d8_val}. Trail: {s_trail}.\n"
                f"3. PHYSICAL INTERACTION: Condition: {b8_val}. {weather_interaction}\n"
                f"4. SCENE DIRECTION: Pose: {s_pose}. Expression: {s_expr}. Pipo: {s_p_act} at {s_p_pos}.")
    st.code(prompt_2)

# =========================================================
# ZONE 6 : ONGLET 3 - VIDÉO (Prompt 3 XLSX)
# =========================================================
with tab3:
    st.subheader("🎞️ Paramètres Vidéo")
    v1, v2, v3 = st.columns(3)
    with v1:
        vm = st.selectbox("1. Mode vidéo", ["Non-loop cinematic", "Perfect loop"], disabled=not e7_bool)
        va = st.selectbox("2. Type d’action", ["Simple gesture", "Still pose"], disabled=not e7_bool)
    with v2:
        vmm = st.selectbox("3. Mouvement de Mélo", ["Slow walk", "Breathing only"], disabled=not e7_bool)
        vpm = st.selectbox("4. Mouvement de Pipo", ["Slow circular float", "Tiny bounce"], disabled=not e7_bool)
    with v3:
        vcam = st.selectbox("5. Mouvement caméra", ["Slow orbit", "Locked camera"], disabled=not e7_bool)
        venv = st.selectbox("6. Mouvement environnement", ["Tiny dust particles", "None"], disabled=not e7_bool)

    prompt_3 = (f"VIDEO GENERATION PROMPT (FLOW / VEO3)\nMODE: Animate existing pixels. No reinterpretation.\n"
                f"SCENE LOCK: Angle: {b6_val}. Time: {b7_val}. Trail: {s_trail}.\n"
                f"REALISM LOCK: Material: {d8_val}. Duration: 8s. Mode: {vm}. Action: {va}. Melo: {vmm}. Pipo: {vpm}. Cam: {vcam}. Env: {venv}.\n"
                f"LOOP RULES: If mode = Perfect loop, motion must be continuous.")
    st.code(prompt_3)

# =========================================================
# ZONE 7 : MOTEUR RENDU
# =========================================================
st.divider()
if st.button("🚀 RENDU VERTEX ULTRA"):
    st.info("Connexion Vertex AI Imagen 3...")
