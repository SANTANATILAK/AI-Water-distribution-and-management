import streamlit as st

st.set_page_config(page_title="AquaAI", page_icon="💧", layout="wide")

st.title("💧 AquaAI - Smart Water Distribution")
st.write("AI-powered water demand prediction and management")

st.sidebar.title("AquaAI")
page = st.sidebar.radio("Navigation", ["Dashboard", "Predict Demand", "About"])

if page == "Dashboard":
    st.header("Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Records", "7")
    c2.metric("Average Demand", "561.4 L")
    c3.metric("Model", "Linear Regression")
    st.subheader("Sample Water Demand Data")
    st.dataframe([
        {"Temperature": 30, "Population": 1000, "Water Demand": 500},
        {"Temperature": 32, "Population": 1200, "Water Demand": 600},
        {"Temperature": 35, "Population": 1500, "Water Demand": 750},
        {"Temperature": 28, "Population": 900, "Water Demand": 450},
        {"Temperature": 25, "Population": 800, "Water Demand": 400},
        {"Temperature": 33, "Population": 1300, "Water Demand": 680},
        {"Temperature": 31, "Population": 1100, "Water Demand": 550}
    ], use_container_width=True, hide_index=True)

elif page == "Predict Demand":
    st.header("Predict Water Demand")
    temperature = st.number_input("Temperature (°C)", 0.0, 60.0, 30.0, 0.5)
    population = st.number_input("Population", 1.0, 10000000.0, 1000.0, 100.0)
    if st.button("Predict Water Demand", type="primary"):
        result = max(0.0, 8.0 * temperature + 0.4 * population - 90.0)
        st.success("Prediction completed")
        st.metric("Estimated Daily Water Demand", f"{result:,.2f} L")

else:
    st.header("About AquaAI")
    st.write("AquaAI is an AI-based water distribution and demand management project.")
    st.write("Technology: Python, Streamlit and Machine Learning")

st.caption("AquaAI • AI Water Distribution & Management")
