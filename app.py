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

# Advance UI with Animations, Center Alignment, and AJAX
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Laptop Prediction</title>
    <style>
        /* Base Styling & Background */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
        }
        
        /* Container Styling with Animation */
        .container { 
            background: rgba(255, 255, 255, 0.95); 
            padding: 30px 40px; 
            border-radius: 15px; 
            box-shadow: 0px 15px 25px rgba(0,0,0,0.2); 
            width: 100%;
            max-width: 350px; 
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 { text-align: center; color: #333; margin-top: 0; }

        /* Input Fields */
        label { font-weight: bold; color: #555; font-size: 14px; display: block; margin-top: 15px;}
        input { 
            width: 100%; 
            padding: 10px; 
            margin-top: 5px; 
            border: 1px solid #ccc; 
            border-radius: 8px; 
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        input:focus { border-color: #667eea; outline: none; }

        /* Button Styling with Hover Animation */
        button { 
            width: 100%; 
            padding: 12px; 
            margin-top: 25px; 
            background: #667eea; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold;
            transition: all 0.3s ease; 
        }
        button:hover { 
            background: #5a6cd6; 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        /* Result Box Styling */
        #result-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            display: none;
            animation: fadeIn 0.5s ease-in-out;
        }
        .success-yes { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .success-no { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .error { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Predict Model</h2>
        <form id="predictionForm">
            <label>Age:</label>
            <input type="number" step="any" id="Age" value="25" required>
            
            <label>Gender:</label>
            <input type="number" step="any" id="Gender" value="1" required>
            
            <label>Region:</label>
            <input type="number" step="any" id="Region" value="1" required>
            
            <label>Occupation:</label>
            <input type="number" step="any" id="Occupation" value="2" required>
            
            <label>Income:</label>
            <input type="number" step="any" id="Income" value="50000" required>
            
            <button type="submit">Predict Now</button>
        </form>

        <!-- Prediction result will show here -->
        <div id="result-box"></div>
    </div>

    <script>
        // Form submit hone par page reload rokne ke liye JavaScript (AJAX)
        document.getElementById("predictionForm").addEventListener("submit", async function(event) {
            event.preventDefault(); // Page refresh hone se rokta hai
            
            const resultBox = document.getElementById("result-box");
            resultBox.style.display = "block";
            resultBox.className = ""; 
            resultBox.innerText = "Predicting...";

            // Values collect karna
            const data = {
                Age: document.getElementById("Age").value,
                Gender: document.getElementById("Gender").value,
                Region: document.getElementById("Region").value,
                Occupation: document.getElementById("Occupation").value,
                Income: document.getElementById("Income").value
            };

            try {
                // API ko background me call karna
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                // Result show karna directly page par
                if(result.status === "success") {
                    resultBox.innerText = "Prediction: " + result.prediction_result.toUpperCase();
                    // Different colors based on "yes" or "no"
                    if(result.prediction_result.toLowerCase() === "yes") {
                        resultBox.className = "success-yes";
                    } else {
                        resultBox.className = "success-no";
                    }
                } else {
                    resultBox.innerText = "Error: " + result.error;
                    resultBox.className = "error";
                }
            } catch (error) {
                resultBox.innerText = "Something went wrong!";
                resultBox.className = "error";
            }
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    if model is None:
        return "Model load nahi hua hai. Kripya logs check karein.", 500
    return HTML_FORM

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model is not loaded."}), 500

    try:
        # Ab data hamesha JSON format me aayega kyu ki front-end JS fetch use kar raha hai
        data = request.get_json()

        feature_names = ['Age', 'Gender', 'Region', 'Occupation', 'Income']
        input_values = [[
            float(data.get('Age', 0)),
            float(data.get('Gender', 0)),
            float(data.get('Region', 0)),
            float(data.get('Occupation', 0)),
            float(data.get('Income', 0))
        ]]
        
        input_df = pd.DataFrame(input_values, columns=feature_names)
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
