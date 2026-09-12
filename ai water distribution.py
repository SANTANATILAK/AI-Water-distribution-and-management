import streamlit as st

st.set_page_config(page_title="AquaAI", page_icon="💧", layout="wide")

DATA = [
    {"Temperature": 30, "Population": 1000, "Water Demand": 500},
    {"Temperature": 32, "Population": 1200, "Water Demand": 600},
    {"Temperature": 35, "Population": 1500, "Water Demand": 750},
    {"Temperature": 28, "Population": 900, "Water Demand": 450},
    {"Temperature": 25, "Population": 800, "Water Demand": 400},
    {"Temperature": 33, "Population": 1300, "Water Demand": 680},
    {"Temperature": 31, "Population": 1100, "Water Demand": 550},
]

st.title("💧 AquaAI - Smart Water Distribution")
st.write("AI-powered water demand prediction and management")
st.success("AquaAI application loaded successfully")

page = st.sidebar.radio("Navigation", ["Dashboard", "Predict Demand", "Data", "About"])

if page == "Dashboard":
    avg = sum(row["Water Demand"] for row in DATA) / len(DATA)
    a, b, c = st.columns(3)
    a.metric("Records", len(DATA))
    b.metric("Average Demand", f"{avg:.1f} L")
    c.metric("Model", "Water Demand Predictor")
    st.subheader("Water Demand Data")
    st.dataframe(DATA, use_container_width=True, hide_index=True)

elif page == "Predict Demand":
    st.subheader("💧 Predict Water Demand")
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=30.0, step=0.5)
    population = st.number_input("Population", min_value=1, max_value=10000000, value=1000, step=100)
    if st.button("Predict Water Demand", type="primary", use_container_width=True):
        demand = max(0.0, 8.0 * temperature + 0.4 * population - 90.0)
        st.success("Prediction completed successfully")
        st.metric("Estimated Daily Water Demand", f"{demand:,.2f} L")

elif page == "Data":
    st.subheader("📊 Dataset")
    st.dataframe(DATA, use_container_width=True, hide_index=True)
    st.bar_chart({"Water Demand": [row["Water Demand"] for row in DATA]})

else:
    st.subheader("About AquaAI")
    st.write("AquaAI is an AI-based water distribution and water demand management project.")
    st.write("Technology: Python and Streamlit")
    st.write("The application predicts daily water demand using temperature and population.")

st.caption("AquaAI • AI Water Distribution & Management • v2.0")
