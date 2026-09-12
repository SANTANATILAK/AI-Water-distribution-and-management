import streamlit as st
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

st.set_page_config(page_title="AquaAI - Water Management", page_icon="💧", layout="wide")

st.markdown("""
<style>
.stApp { background: #071923; color: #f5fbff; }
.block-container { padding-top: 2rem; }
.hero { padding: 28px; border-radius: 18px; background: #0b2b3a; border: 1px solid #1d5368; margin-bottom: 24px; }
.hero h1 { margin: 0; font-size: 38px; }
.hero p { color: #b4ced8; }
.card { padding: 18px; border-radius: 14px; background: #0b2633; border: 1px solid #1d5368; }
.value { font-size: 28px; font-weight: 700; }
.label { color: #8fb4c3; font-size: 13px; text-transform: uppercase; }
.result { padding: 25px; border-radius: 16px; background: #0b3547; border: 1px solid #2a91b5; text-align: center; }
.result-value { font-size: 42px; font-weight: 700; color: #58dcff; }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).parent / "data" / "sample.csv"
DEFAULT_DATA = pd.DataFrame({
    "Temperature": [30, 32, 35, 28, 25, 33, 31],
    "Population": [1000, 1200, 1500, 900, 800, 1300, 1100],
    "Water_Demand": [500, 600, 750, 450, 400, 680, 550]
})


def load_data():
    try:
        if DATA_PATH.exists():
            data = pd.read_csv(DATA_PATH)
            required = ["Temperature", "Population", "Water_Demand"]
            if all(column in data.columns for column in required):
                data = data[required].copy()
                for column in required:
                    data[column] = pd.to_numeric(data[column], errors="coerce")
                data = data.dropna().reset_index(drop=True)
                if len(data) >= 2:
                    return data
    except Exception:
        pass
    return DEFAULT_DATA.copy()


def build_model(data):
    model = LinearRegression()
    X = data[["Temperature", "Population"]]
    y = data["Water_Demand"]
    model.fit(X, y)
    prediction = model.predict(X)
    return model, r2_score(y, prediction), mean_absolute_error(y, prediction)

try:
    df = load_data()
    model, r2, mae = build_model(df)
except Exception as error:
    st.error("The application could not start.")
    st.exception(error)
    st.stop()

with st.sidebar:
    st.title("💧 AquaAI")
    st.caption("AI Water Distribution & Management")
    page = st.radio("Navigation", ["Dashboard", "Predict Demand", "Data Explorer", "About"])
    st.divider()
    st.write("**Model:** Linear Regression")
    st.write("**Records:**", len(df))

st.markdown("""
<div class="hero">
<h1>💧 Smart Water Distribution</h1>
<p>AI-powered water demand prediction using temperature and population.</p>
</div>
""", unsafe_allow_html=True)

if page == "Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="card"><div class="label">Records</div><div class="value">{len(df):,}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="label">Average Demand</div><div class="value">{df["Water_Demand"].mean():,.1f} L</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><div class="label">R² Score</div><div class="value">{r2:.3f}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="card"><div class="label">MAE</div><div class="value">{mae:.2f} L</div></div>', unsafe_allow_html=True)
    st.subheader("Water Demand Overview")
    chart = df[["Temperature", "Water_Demand"]].sort_values("Temperature").set_index("Temperature")
    st.line_chart(chart)
    st.subheader("Dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "Predict Demand":
    st.subheader("💧 Predict Water Demand")
    left, right = st.columns(2)
    with left:
        temperature = st.number_input("Temperature (°C)", 0.0, 60.0, 30.0, 0.5)
        population = st.number_input("Population", 1.0, 10000000.0, 1000.0, 100.0)
        predict = st.button("Predict Water Demand", type="primary", use_container_width=True)
    with right:
        if predict:
            input_df = pd.DataFrame({"Temperature": [temperature], "Population": [population]})
            result = max(0.0, float(model.predict(input_df)[0]))
            st.markdown(f'<div class="result"><div>ESTIMATED WATER DEMAND</div><div class="result-value">{result:,.2f} L</div><div>per day</div></div>', unsafe_allow_html=True)
        else:
            st.info("Enter temperature and population, then click Predict Water Demand.")
    st.subheader("Model Performance")
    a, b = st.columns(2)
    a.metric("R² Score", f"{r2:.3f}")
    b.metric("Mean Absolute Error", f"{mae:.2f} L")

elif page == "Data Explorer":
    st.subheader("📊 Data Explorer")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader("Statistics")
    st.dataframe(df.describe().round(2), use_container_width=True)
    st.subheader("Demand by Temperature")
    chart = df[["Temperature", "Water_Demand"]].sort_values("Temperature").set_index("Temperature")
    st.bar_chart(chart)

else:
    st.subheader("About AquaAI")
    st.write("AquaAI demonstrates how machine learning can support water resource planning by estimating water demand from temperature and population.")
    st.markdown("**Technology:** Python, Streamlit, Pandas, Scikit-learn")
    st.markdown("**Model:** Linear Regression")
    st.markdown("**Inputs:** Temperature and Population")
    st.dataframe(df, use_container_width=True, hide_index=True)

st.caption("AquaAI • AI Water Distribution & Management")
