let chart;


function runWorkout() {
    const response = {
        text: "Recommended Workout: Strength + Cardio",
        chart: { Strength: 60, Cardio: 40 }
    };
    updateUI(response);
}

function runIndianFood() {
    const food = document.getElementById("foodNameInput").value;
    const response = {
        text: `Estimated Calories for ${food}: 320 kcal`,
        chart: { Calories: 320 }
    };
    updateUI(response);
}

function runLifestyleRisk() {

    const data = {
        Pregnancies: Number(document.getElementById("Pregnancies").value),
        Glucose: Number(document.getElementById("Glucose").value),
        BloodPressure: Number(document.getElementById("BloodPressure").value),
        SkinThickness: Number(document.getElementById("SkinThickness").value),
        Insulin: Number(document.getElementById("Insulin").value),
        BMI: Number(document.getElementById("BMI").value),
        DiabetesPedigreeFunction: Number(document.getElementById("DiabetesPedigreeFunction").value),
        AgeRisk: Number(document.getElementById("AgeRisk").value)
    };

    fetch(`${API_URL}/predict/lifestyle-risk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {

        let chartData;
        if (result.risk_level === "Low") {
            chartData = { Low: 1 };
        } else if (result.risk_level === "Medium") {
            chartData = { Medium: 1 };
        } else {
            chartData = { High: 1 };
        }

        updateUI({
            text: `Lifestyle Disease Risk: ${result.risk_level}`,
            chart: chartData
        });
    })
    .catch(err => {
        updateUI({
            text: "Error predicting lifestyle risk",
            chart: {}
        });
        console.error(err);
    });
}


function updateUI(response) {
    document.querySelector(".output").classList.remove("hidden");
    document.getElementById("resultText").innerText = response.text;

    if (chart) chart.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type: "bar",
        data: {
            labels: Object.keys(response.chart),
            datasets: [{
                data: Object.values(response.chart)
            }]
        },
        options: {
            plugins: { legend: { display: false } }
        }
    });
}
window.addEventListener("load", () => {
    const cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.classList.add("show");
    });
});
