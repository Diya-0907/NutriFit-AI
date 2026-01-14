import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= LOAD MODELS =================

workout_model = pickle.load(
    open(os.path.join(BASE_DIR, "models", "workout_recommendation_model.pkl"), "rb")
)

food_model = pickle.load(
    open(os.path.join(BASE_DIR, "models", "indian_food_calorie_model.pkl"), "rb")
)

lifestyle_model = pickle.load(
    open(os.path.join(BASE_DIR, "models", "lifestyle_disease_risk_model.pkl"), "rb")
)

# ================= ROUTES =================

@app.route("/")
def home():
    return jsonify({"status": "NutriFit AI Backend Running"})

# 1️⃣ WORKOUT
@app.route("/predict/workout", methods=["POST"])
def predict_workout():
    data = request.json

    age = data["age"]
    weight = data["weight"]
    height = data["height"]

    result = workout_model.predict([[age, weight, height]])[0]

    return jsonify({
        "recommended_workout": result
    })

# 2️⃣ FOOD CALORIES
@app.route("/predict/food-calorie", methods=["POST"])
def predict_food():
    data = request.json
    food = data["food"].lower()

    calories = food_model.predict([food])[0]

    return jsonify({
        "food": food,
        "calories": int(calories)
    })

# 3️⃣ LIFESTYLE RISK
@app.route("/predict/lifestyle-risk", methods=["POST"])
def predict_risk():
    data = request.json

    features = [[
        data["pregnancies"],
        data["glucose"],
        data["bloodpressure"],
        data["skinthickness"],
        data["insulin"],
        data["bmi"],
        data["diabetespedigreefunction"],
        data["age"]
    ]]

    pred = lifestyle_model.predict(features)[0]
    risk_map = {0: "Low", 1: "Medium", 2: "High"}

    return jsonify({
        "risk_level": risk_map[pred],
        "disclaimer": "This is not a medical diagnosis."
    })

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
