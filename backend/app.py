import streamlit as st
import pickle
import numpy as np
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="NutriFit AI",
    page_icon="💪",
    layout="wide"
)

st.title("💪 NutriFit AI – Smart Health Assistant")
st.caption("AI-powered fitness, nutrition & lifestyle risk prediction")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- LOAD MODELS ----------
@st.cache_resource
def load_models():
    workout = pickle.load(open(os.path.join(BASE_DIR, "models", "workout_recommendation_model.pkl"), "rb"))
    food = pickle.load(open(os.path.join(BASE_DIR, "models", "indian_food_calorie_model.pkl"), "rb"))
    lifestyle = pickle.load(open(os.path.join(BASE_DIR, "models", "lifestyle_disease_risk_model.pkl"), "rb"))
    return workout, food, lifestyle

workout_model, food_model, lifestyle_model = load_models()

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs([
    "🏋️ Workout Recommendation",
    "🍛 Indian Food Calories",
    "🩺 Lifestyle Health Risk"
])

# ---------- TAB 1: WORKOUT ----------
with tab1:
    st.subheader("🏋️ Personalized Workout Plan")

    age = st.number_input("Age", 10, 80)
    weight = st.number_input("Weight (kg)", 30, 150)
    height = st.number_input("Height (cm)", 120, 220)

    if st.button("Predict Workout"):
        result = workout_model.predict([[age, weight, height]])[0]
        st.success(f"✅ Recommended Workout: **{result}**")

# ---------- TAB 2: FOOD ----------
with tab2:
    st.subheader("🍛 Indian Food Calorie Estimation")

    food = st.text_input("Enter Indian food name")

    if st.button("Predict Calories"):
        calories = food_model.predict([food.lower()])[0]
        st.info(f"🍽️ **{food.title()}** contains approx **{int(calories)} kcal**")

# ---------- TAB 3: LIFESTYLE RISK ----------
with tab3:
    st.subheader("🩺 Lifestyle Disease Risk Prediction")

    pregnancies = st.number_input("Pregnancies", 0, 15)
    glucose = st.number_input("Glucose", 50, 300)
    bloodpressure = st.number_input("Blood Pressure", 30, 200)
    skinthickness = st.number_input("Skin Thickness", 0, 100)
    insulin = st.number_input("Insulin", 0, 900)
    bmi = st.number_input("BMI", 10.0, 60.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0)
    age_risk = st.number_input("Age", 10, 90)

    if st.button("Predict Risk"):
        features = [[
            pregnancies,
            glucose,
            bloodpressure,
            skinthickness,
            insulin,
            bmi,
            dpf,
            age_risk
        ]]

        risk = lifestyle_model.predict(features)[0]
        risk_map = {0: "Low", 1: "Medium", 2: "High"}

        st.warning(f"⚠️ **Lifestyle Disease Risk: {risk_map[risk]}**")
        st.caption("This is not a medical diagnosis.")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built with ❤️ using Machine Learning & Streamlit")
