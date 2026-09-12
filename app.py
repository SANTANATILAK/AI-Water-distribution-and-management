import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

st.set_page_config(
    page_title="AquaAI | Smart Water Management",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg,#06121c 0%,#071d2b 48%,#031018 100%); color:#f5fbff; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#071923,#041018); border-right:1px solid rgba(67,211,255,.16); }
.hero { padding: 34px 38px; border:1px solid rgba(67,211,255,.20); border-radius:24px; background:linear-gradient(135deg,rgba(8,55,76,.72),rgba(4,24,35,.82)); box-shadow:0 20px 60px rgba(0,0,0,.25); margin-bottom:24px; }
.hero h1 { font-size:42px; margin:0; font-weight:800; letter-spacing:-1px; }
.hero p { color:#a9c7d4; font-size:16px; margin-top:10px; }
.badge { display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(39,210,170,.12); color:#54e7c5; border:1px solid rgba(39,210,170,.25); font-size:12px; font-weight:700; letter-spacing:.5px; }
.card { padding:20px; border-radius:18px; background:rgba(9,31,43,.72); border:1px solid rgba(115,214,255,.12); min-height:120px; }
.card-title { color:#8fb4c3; font-size:13px; text-transform:uppercase; letter-spacing:1px; }
.card-value { font-size:28px; font-weight:800; margin-top:8px; }
.result { padding:26px; border-radius:20px; background:linear-gradient(135deg,rgba(0,133,174,.22),rgba(0,65,90,.16)); border:1px solid rgba(69,216,255,.30); text-align:center; }
.result-value { font-size:46px; font-weight:800; color:#56ddff; }
.small { color:#91afba; font-size:13px; }
div[data-testid="stMetric"] { background:rgba(9,31,43,.72); padding:16px; border-radius:16px; border:1px solid rgba(115,214,255,.12); }
.stButton > button { border-radius:12px; font-weight:700; border:1px solid rgba(69,216,255,.30); }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = Path(__file__).parent / "data" / "sample.csv"
    if path.exists():
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame({
            "Temperature": [30,32,35,28,25,33,31],
            "Population": [1000,1200,1500,900,800,1300,1100],
            "Water_Demand": [500,600,750,450,400,680,550],
        })
    required = {"Temperature", "Population", "Water_Demand"}
    if not required.issubset(df.columns):
        raise ValueError("Dataset must contain Temperature, Population and Water_Demand columns.")
    return df.dropna(subset=list(required)).copy()

@st.cache_resource
def train_model():
    df = load_data()
    X = df[["Temperature", "Population"]]
    y = df["Water_Demand"]
    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(X)
    return model, r2_score(y, pred), mean_absolute_error(y, pred)

try:
    df = load_data()
    model, r2, mae = train_model()
except Exception as e:
    st.error(f"Application startup error: {e}")
    st.stop()

with st.sidebar:
    st.markdown("## 💧 AquaAI")
    st.caption("Smart Water Distribution & Demand Management")
    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Predict Demand", "Data Explorer", "About"], index=0)
    st.markdown("---")
    st.markdown("**Model:** Linear Regression")
    st.markdown("**Inputs:** Temperature + Population")
    st.markdown("**Dataset:** Local CSV")

st.markdown("""
<div class="hero">
<span class="badge">AI-POWERED WATER MANAGEMENT</span>
<h1>Smart Water Distribution</h1>
<p>Predict water demand from temperature and population data and support smarter resource planning.</p>
</div>
""", unsafe_allow_html=True)

if page == "Dashboard":
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="card"><div class="card-title">Records</div><div class="card-value">{len(df):,}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card"><div class="card-title">Avg Demand</div><div class="card-value">{df.Water_Demand.mean():,.1f} L</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="card"><div class="card-title">Model R²</div><div class="card-value">{r2:.3f}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="card"><div class="card-title">MAE</div><div class="card-value">{mae:.2f} L</div></div>', unsafe_allow_html=True)
    st.markdown("### Demand Overview")
    chart = df[["Temperature", "Water_Demand"]].set_index("Temperature")
    st.line_chart(chart, height=330)
    st.markdown("### Recent Dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "Predict Demand":
    st.markdown("### 💧 Water Demand Predictor")
    left,right = st.columns([1,1])
    with left:
        temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=30.0, step=0.5)
        pop = st.number_input("Population", min_value=1.0, max_value=10000000.0, value=1000.0, step=100.0)
        predict = st.button("Predict Water Demand", type="primary", use_container_width=True)
    with right:
        if predict:
            prediction = float(model.predict(pd.DataFrame({"Temperature":[temp], "Population":[pop]}))[0])
            prediction = max(0.0, prediction)
            st.markdown(f'<div class="result"><div class="small">ESTIMATED DAILY WATER DEMAND</div><div class="result-value">{prediction:,.2f} L</div><div class="small">Based on temperature and population</div></div>', unsafe_allow_html=True)
            st.success("Prediction completed successfully.")
        else:
            st.info("Enter values and click Predict Water Demand.")
    st.markdown("### Model Information")
    a,b = st.columns(2)
    a.metric("R² Score", f"{r2:.3f}")
    b.metric("Mean Absolute Error", f"{mae:.2f} L")

elif page == "Data Explorer":
    st.markdown("### 📊 Dataset Explorer")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("### Statistics")
    st.dataframe(df.describe().round(2), use_container_width=True)
    st.markdown("### Water Demand by Temperature")
    st.bar_chart(df.set_index("Temperature")["Water_Demand"], height=350)

else:
    st.markdown("### About AquaAI")
    st.markdown("""
    **AquaAI** is a lightweight AI-based water demand prediction system designed to demonstrate how machine learning can support water resource planning.

    **How it works**
    1. Loads the project dataset from `data/sample.csv`.
    2. Trains a Linear Regression model using temperature and population.
    3. Predicts estimated water demand for new conditions.
    4. Presents the results through an interactive Streamlit dashboard.

    **Project stack:** Python, Pandas, NumPy, Scikit-learn and Streamlit.
    """)
    st.markdown("### Project Dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("<p class='small' style='text-align:center;margin-top:35px;'>AquaAI • AI Water Distribution & Management</p>", unsafe_allow_html=True)
