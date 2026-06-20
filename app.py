import streamlit as st
import pandas as pd
import joblib

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Gold Rate Prediction Dashboard",
    page_icon="📈",
    layout="wide"
)

# ====================================
# PREMIUM CSS
# ====================================

st.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

/* Metric Cards */
[data-testid="metric-container"]{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    padding:20px;
    border-radius:20px;
    backdrop-filter: blur(12px);
}

/* Number Inputs */
.stNumberInput{
    background: rgba(255,255,255,0.04);
    border-radius:15px;
    padding:5px;
}

/* Buttons */
.stButton button{
    width:100%;
    height:55px;
    border-radius:15px;
    font-size:18px;
    font-weight:bold;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# ====================================
# LOAD MODEL
# ====================================

model = joblib.load("gold_model.pkl")

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Choose Page",
    ["Prediction", "Analytics"]
)

try:
    st.sidebar.image(
        "gold_necklace.jpeg",
        caption="Gold Jewellery",
        use_container_width=True
    )
except:
    st.sidebar.warning(
        "Add gold_necklace.jpeg to project folder"
    )

st.sidebar.markdown("---")

# ====================================
# PREDICTION PAGE
# ====================================

if page == "Prediction":

    st.markdown("""
    <h1 style='color:#FFD700;'>
    🏆 Gold Rate Trend Prediction Dashboard
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "Predict whether tomorrow's gold rate will move UP 📈 or DOWN 📉"
    )

    st.divider()

    st.subheader("Enter Gold Market Values")

    col1, col2 = st.columns(2)

    with col1:

        close = st.number_input(
            "Today's Gold Price",
            value=3400.0,
            help="Current gold price"
        )

        ma5 = st.number_input(
            "Average Gold Price (Last 5 Days)",
            value=3395.0,
            help="Average gold price during the last 5 days"
        )

    with col2:

        ma10 = st.number_input(
            "Average Gold Price (Last 10 Days)",
            value=3380.0,
            help="Average gold price during the last 10 days"
        )

        daily_return = st.number_input(
            "Daily Change (%)",
            value=0.002,
            help="Price change compared to previous day"
        )

    st.divider()

    metric1, metric2 = st.columns(2)

    with metric1:
        st.metric(
            label="Model Accuracy",
            value="54%"
        )

    with metric2:
        st.metric(
            label="Prediction Type",
            value="UP / DOWN"
        )

    st.divider()

    if st.button("🚀 Predict Gold Trend"):

        input_data = pd.DataFrame(
            [[close, ma5, ma10, daily_return]],
            columns=[
                "Close",
                "MA_5",
                "MA_10",
                "Daily_Return"
            ]
        )

        prediction = model.predict(input_data)

        st.subheader("Prediction Result")

        if prediction[0] == 1:

            st.markdown("""
            <div style="
            padding:20px;
            border-radius:20px;
            background:#064e3b;
            text-align:center;
            font-size:28px;
            font-weight:bold;
            ">
            📈 GOLD PRICE LIKELY TO MOVE UP
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div style="
            padding:20px;
            border-radius:20px;
            background:#7f1d1d;
            text-align:center;
            font-size:28px;
            font-weight:bold;
            ">
            📉 GOLD PRICE LIKELY TO MOVE DOWN
            </div>
            """, unsafe_allow_html=True)

# ====================================
# ANALYTICS PAGE
# ====================================

elif page == "Analytics":

    st.title("📊 Gold Market Analytics")

    st.metric(
        label="Current Model Accuracy",
        value="54%"
    )

    st.divider()

    try:

        data = pd.read_csv("prepared_data.csv")

        st.subheader("📈 Historical Gold Price Trend")

        st.line_chart(data["Close"])

        st.divider()

        st.subheader("Dataset Overview")

        st.dataframe(data.head())

        st.write(
            f"📌 Total Records: {len(data)}"
        )

    except Exception as e:

        st.error(f"Error loading data: {e}")