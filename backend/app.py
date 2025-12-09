
from flask import Flask, render_template, request
import pickle
import os
import warnings
import sklearn

# Suppress scikit-learn version warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Load the model
model_path = "car_price_prediction.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found. Please ensure the model file is in the same directory as app.py")

try:
    with open(model_path, "rb") as file:
        model_rf = pickle.load(file)
    print(f"✅ Model loaded successfully")
    print(f"📊 Scikit-learn version: {sklearn.__version__}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("💡 Consider retraining the model with the current scikit-learn version")
    raise

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("car_price_prediction.html")

@app.route("/predict", methods=["GET"])
def predict_price():
    try:
        # Get form data
        year = int(request.args.get("year"))
        age = 2025 - year
        manuf = int(request.args.get("slct1"))
        model = int(request.args.get("slct2"))
        cond = int(request.args.get("cond"))
        cylin = int(request.args.get("cylin"))
        fueltyp = int(request.args.get("fueltyp"))
        odom = float(request.args.get("odom"))
        title = int(request.args.get("title"))
        transm = int(request.args.get("transm"))
        drivetype = int(request.args.get("drivetype"))
        car_type = int(request.args.get("type"))  # Renamed to avoid conflict with built-in type
        color = int(request.args.get("color"))
        state = int(request.args.get("state"))
        region = int(request.args.get("region"))
        avg_mil = float(request.args.get("avg_mil"))
        manufc = int(request.args.get("manufc"))
        type_class = int(request.args.get("type_class"))
        color_class = int(request.args.get("color_class"))

        # Prepare input data for prediction
        input_data = [[
            year, manuf, model, cond, cylin, fueltyp, odom,
            title, transm, drivetype, car_type, color, state,
            region, age, avg_mil, manufc, type_class, color_class
        ]]

        # Make prediction
        price = model_rf.predict(input_data)
        car_price = "{:,.2f}".format(price[0])  # Format with commas for better readability
        return render_template("result.html", prediction=car_price)

    except ValueError as e:
        # Handle invalid input data
        error_message = "Please ensure all form fields are filled with valid values."
        return render_template("error.html", error=error_message)
    except Exception as e:
        # Handle other errors
        error_message = f"An error occurred: {str(e)}"
        return render_template("error.html", error=error_message)

if __name__ == "__main__":
    print("🚀 Starting Car Price Prediction App...")
    print("🌐 Server will be available at: http://localhost:4500")
    app.run(host="0.0.0.0", port=4500, debug=True)

        # # Now predict (skip region for now unless one-hot encoded already)
        # input_data = [[
        #     year, manuf, model, cond, int(request.args.get("cylin")), fueltyp,
        #     odom, title, transm, drivetype, type, color, state, region, age,
        #     avg_mil, manufc, type_class, color_class
        # ]]

        # # remove 'region' if model does not use it directly
        # input_data = [[
        #     year, manuf, model, cond, int(request.args.get("cylin")), fueltyp,
        #     odom, title, transm, drivetype, type, color, state, age,
        #     avg_mil, manufc, type_class, color_class
        # ]]

        