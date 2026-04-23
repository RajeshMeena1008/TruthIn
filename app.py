
from image_utils import load_model, predict_food

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import io
from openfoodfacts_utils import get_product_by_barcode
from image_utils import load_model, predict_food
from ocr_utils import extract_text_from_image, parse_nutrition_from_text
from barcode_utils import scan_barcode, fetch_product_from_openfoodfacts
from scoring import compute_health_score, classify_score, get_recommendations, get_goal_verdict
from database import init_db, save_scan, get_history
from report import generate_pdf_report
import utils

# ─── INIT ────────────────────────────────────────────────────────────────────────
init_db()

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TruthIn",
    page_icon="🪽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* 🔥 MAKE TEXT PREMIUM WHITE */
html, body, [class*="css"] {
    color: #f8fafc !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
}

/* Labels */
label {
    color: #f8fafc !important;
}

/* Radio text */
.stRadio label {
    color: #f8fafc !important;
}

/* File uploader */
.stFileUploader label {
    color: #f8fafc !important;
}

/* Paragraph */
p {
    color: #f8fafc !important;
}

/* Small text */
span {
    color: #f8fafc !important;
}
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #222636;
    --surface3: #2a2f42;
    --accent-green: #22c55e;
    --accent-red: #ef4444;
    --accent-yellow: #f59e0b;
    --accent-blue: #3b82f6;
    --accent-purple: #a855f7;
    --text: #f0f2f8;
    --text-muted: #8891a8;
    --border: #2d3348;
    --border2: #363d55;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
h1,h2,h3,h4,h5,h6 { font-family: 'Nunito', sans-serif !important; }
.stApp { background-color: var(--bg) !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12151f 0%, #1a1d2e 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #c4c9db !important;
    font-size: 14px !important;
    padding: 4px 0 !important;
    transition: color 0.2s !important;
}
section[data-testid="stSidebar"] .stRadio label:hover { color: #22c55e !important; }
section[data-testid="stSidebar"] .stSelectbox label { color: #8891a8 !important; font-size: 11px !important; }

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 14px;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.card:hover {
    border-color: var(--border2);
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}
.card-accent-green  { border-left: 4px solid var(--accent-green) !important; }
.card-accent-yellow { border-left: 4px solid var(--accent-yellow) !important; }
.card-accent-red    { border-left: 4px solid var(--accent-red) !important; }

/* ── Score ring ── */
.score-wrap { text-align:center; }
.score-num { font-family:'Nunito',sans-serif; font-size:72px; font-weight:900; line-height:1; }
.score-sub { font-size:13px; color:var(--text-muted); margin-top:4px; }

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 5px 16px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-healthy  { background:rgba(34,197,94,0.15);  color:#22c55e; border:1px solid #22c55e; }
.badge-moderate { background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid #f59e0b; }
.badge-unhealthy{ background:rgba(239,68,68,0.15);  color:#ef4444; border:1px solid #ef4444; }

/* ── Tags ── */
.harm-tag {
    display:inline-block; background:rgba(239,68,68,0.12);
    color:#ef4444; border:1px solid rgba(239,68,68,0.4);
    border-radius:6px; padding:3px 10px; font-size:12px; margin:3px;
}
.safe-tag {
    display:inline-block; background:rgba(34,197,94,0.1);
    color:#22c55e; border:1px solid rgba(34,197,94,0.35);
    border-radius:6px; padding:3px 10px; font-size:12px; margin:3px;
}

/* ── Tip box ── */
.tip { background:rgba(34,197,94,0.06); border-left:3px solid #22c55e;
       padding:11px 15px; border-radius:0 8px 8px 0;
       font-size:13.5px; color:var(--text); margin:7px 0; }
.warn { background:rgba(239,68,68,0.06); border-left:3px solid #ef4444;
        padding:11px 15px; border-radius:0 8px 8px 0;
        font-size:13.5px; color:var(--text); margin:7px 0; }

/* ── Inputs ── */
.stTextInput>div>input, .stTextArea>div>textarea {
    background: var(--surface2) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 10px !important; font-size:14px !important;
}
.stTextInput>div>input:focus { border-color: #22c55e !important; box-shadow: 0 0 0 2px rgba(34,197,94,0.2) !important; }

/* ── Buttons ── */
.stButton>button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: #000 !important; font-family:'Nunito',sans-serif !important;
    font-weight:800 !important; border:none !important;
    border-radius:10px !important; padding:10px 28px !important;
    font-size:14px !important; letter-spacing:0.02em !important;
    transition: all 0.2s !important;
}
.stButton>button:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(34,197,94,0.35) !important; }

/* ── Progress bar ── */
div[data-testid="stProgress"]>div>div {
    background: linear-gradient(90deg,#22c55e,#3b82f6) !important;
    border-radius:99px !important;
}

/* ── Dataframe ── */
.dataframe, table { color:var(--text) !important; }
.stDataFrame { background:var(--surface) !important; border-radius:12px !important; }

/* ── Divider ── */
hr { border-color:var(--border) !important; margin:16px 0 !important; }

/* ── Stat row ── */
.stat-row { display:flex; gap:16px; margin:12px 0; flex-wrap:wrap; }
.stat-box {
    flex:1; min-width:100px;
    background:var(--surface2); border:1px solid var(--border);
    border-radius:12px; padding:14px 16px; text-align:center;
}
.stat-val { font-family:'Nunito',sans-serif; font-size:22px; font-weight:800; }
.stat-lbl { font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.06em; margin-top:2px; }

/* ── Upload zone ── */
.stFileUploader { background:var(--surface) !important; border:2px dashed var(--border2) !important; border-radius:14px !important; }
.stFileUploader:hover { border-color:#22c55e !important; }

/* ── Page header ── */
.page-header { font-family:'Nunito',sans-serif; font-size:28px; font-weight:900; letter-spacing:-0.02em; margin-bottom:2px; }
.page-sub { font-size:14px; color:var(--text-muted); margin-bottom:18px; }

/* ── Metric delta ── */
[data-testid="metric-container"] { background:var(--surface2) !important; border-radius:12px !important; padding:12px 16px !important; border:1px solid var(--border) !important; }

/* ── Goal verdict ── */
.goal-good { background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.5); border-radius:12px; padding:14px 18px; color:#22c55e; font-weight:700; font-size:15px; }
.goal-bad  { background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.5); border-radius:12px; padding:14px 18px; color:#ef4444; font-weight:700; font-size:15px; }

/* ── Ingredients box ── */
.ing-box { background:var(--surface2); border:1px solid var(--border); border-radius:10px; padding:12px 16px; font-size:13px; color:var(--text-muted); line-height:1.7; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:16px 0 8px 0;">
        <div style="font-size:40px">🍔</div>
        <div style="font-family:'Nunito',sans-serif; font-size:22px; font-weight:900;
                    background:linear-gradient(135deg,#22c55e,#3b82f6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; letter-spacing:-0.02em;">
            TruthIn
        </div>
        <div style="font-size:11px; color:#8891a8; margin-top:2px;">Nutrition Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠 Home", "📷 Image Scan", "📦 Packaged Food", "📜 History", "📊 Insights"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # ── GOAL SELECTOR ────────────────────────────────────────────────────────────
    st.markdown('<div style="font-size:11px;color:#8891a8;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">🎯 My Health Goal</div>', unsafe_allow_html=True)
    user_goal = st.selectbox(
        "goal",
        ["⚖️ General Health", "🏃 Weight Loss", "💪 Weight Gain"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div style="font-size:11px; color:#8891a8; text-align:center;">Powered by TF + OpenFoodFacts</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# HELPER: render result block (shared by Image Scan + Packaged Food)
# ════════════════════════════════════════════════════════════════════════════════
def render_result(food_name: str, nutrition: dict, ingredients: str, scan_type: str):
    """Render score, badge, goal verdict, ingredients, recommendations, PDF."""
    harmful, safe = utils.analyze_ingredients(ingredients)
    score = compute_health_score(nutrition, has_harmful=bool(harmful))
    label_cls = classify_score(score)

    color_map = {"Healthy": "#22c55e", "Moderate": "#f59e0b", "Unhealthy": "#ef4444"}
    badge_map = {"Healthy": "badge-healthy", "Moderate": "badge-moderate", "Unhealthy": "badge-unhealthy"}
    card_map  = {"Healthy": "card-accent-green", "Moderate": "card-accent-yellow", "Unhealthy": "card-accent-red"}
    color = color_map[label_cls]
    badge = badge_map[label_cls]
    card  = card_map[label_cls]

    recs = get_recommendations(nutrition, label_cls)
    goal_key = user_goal.split(" ", 1)[-1]  # strip emoji
    verdict, verdict_ok = get_goal_verdict(nutrition, goal_key)

    # ── Score + Goal ─────────────────────────────────────────────────────────────
    left, right = st.columns([1, 1.5])

    with left:
        st.markdown(f"""
        <div class="card {card}" style="text-align:center; padding:28px 16px;">
            <div class="score-num" style="color:{color}">{score}</div>
            <div class="score-sub">/ 100 Health Score</div>
            <div style="margin-top:12px"><span class="badge {badge}">{label_cls}</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(score / 100)

        # Goal verdict
        if goal_key != "General Health":
            cls = "goal-good" if verdict_ok else "goal-bad"
            icon = "✅" if verdict_ok else "❌"
            st.markdown(f'<div class="{cls}" style="margin-top:10px">{icon} {verdict}</div>', unsafe_allow_html=True)

    with right:
        # Nutrition stats
        cal  = nutrition.get("calories", 0)
        fat  = nutrition.get("fat", 0)
        sug  = nutrition.get("sugar", 0)
        prot = nutrition.get("protein", 0)
        sod  = nutrition.get("sodium", 0)
        carb = nutrition.get("carbohydrates", 0)

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-box"><div class="stat-val">{cal:.0f}</div><div class="stat-lbl">Cal</div></div>
            <div class="stat-box"><div class="stat-val">{fat:.1f}g</div><div class="stat-lbl">Fat</div></div>
            <div class="stat-box"><div class="stat-val">{sug:.1f}g</div><div class="stat-lbl">Sugar</div></div>
            <div class="stat-box"><div class="stat-val">{prot:.1f}g</div><div class="stat-lbl">Protein</div></div>
        </div>
        <div class="stat-row">
            <div class="stat-box"><div class="stat-val">{sod:.0f}mg</div><div class="stat-lbl">Sodium</div></div>
            <div class="stat-box"><div class="stat-val">{carb:.1f}g</div><div class="stat-lbl">Carbs</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Recommendations
        if recs:
            st.markdown('<div style="margin-top:6px">', unsafe_allow_html=True)
            for r in recs:
                box_cls = "warn" if any(w in r for w in ["High","excess","Unhealthy","limit","Excess"]) else "tip"
                st.markdown(f'<div class="{box_cls}">{r}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Ingredients ──────────────────────────────────────────────────────────────
    st.markdown("#### 🧪 Ingredients")
    display_ing = ingredients if ingredients.strip() else utils.get_default_ingredients(food_name)

    if harmful:
        st.markdown("**⚠️ Harmful detected:** " + " ".join([f'<span class="harm-tag">{h}</span>' for h in harmful]), unsafe_allow_html=True)
    if safe:
        st.markdown("**✅ Positives:** " + " ".join([f'<span class="safe-tag">{s}</span>' for s in safe[:6]]), unsafe_allow_html=True)

    if display_ing:
        st.markdown(f'<div class="ing-box">{display_ing}</div>', unsafe_allow_html=True)
    else:
        st.caption("Ingredient data not available for this item.")

    # ── Save + PDF ────────────────────────────────────────────────────────────────
    save_scan(food_name, score, scan_type)
    pdf_bytes = generate_pdf_report(food_name, nutrition, score, label_cls, recs)
    st.download_button("📄 Download PDF Report", pdf_bytes,
                       file_name=f"foodscan_{food_name.replace(' ','_')}.pdf",
                       mime="application/pdf")


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ════════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("""
    <div style="padding:16px 0 8px 0">
        <div style="font-family:'Nunito',sans-serif; font-size:48px; font-weight:900;
                    letter-spacing:-0.03em; line-height:1.05;
                    background:linear-gradient(135deg,#22c55e 0%,#3b82f6 50%,#a855f7 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            TruthIn
        </div>
        <div style="font-size:16px; color:#8891a8; margin-top:6px;">
            Intelligent nutrition analysis powered by deep learning.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, title, desc, clr in zip(
        [c1,c2,c3,c4],
        ["📷","📦","🎯","📊"],
        ["Image Detection","Packaged Food","Goal Tracking","Insights"],
        ["MobileNetV2 AI","OCR + OpenFoodFacts API","Weight Loss / Gain","PDF Reports & Charts"],
        ["#22c55e","#3b82f6","#f59e0b","#a855f7"]
    ):
        col.markdown(f"""
        <div class="card" style="border-top:3px solid {clr}; text-align:center; padding:24px 16px;">
            <div style="font-size:32px">{icon}</div>
            <div style="font-family:'Nunito',sans-serif; font-weight:800; font-size:14px; margin:10px 0 4px 0; color:{clr}">{title}</div>
            <div style="font-size:12px; color:#8891a8">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 How It Works")
    steps = [
        ("1","Upload or Search","Upload a food image or enter a product name."),
        ("2","AI Analysis","Deep learning or API fetches nutrition data instantly."),
        ("3","Health Score","Get a 0–100 score with Healthy / Moderate / Unhealthy status."),
        ("4","Goal Verdict","See if food fits your Weight Loss or Weight Gain goal."),
    ]
    cols = st.columns(4)
    for col, (num, title, desc) in zip(cols, steps):
        col.markdown(f"""
        <div class="card" style="text-align:center; padding:20px 14px;">
            <div style="font-family:'Nunito',sans-serif; font-size:28px; font-weight:900; color:#22c55e">{num}</div>
            <div style="font-weight:700; font-size:13px; margin:6px 0 4px 0">{title}</div>
            <div style="font-size:12px; color:#8891a8">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: IMAGE SCAN
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📷 Image Scan":
    st.markdown('<div class="page-header">📷 Food Image Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Upload any food photo for deep learning–based detection & nutrition analysis.</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Food Image", type=["jpg","jpeg","png","webp"])

    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        img_col, result_col = st.columns([1, 1.3])

        with img_col:
            st.image(img, caption="Uploaded Image")

        with result_col:
            with st.spinner("🤖 Running AI inference..."):
                model = load_model()
                
                predictions = predict_food(model, img)

            st.markdown("#### 🔍 Top Predictions")
            for i, (label, conf) in enumerate(predictions):
                medal = ["🥇","🥈","🥉"][i]
                c1, c2 = st.columns([2,1])
                c1.markdown(f"**{medal} {label}**")
                c2.caption(f"{conf:.1f}%")
                st.progress(int(min(conf, 100)) / 100)
                

        # Results block
        top_label = predictions[0][0]
        nutrition = utils.get_estimated_nutrition(top_label)
        ingredients = utils.get_default_ingredients(top_label)

        st.markdown("---")
        st.markdown(f"### 🍽️ Detected: **{top_label}**")
        render_result(top_label, nutrition, ingredients, "image_scan")

        # Full nutrition table
        st.markdown("---")
        st.markdown("#### 📋 Full Nutrition Table (per 100g)")
        df = pd.DataFrame([{k: v for k, v in nutrition.items() if k != "ingredients"}])
        st.dataframe(df, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: PACKAGED FOOD
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📦 Packaged Food":

    # ✅ Header
    st.markdown('<div class="page-header">📦 Packaged Food Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Scan label via OCR, barcode, or search by product name.</div>', unsafe_allow_html=True)

    # ✅ ONLY ONE Input Method
    method = st.radio(
        "Input Method",
        ["🔤 Enter Product Name", "📷 Upload Label (OCR)", "🔲 Barcode Scan"],
        horizontal=True
    )

    
    product_data = None
    product_name = None
    raw_ingredients = ""

    # ── Manual Name Entry ─────────────────────────────────────────────────────────
    if method == "🔤 Enter Product Name":
        col_input, col_btn = st.columns([4,1])
        with col_input:
            product_name_input = st.text_input(
                "Product name",
                placeholder="e.g. Maggi Noodles, Oreo, Lays, Cadbury",
                label_visibility="collapsed"
            )
        with col_btn:
            search_clicked = st.button("🔍 Search", use_container_width=True)

        if search_clicked and product_name_input:
            name_clean = product_name_input.strip()
            if len(name_clean) < 2:
                st.error("❌ Please enter a valid product name (at least 2 characters).")
                st.stop()

            with st.spinner(f"Searching for **{name_clean}**..."):
                product_data, fetched_name = fetch_product_from_openfoodfacts(None, name_clean)

            # Use fetched name if clean, else keep what user typed
            if fetched_name and len(fetched_name.strip()) > 1:
                product_name = fetched_name.strip()
            else:
                product_name = name_clean

            if not product_data:
                # Fallback to local DB
                product_data = utils.get_local_product_fallback(name_clean)
                if product_data:
                    st.info(f"ℹ️ Showing estimated data for **{product_name}**.")
                else:
                    st.error(f"❌ Could not find nutrition data for **{name_clean}**. Try a different spelling.")
                    st.stop()

            raw_ingredients = product_data.get("ingredients", "")

    # ── OCR Upload ────────────────────────────────────────────────────────────────
    elif method == "📷 Upload Label (OCR)":
        uploaded = st.file_uploader("Upload Nutrition Label Image", type=["jpg","jpeg","png"])
        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.image(img, width=300)
            with st.spinner("🔍 Extracting text via OCR..."):
                raw_text = extract_text_from_image(img)
                product_data = parse_nutrition_from_text(raw_text)
            product_name = "Scanned Label Product"
            raw_ingredients = product_data.get("ingredients", "")
            with st.expander("📝 Raw OCR Text"):
                st.code(raw_text)

    # ── Barcode ───────────────────────────────────────────────────────────────────
    else:
        uploaded = st.file_uploader("Upload Packaged Food Image (with barcode)", type=["jpg","jpeg","png"])
        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.image(img, width=300)
            with st.spinner("🔎 Scanning barcode..."):
                barcode = scan_barcode(img)
            if barcode:
                st.success(f"✅ Barcode: `{barcode}`")
                with st.spinner("🌐 Fetching from OpenFoodFacts..."):
                    product_data, product_name = fetch_product_from_openfoodfacts(barcode)
                raw_ingredients = (product_data or {}).get("ingredients", "")
                if not product_data:
                    st.warning("Product not found in database.")
            else:
                st.warning("⚠️ No barcode detected. Try the 'Enter Product Name' method.")

    # ── RESULTS ──────────────────────────────────────────────────────────────────
    if product_data and product_name:
        st.markdown("---")

        # Clean product name — only the name, nothing else
        clean_name = product_name.split("\n")[0].strip()
        clean_name = clean_name[:80]  # cap at 80 chars

        st.markdown(f"""
        <div class="card" style="padding:18px 24px; margin-bottom:18px;">
            <div style="font-size:11px; color:#8891a8; text-transform:uppercase; letter-spacing:0.1em; font-weight:700;">Product Detected</div>
            <div style="font-family:'Nunito',sans-serif; font-size:24px; font-weight:900; margin-top:4px;">{clean_name}</div>
        </div>
        """, unsafe_allow_html=True)

        render_result(clean_name, product_data, raw_ingredients, "packaged_food")


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: HISTORY
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📜 History":
    st.markdown('<div class="page-header">📜 Scan History</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">All your previous food scans, tracked automatically.</div>', unsafe_allow_html=True)

    rows = get_history()
    if rows:
        df = pd.DataFrame(rows, columns=["ID","Food Name","Health Score","Scan Type","Timestamp"])
        df["Status"] = df["Health Score"].apply(classify_score)

        # Summary metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Scans", len(df))
        c2.metric("Avg Score", f"{df['Health Score'].mean():.0f}/100")
        c3.metric("Healthy Items", (df["Status"] == "Healthy").sum())
        c4.metric("Unhealthy Items", (df["Status"] == "Unhealthy").sum())

        st.markdown("---")
        st.dataframe(df.drop("ID", axis=1), use_container_width=True, hide_index=True)

        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        fig = px.line(df, x="Timestamp", y="Health Score",
                      title="Health Score Over Time",
                      color_discrete_sequence=["#22c55e"],
                      template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          title_font=dict(family="Nunito", size=16))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:48px; color:#8891a8;">
            <div style="font-size:48px">📭</div>
            <div style="margin-top:12px; font-size:16px">No scans yet.</div>
            <div style="font-size:13px; margin-top:6px">Go to Image Scan or Packaged Food to get started.</div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE: INSIGHTS
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📊 Insights":
    st.markdown('<div class="page-header">📊 Nutrition Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Visual breakdown of your food scan history.</div>', unsafe_allow_html=True)

    rows = get_history()
    if rows:
        df = pd.DataFrame(rows, columns=["ID","Food Name","Health Score","Scan Type","Timestamp"])
        df["Status"] = df["Health Score"].apply(classify_score)

        col1, col2 = st.columns(2)
        with col1:
            pie = df["Status"].value_counts().reset_index()
            pie.columns = ["Status","Count"]
            fig = px.pie(pie, names="Status", values="Count",
                         title="Classification Distribution",
                         color="Status",
                         color_discrete_map={"Healthy":"#22c55e","Moderate":"#f59e0b","Unhealthy":"#ef4444"},
                         template="plotly_dark", hole=0.4)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font=dict(family="Nunito",size=15))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            bar = px.bar(df.tail(12), x="Food Name", y="Health Score",
                         title="Recent Scans – Health Score",
                         color="Health Score",
                         color_continuous_scale=["#ef4444","#f59e0b","#22c55e"],
                         template="plotly_dark")
            bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              title_font=dict(family="Nunito",size=15),
                              xaxis_tickangle=-35)
            st.plotly_chart(bar, use_container_width=True)

        hist = px.histogram(df, x="Health Score", nbins=10,
                            title="Score Distribution",
                            color_discrete_sequence=["#3b82f6"],
                            template="plotly_dark")
        hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           title_font=dict(family="Nunito",size=15))
        st.plotly_chart(hist, use_container_width=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:48px; color:#8891a8;">
            <div style="font-size:48px">📈</div>
            <div style="margin-top:12px">No data yet. Scan foods to see insights!</div>
        </div>
        """, unsafe_allow_html=True)
