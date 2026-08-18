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

# Advance UI with Dynamic Typing Effect, Dropdowns, and Confetti
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
        
        /* Container Styling */
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

        /* Dynamic Typing Effect CSS */
        .typewriter-container {
            text-align: center;
            margin-bottom: 20px;
            font-size: 26px;
            font-weight: bold;
            color: #333;
            min-height: 35px; /* Taki layout shift na ho */
        }
        .cursor {
            display: inline-block;
            width: 3px;
            height: 25px;
            background-color: #667eea;
            vertical-align: middle;
            margin-left: 3px;
            animation: blink 0.75s step-end infinite;
        }
        @keyframes blink { 50% { opacity: 0; } }

        /* Input & Dropdown Fields */
        label { font-weight: bold; color: #555; font-size: 14px; display: block; margin-top: 15px;}
        input, select { 
            width: 100%; 
            padding: 10px; 
            margin-top: 5px; 
            border: 1px solid #ccc; 
            border-radius: 8px; 
            box-sizing: border-box;
            transition: border-color 0.3s;
            font-size: 15px;
            background-color: white;
        }
        input:focus, select:focus { border-color: #667eea; outline: none; }

        /* Button Styling */
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
        
        <!-- JavaScript se control hone wala Dynamic Heading -->
        <div class="typewriter-container">
            <span id="typewriter-text"></span><span class="cursor"></span>
        </div>

        <form id="predictionForm">
            <label>Age:</label>
            <input type="number" step="any" id="Age" value="25" required>
            
            <label>Gender:</label>
            <select id="Gender" required>
                <option value="0">Female (0)</option>
                <option value="1" selected>Male (1)</option>
            </select>
            
            <label>Region:</label>
            <select id="Region" required>
                <option value="0">Region Type 0</option>
                <option value="1" selected>Region Type 1</option>
                <option value="2">Region Type 2</option>
                <option value="3">Region Type 3</option>
            </select>
            
            <label>Occupation:</label>
            <select id="Occupation" required>
                <option value="0">Student (0)</option>
                <option value="1">Professional (1)</option>
                <option value="2" selected>Business (2)</option>
                <option value="3">Freelancer (3)</option>
                <option value="4">Other (4)</option>
            </select>
            
            <label>Income:</label>
            <input type="number" step="any" id="Income" value="50000" required>
            
            <button type="submit">Predict Now</button>
        </form>

        <div id="result-box"></div>
    </div>

    <script>
        // 1. DYNAMIC TYPING EFFECT LOGIC
        const words = ["AI Prediction", "Laptop Predictor", "Smart AI Engine", "Data Analytics"];
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

            let typingSpeed = isDeleting ? 50 : 100;

            if (!isDeleting && charIndex === currentWord.length) {
                typingSpeed = 2000; // Word complete hone ke baad rukne ka time
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length; // Next word select karo
                typingSpeed = 500;
            }

            setTimeout(typeEffect, typingSpeed);
        }
        
        // Start typing effect jab page load ho
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
                        
                        // Fire the Confetti Celebration Animation!
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
