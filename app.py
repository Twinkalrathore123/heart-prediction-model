# import streamlit as st
# import pickle
# import numpy as np

# # Load model
# model = pickle.load(open("heart_model.pkl","rb"))

# # Page config
# st.set_page_config(
#     page_title="Heart Attack Prediction",
#     page_icon="❤️",
#     layout="wide"
# )

# # Title
# st.title("❤️ Heart Attack Prediction System")

# st.write(
#     "Enter patient medical information below."
# )

# # Create columns
# col1,col2 = st.columns(2)

# with col1:

#     age = st.number_input(
#         "Age",
#         1,
#         120,
#         30
#     )

#     gender = st.selectbox(
#         "Gender",
#         ["Female","Male"]
#     )

#     heart_rate = st.number_input(
#         "Heart Rate",
#         40,
#         220,
#         80
#     )

#     systolic = st.number_input(
#         "Systolic Blood Pressure",
#         50,
#         250,
#         120
#     )

# with col2:

#     diastolic = st.number_input(
#         "Diastolic Blood Pressure",
#         30,
#         200,
#         80
#     )

#     blood_sugar = st.number_input(
#         "Blood Sugar",
#         50.0,
#         600.0,
#         120.0
#     )

#     ckmb = st.number_input(
#         "CK-MB",
#         0.0,
#         50.0,
#         2.0
#     )

#     troponin = st.number_input(
#         "Troponin",
#         0.000,
#         10.000,
#         0.010
#     )

# # Convert gender
# gender_value = 1 if gender=="Male" else 0

# # Prediction button
# if st.button("Predict Result"):

#     input_data = np.array([[
#         age,
#         gender_value,
#         heart_rate,
#         systolic,
#         diastolic,
#         blood_sugar,
#         ckmb,
#         troponin
#     ]])

#     prediction = model.predict(input_data)

#     if prediction[0]==1:

#         st.error(
#             "⚠️ Positive Heart Attack Risk"
#         )

#     else:

#         st.success(
#             "✅ Negative Heart Attack Risk"
#         )


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle

# Load model
model = pickle.load(open("heart_model.pkl","rb"))
df = pd.read_csv("heart.csv")


# -------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Heart Dashboard",
    layout="wide"
)

# -------- CSS ----------
st.markdown("""
<style>

.card{
background: linear-gradient(145deg,#1E1E1E,#2A2A2A);
padding:25px;
border-radius:18px;
box-shadow:0 0 15px rgba(0,173,181,0.4);
text-align:center;
margin-bottom:20px;
}

.card h3{
color:#EEEEEE;
margin-bottom:12px;
}

.metric{
font-size:34px;
font-weight:bold;
color:#00ADB5;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
page = st.sidebar.radio(
    "Navigation",
    ["Prediction","Dashboard","Analytics"]
)

# DASHBOARD
if page=="Dashboard":

    st.title("Heart Attack prediction Dashboard")

    # ---------- Row 1 ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='card'>
            <h3>Total Patients</h3>
            <div class='metric'>{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
            <h3>Average Age</h3>
            <div class='metric'>{round(df['Age'].mean(),1)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- Row 2 ----------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"""
        <div class='card'>
            <h3>Positive Cases</h3>
            <div class='metric'>
                {(df['Result']=='positive').sum()}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='card'>
            <h3>Negative Cases</h3>
            <div class='metric'>
                {(df['Result']=='negative').sum()}
            </div>
        </div>
        """, unsafe_allow_html=True)
# PREDICTION PAGE
elif page=="Prediction":

    st.title("🩺 Heart Risk Prediction")

    col1,col2 = st.columns(2)

    with col1:

        age = st.number_input("Age",1,120,40)
        gender = st.selectbox("Gender",[0,1])
        hr = st.number_input("Heart Rate",40,220,80)
        sys = st.number_input("Systolic BP",50,250,120)

    with col2:

        dia = st.number_input("Diastolic BP",30,200,80)
        sugar = st.number_input("Blood Sugar",50.0,500.0,120.0)
        ckmb = st.number_input("CK-MB",0.0,20.0,2.0)
        troponin = st.number_input("Troponin",0.0,10.0,0.01)

    if st.button("Predict"):

        data = np.array([[
            age,
            gender,
            hr,
            sys,
            dia,
            sugar,
            ckmb,
            troponin
        ]])

        pred = model.predict(data)[0]
        prob = model.predict_proba(data)[0]

        risk = prob[1]*100

        if pred==1:
            st.error(f"⚠️ HIGH RISK ({risk:.2f}%)")
        else:
            st.success(f"✅ LOW RISK ({100-risk:.2f}%)")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            title={'text':"Risk %"},
            gauge={
                'axis':{'range':[0,100]},
                'bar':{'color':'red'}
            }
        ))

        st.plotly_chart(fig,use_container_width=True)

# ANALYTICS
else:

    st.title("📊 Analytics")

    fig1 = px.histogram(
        df,
        x="Age",
        color="Result",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.box(
        df,
        x="Result",
        y="Heart rate",
        color="Result",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    fig3 = px.scatter(
        df,
        x="Blood sugar",
        y="Heart rate",
        color="Result",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(df.head())