from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load the SVC model securely
MODEL_PATH = "model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint for Render."""
    if model is None:
        return jsonify({"status": "error", "message": "Model failed to load."}), 500
    return jsonify({"status": "healthy", "message": "SVC Model API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    """Endpoint to get predictions from the model."""
    if model is None:
        return jsonify({"error": "Model is not loaded."}), 500

    try:
        # Parse JSON request
        data = request.get_json()

        # The model expects exactly these 5 features in this specific order
        feature_names = ['Age', 'Gender', 'Region', 'Occupation', 'Income']
        
        # Extract features from the incoming JSON (defaulting to 0 if missing)
        # Note: Ensure categorical inputs (Gender, Region, Occupation) are mapped 
        # to the correct numeric encodings that the model was originally trained on.
        input_values = [[data.get(feat, 0) for feat in feature_names]]
        
        # Convert to a pandas DataFrame to suppress scikit-learn warnings about missing feature names
        input_df = pd.DataFrame(input_values, columns=feature_names)
        
        # Make the prediction
        prediction = model.predict(input_df)
        
        return jsonify({
            "prediction": prediction[0], # Will output "yes" or "no"
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400

if __name__ == "__main__":
    # Render assigns a dynamic PORT via environment variables
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
