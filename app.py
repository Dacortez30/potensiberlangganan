from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("model.pkl")
feature_columns = joblib.load("feature_columns.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    tenure = float(request.form["tenure"])
    monthlycharges = float(request.form["monthlycharges"])
    totalcharges = float(request.form["totalcharges"])

    senior = int(request.form["senior"])
    gender = request.form["gender"]
    partner = request.form["partner"]
    dependents = request.form["dependents"]
    internet = request.form["internet"]
    contract = request.form["contract"]
    paperless = request.form["paperless"]

    data = pd.DataFrame(
        [[0] * len(feature_columns)],
        columns=feature_columns
    )

    # Numeric
    if "SeniorCitizen" in data.columns:
        data["SeniorCitizen"] = senior

    if "tenure" in data.columns:
        data["tenure"] = tenure

    if "MonthlyCharges" in data.columns:
        data["MonthlyCharges"] = monthlycharges

    if "TotalCharges" in data.columns:
        data["TotalCharges"] = totalcharges

    # Gender
    if gender == "Male":
        if "gender_Male" in data.columns:
            data["gender_Male"] = 1

    # Partner
    if partner == "Yes":
        if "Partner_Yes" in data.columns:
            data["Partner_Yes"] = 1

    # Dependents
    if dependents == "Yes":
        if "Dependents_Yes" in data.columns:
            data["Dependents_Yes"] = 1

    # Internet Service
    if internet == "Fiber optic":
        if "InternetService_Fiber optic" in data.columns:
            data["InternetService_Fiber optic"] = 1

    elif internet == "No":
        if "InternetService_No" in data.columns:
            data["InternetService_No"] = 1

    # Contract
    if contract == "One year":
        if "Contract_One year" in data.columns:
            data["Contract_One year"] = 1

    elif contract == "Two year":
        if "Contract_Two year" in data.columns:
            data["Contract_Two year"] = 1

    # Paperless Billing
    if paperless == "Yes":
        if "PaperlessBilling_Yes" in data.columns:
            data["PaperlessBilling_Yes"] = 1

    prediction = model.predict(data)[0]

    if prediction == 1:
        result = "⚠️ Customer Berpotensi Churn"
    else:
        result = "✅ Customer Tidak Churn"

    return render_template(
        "index.html",
        prediction=result
    )


if __name__ == "__main__":
    app.run(debug=True)