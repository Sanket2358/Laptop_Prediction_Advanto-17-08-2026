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

# Premium UI with Animated Background, 2-Word Typing Effect, and Clean Dropdowns
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Laptop Prediction</title>
    <!-- Confetti Library for Celebration Animation -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        /* Animated Gradient Background */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 0;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            flex-direction: column;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Container Styling */
        .container { 
            background: #ffffff; 
            padding: 35px 40px; 
            border-radius: 16px; 
            box-shadow: 0px 20px 40px rgba(0,0,0,0.2); 
            width: 100%;
            max-width: 360px; 
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Dynamic Typing Effect CSS */
        .typewriter-container {
            text-align: center;
            margin-bottom: 25px;
            font-size: 26px;
            font-weight: 800;
            color: #2c3e50;
            min-height: 35px;
        }
        .cursor {
            display: inline-block;
            width: 3px;
            height: 25px;
            background-color: #e73c7e;
            vertical-align: middle;
            margin-left: 4px;
            animation: blink 0.75s step-end infinite;
        }
        @keyframes blink { 50% { opacity: 0; } }

        /* Input & Dropdown Fields */
        label { font-weight: 600; color: #34495e; font-size: 14px; display: block; margin-top: 15px;}
        input, select { 
            width: 100%; 
            padding: 12px; 
            margin-top: 6px; 
            border: 2px solid #eaeded; 
            border-radius: 8px; 
            box-sizing: border-box;
            transition: all 0.3s ease;
            font-size: 15px;
            background-color: #fcfcfc;
            color: #2c3e50;
        }
        input:focus, select:focus { 
            border-color: #3498db; 
            background-color: #fff;
            outline: none; 
            box-shadow: 0 0 8px rgba(52, 152, 219, 0.2);
        }

        /* Button Styling */
        button { 
            width: 100%; 
            padding: 14px; 
            margin-top: 30px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold;
            letter-spacing: 0.5px;
            transition: all 0.3s ease; 
        }
        button:hover { 
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4);
        }
        button:active {
            transform: translateY(1px);
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
        <!-- JavaScript se control hone wala Dynamic Heading (Sirf 2 words) -->
        <div class="typewriter-container">
            <span id="typewriter-text"></span><span class="cursor"></span>
        </div>

        <form id="predictionForm">
            <label>Age:</label>
            <input type="number" step="any" id="Age" value="25" required>
            
            <label>Gender:</label>
            <select id="Gender" required>
                <option value="0">Female</option>
                <option value="1" selected>Male</option>
            </select>
            
            <label>Region:</label>
            <select id="Region" required>
                <option value="0">North</option>
                <option value="1" selected>South</option>
                <option value="2">East</option>
                <option value="3">West</option>
            </select>
            
            <label>Occupation:</label>
            <select id="Occupation" required>
                <option value="0">Student</option>
                <option value="1">Professional</option>
                <option value="2" selected>Business</option>
                <option value="3">Freelancer</option>
                <option value="4">Other</option>
            </select>
            
            <label>Income:</label>
            <input type="number" step="any" id="Income" value="50000" required>
            
            <button type="submit">Predict Now</button>
        </form>

        <div id="result-box"></div>
    </div>

    <script>
        // 1. DYNAMIC TYPING EFFECT LOGIC (Sirf 2 Words)
        const words = ["AI Laptop Predictor", "Smart ML Engine"];
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typingElement = document.getElementById("typewriter-text");

        function typeEffect() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentWord.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingElement.textContent = currentWord.substring(0, charIndex + 1);
                charIndex++;
            }

            let typingSpeed = isDeleting ? 40 : 100;

            if (!isDeleting && charIndex === currentWord.length) {
                typingSpeed = 2500; // Word complete hone ke baad jyada der ruke
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length; // Sirf do words ke bich ghumega
                typingSpeed = 500;
            }

            setTimeout(typeEffect, typingSpeed);
        }
        
        document.addEventListener("DOMContentLoaded", typeEffect);

        // 2. FORM SUBMISSION & PREDICTION LOGIC
        document.getElementById("predictionForm").addEventListener("submit", async function(event) {
            event.preventDefault(); 
            
            const resultBox = document.getElementById("result-box");
            const btn = document.querySelector("button");
            
            resultBox.style.display = "block";
            resultBox.className = ""; 
            resultBox.innerText = "Predicting...";
            btn.innerText = "Processing...";
            btn.disabled = true;

            const data = {
                Age: document.getElementById("Age").value,
                Gender: document.getElementById("Gender").value,
                Region: document.getElementById("Region").value,
                Occupation: document.getElementById("Occupation").value,
                Income: document.getElementById("Income").value
            };

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if(result.status === "success") {
                    resultBox.innerText = "Prediction: " + result.prediction_result.toUpperCase();
                    
                    if(result.prediction_result.toLowerCase() === "yes") {
                        resultBox.className = "success-yes";
                        
                        // Confetti Celebration
                        confetti({
                            particleCount: 150,
                            spread: 80,
                            origin: { y: 0.6 },
                            colors: ['#26ccff', '#a25afd', '#ff5e7e', '#88ff5a', '#fcff42', '#ffa62d', '#ff36ff']
                        });
                        
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
            } finally {
                btn.innerText = "Predict Now";
                btn.disabled = false;
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
