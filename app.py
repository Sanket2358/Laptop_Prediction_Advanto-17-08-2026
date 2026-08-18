from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Model load karna
MODEL_PATH = "model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Browser ke liye ek simple HTML form
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Laptop Prediction Model</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; }
        .container { max-width: 400px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 8px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Test Your Model</h2>
        <form action="/predict" method="post">
            <label>Age:</label>
            <input type="number" step="any" name="Age" value="25" required>
            
            <label>Gender:</label>
            <input type="number" step="any" name="Gender" value="0" required>
            
            <label>Region:</label>
            <input type="number" step="any" name="Region" value="1" required>
            
            <label>Occupation:</label>
            <input type="number" step="any" name="Occupation" value="2" required>
            
            <label>Income:</label>
            <input type="number" step="any" name="Income" value="50000" required>
            
            <button type="submit">Predict Now</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    """Ye direct aapke browser me form dikhayega."""
    if model is None:
        return "Model load nahi hua hai. Kripya logs check karein.", 500
    return HTML_FORM

@app.route("/predict", methods=["POST"])
def predict():
    """Ye form ya API se data lega aur prediction dega."""
    if model is None:
        return jsonify({"error": "Model is not loaded."}), 500

    try:
        # Check karna ki data JSON se aaya hai (Postman/Python) ya Web Form se
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Features extract karna aur float format me convert karna
        feature_names = ['Age', 'Gender', 'Region', 'Occupation', 'Income']
        input_values = [[
            float(data.get('Age', 0)),
            float(data.get('Gender', 0)),
            float(data.get('Region', 0)),
            float(data.get('Occupation', 0)),
            float(data.get('Income', 0))
        ]]
        
        # DataFrame me convert karna
        input_df = pd.DataFrame(input_values, columns=feature_names)
        
        # Prediction nikalna
        prediction = model.predict(input_df)
        
        return jsonify({
            "status": "success",
            "prediction_result": prediction[0],
            "input_provided": data
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
