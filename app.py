import os
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# --- 1. RESOLVE ABSOLUTE PATH TO THE ROOT MODEL FILE ---
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
model_path = os.path.join(parent_dir, "stock_reg_model.pkl")

try:
    with open(model_path, "rb") as f1:
        saved_bundle = pickle.load(f1)
        model = saved_bundle['model']
    print("MarketPulse Scalable Translation Engine Mounted Successfully!")
except FileNotFoundError:
    model = None
    print(f"Warning: Model file missing at {model_path}")

import os
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# --- 1. RESOLVE ABSOLUTE PATH TO THE ROOT MODEL FILE ---
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
model_path = os.path.join(parent_dir, "stock_reg_model.pkl")

try:
    with open(model_path, "rb") as f1:
        saved_bundle = pickle.load(f1)
        model = saved_bundle['model']
    print("MarketPulse Scalable Translation Engine Mounted Successfully!")
except FileNotFoundError:
    model = None
    print(f"Warning: Model file missing at {model_path}")

import os
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# --- 1. RESOLVE ABSOLUTE PATH TO THE ROOT MODEL FILE ---
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
model_path = os.path.join(parent_dir, "stock_reg_model.pkl")

try:
    with open(model_path, "rb") as f1:
        saved_bundle = pickle.load(f1)
        model = saved_bundle['model']
    print("MarketPulse Scalable Translation Engine Mounted Successfully!")
except FileNotFoundError:
    model = None
    print(f"Warning: Model file missing at {model_path}")

@app.route("/", methods=["GET", "POST"])
def home():
    prediction_text = None
    alert_class = ""
    
    if request.method == "POST":
        try:
            # 1. Ingest all values currently showing on your HTML dashboard screen
            open_p = float(request.form.get("open"))
            high_p = float(request.form.get("high"))
            low_p = float(request.form.get("low"))
            close_p = float(request.form.get("close"))
            sma_7_val = float(request.form.get("sma_7"))
            sma_21_val = float(request.form.get("sma_21"))
            
            # 2. TRANSLATOR METHOD: Convert absolute inputs into relative ratios
            open_ratio = open_p / close_p
            high_ratio = high_p / close_p
            low_ratio = low_p / close_p
            sma7_ratio = sma_7_val / close_p
            sma21_ratio = sma_21_val / close_p
            
            # Map ratios onto a baseline dataset anchor range that your model trained on
            anchor_close = 18015.45
            sim_open = open_ratio * anchor_close
            sim_high = high_ratio * anchor_close
            sim_low = low_ratio * anchor_close
            sim_sma7 = sma7_ratio * anchor_close
            sim_sma21 = sma21_ratio * anchor_close
            
            # Construct the input matrix matching the exact 6 features your model expects
            input_matrix = np.array([[sim_open, sim_high, sim_low, anchor_close, sim_sma7, sim_sma21]])
            
            if model:
                # 3. COMPUTE CALCULATED VALUE & CONVERT TO A SINGLE PYTHON FLOAT
                # Fixed: Added float() to extract the number cleanly from array containers
                raw_prediction = float(model.predict(input_matrix)[0])
                
                # REVERSE THE TRANSLATION: Upscale back to your high 22k price scale
                predicted_ratio = raw_prediction / anchor_close
                predicted_price = close_p * predicted_ratio
                
                # 4. Compare predicted outcome to today's closing price to dynamically swap banners
                if predicted_price > close_p:
                    prediction_text = f"MarketPulse Target Forecast: UPWARD Trend Expected. Predicted Value: ₹ {predicted_price:.2f}"
                    alert_class = "up"
                else:
                    prediction_text = f"MarketPulse Target Forecast: DOWNWARD/FLAT Trend Expected. Predicted Value: ₹ {predicted_price:.2f}"
                    alert_class = "down"
            else:
                prediction_text = "System Error: Regressor weight bundle not mounted."
                alert_class = "down"
                
        except Exception as e:
            # Displays any actual code execution bugs directly inside your web banner for fast verification
            prediction_text = f"Form Processing Interruption: {str(e)}"
            alert_class = "down"

    return render_template("index.html", prediction=prediction_text, alert_class=alert_class)

if __name__ == "__main__":
    app.run(debug=True)
