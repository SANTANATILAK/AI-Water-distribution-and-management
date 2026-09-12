import csv
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="AquaAI", page_icon="💧", layout="wide")

DEFAULT_DATA = [
    {"Temperature": 30.0, "Population": 1000.0, "Water_Demand": 500.0},
    {"Temperature": 32.0, "Population": 1200.0, "Water_Demand": 600.0},
    {"Temperature": 35.0, "Population": 1500.0, "Water_Demand": 750.0},
    {"Temperature": 28.0, "Population": 900.0, "Water_Demand": 450.0},
    {"Temperature": 25.0, "Population": 800.0, "Water_Demand": 400.0},
    {"Temperature": 33.0, "Population": 1300.0, "Water_Demand": 680.0},
    {"Temperature": 31.0, "Population": 1100.0, "Water_Demand": 550.0},
]


def load_data():
    path = Path(__file__).parent / "data" / "sample.csv"
    try:
        with path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        data = []
        for row in rows:
            data.append({
                "Temperature": float(row["Temperature"]),
                "Population": float(row["Population"]),
                "Water_Demand": float(row["Water_Demand"]),
            })
        return data if len(data) >= 2 else DEFAULT_DATA
    except Exception:
        return DEFAULT_DATA


def regression(rows):
    n = len(rows)
    sx = sum(r["Temperature"] for r in rows)
    sz = sum(r["Population"] for r in rows)
    sy = sum(r["Water_Demand"] for r in rows)
    sxx = sum(r["Temperature"] ** 2 for r in rows)
    szz = sum(r["Population"] ** 2 for r in rows)
    sxz = sum(r["Temperature"] * r["Population"] for r in rows)
    sxy = sum(r["Temperature"] * r["Water_Demand"] for r in rows)
    szy = sum(r["Population"] * r["Water_Demand"] for r in rows)
    a = [[n, sx, sz], [sx, sxx, sxz], [sz, sxz, szz]]
    b = [sy, sxy, szy]

    for i in range(3):
        pivot_row = max(range(i, 3), key=lambda j: abs(a[j][i]))
        a[i], a[pivot_row] = a[pivot_row], a[i]
        b[i], b[pivot_row] = b[pivot_row], b[i]
        pivot = a[i][i]
        if abs(pivot) < 1e-12:
            return 0.0, 0.0, sy / n
        for j in range(i, 3):
            a[i][j] /= pivot
        b[i] /= pivot
        for k in range(3):
            if k == i:
                continue
            factor = a[k][i]
            for j in range(i, 3):
                a[k][j] -= factor * a[i][j]
            b[k] -= factor * b[i]

    return b[1], b[2], b[0]


rows = load_data()
temp_coef, pop_coef, intercept = regression(rows)


def predict(temperature, population):
    value = intercept + temp_coef * temperature + pop_coef * population
    return max(0.0, value)


st.markdown("""
<style>
.stApp { background: #071923; }
.hero { padding: 28px; border-radius: 18px; background: #0b2b3a; border: 1px solid #1d5368; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("💧 AquaAI")
    page = st.radio("Navigation", ["Dashboard", "Predict Demand", "Data Explorer", "About"])
    st.divider()
    st.write("AI Water Distribution & Management")
    st.write("Records:", len(rows))

st.markdown(
    "<div class='hero'><h1>💧 Smart Water Distribution</h1><p>AI-powered water demand prediction and management.</p></div>",
    unsafe_allow_html=True,
)

if page == "Dashboard":
    average = sum(r["Water_Demand"] for r in rows) / len(rows)
    c1, c2, c3 = st.columns(3)
    c1.metric("Records", len(rows))
    c2.metric("Average Demand", f"{average:,.1f} L")
    c3.metric("Model", "Linear Regression")
    st.subheader("Water Demand Overview")
    st.line_chart({"Water Demand": [r["Water_Demand"] for r in rows]})
    st.subheader("Dataset")
    st.dataframe(rows, use_container_width=True)

elif page == "Predict Demand":
    st.subheader("💧 Predict Water Demand")
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=30.0, step=0.5)
    population = st.number_input("Population", min_value=1.0, max_value=10000000.0, value=1000.0, step=100.0)
    if st.button("Predict Water Demand", type="primary", use_container_width=True):
        result = predict(temperature, population)
        st.success("Prediction completed successfully")
        st.metric("Estimated Daily Water Demand", f"{result:,.2f} L")

elif page == "Data Explorer":
    st.subheader("📊 Data Explorer")
    st.dataframe(rows, use_container_width=True)
    st.subheader("Water Demand")
    st.bar_chart({"Water Demand": [r["Water_Demand"] for r in rows]})

else:
    st.subheader("About AquaAI")
    st.write("AquaAI demonstrates AI-based water demand prediction using temperature and population data.")
    st.write("Technology: Python and Streamlit")
    st.write("Model: Linear Regression")
    st.write("The app includes a fallback dataset, so it remains functional if the CSV is unavailable.")

st.caption("AquaAI • AI Water Distribution & Management")
