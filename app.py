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
    height:60px;
    border-radius:18px;
    font-size:20px;
    font-weight:bold;
    background: linear-gradient(
        90deg,
        #FFD700,
        #FFA500
    );
    color:black;
    border:none;
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

st.sidebar.title(" Navigation")

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
    <h1 style="
    background: linear-gradient(90deg,#FFD700,#FFA500,#FFF8DC);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-size:45px;
    font-weight:800;
    ">
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
            value="54%",
            delta="+4%"
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

        probability = model.predict_proba(input_data)

        down_prob = round(probability[0][0] * 100, 2)
        up_prob = round(probability[0][1] * 100, 2)

        confidence = max(down_prob, up_prob)

        st.subheader("Prediction Result")

        if prediction[0] == 1:

            st.markdown(f"""
            <div style="
            padding:25px;
            border-radius:20px;
            background:linear-gradient(
            90deg,
            #065f46,
            #10b981
            );
            box-shadow:0 0 25px #10b981;
            text-align:center;
            font-size:28px;
            font-weight:bold;
           ">
           📈 GOLD PRICE LIKELY TO MOVE UP
           <br><br>
           🎯 Confidence: {confidence}%
           </div>
           """, unsafe_allow_html=True)

        else:

           st.markdown(f"""
           <div style="
           padding:25px;
           border-radius:20px;
           background:linear-gradient(
           90deg,
           #991b1b,
           #ef4444
           );
           box-shadow:0 0 25px #ef4444;
           text-align:center;
           font-size:28px;
           font-weight:bold;
           ">
           📉 GOLD PRICE LIKELY TO MOVE DOWN
           <br><br>
           🎯 Confidence: {confidence}%
           </div>
           """, unsafe_allow_html=True)

        st.divider()

        st.subheader("📊 Prediction Probabilities")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
               "📉 Down Probability",
               f"{down_prob}%"
            )

        with col2:
           st.metric(
              "📈 Up Probability",
              f"{up_prob}%"
            )

        st.progress(confidence / 100)

        st.info(
           f"Model Confidence Score: {confidence}%"
        )

        st.write("Input Used:")
        st.dataframe(input_data)

# ====================================
# ANALYTICS PAGE
# ====================================

elif page == "Analytics":

    st.title("📊 Gold Market Analytics")

    st.metric(
        label="Model Accuracy",
        value="54%",
        delta="+4%"
    )

    st.divider()

    try:

        data = pd.read_csv("prepared_data.csv")

        st.subheader("📈 Historical Gold Price Trend")

        st.line_chart(data["Close"])

        st.info(
            "Historical gold market data used for model training and evaluation."
        )

        st.subheader("Price Statistics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Maximum Price",
            f"{data['Close'].max():.2f}"
        )

        col2.metric(
            "Minimum Price",
            f"{data['Close'].min():.2f}"
        )

        col3.metric(
            "Average Price",
            f"{data['Close'].mean():.2f}"
        )

        st.divider()

        st.subheader("Dataset Overview")

        st.dataframe(data.head())

        st.write(
            f"📌 Total Records: {len(data)}"
        )

    except Exception as e:

        st.error(f"Error loading data: {e}")

