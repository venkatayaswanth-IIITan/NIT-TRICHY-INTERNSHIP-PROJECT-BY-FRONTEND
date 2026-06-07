# ==========================================
# AI CONTENT DETECTOR — FLASK APP
# ==========================================
# pip install flask pandas scikit-learn xgboost joblib
# Run: python app.py
# ==========================================

import os
import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ==========================================
# LOAD MODEL AT STARTUP
# ==========================================

MODEL_PATH      = os.path.join("model", "xgboost_ai_detector.pkl")
VECTORIZER_PATH = os.path.join("model", "tfidf_vectorizer.pkl")

model      = None
vectorizer = None

def load_model():
    global model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        print("Loading model...")
        model      = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("Model loaded successfully.")
    else:
        print("WARNING: Model files not found.")
        print(f"  Expected: {MODEL_PATH}")
        print(f"  Expected: {VECTORIZER_PATH}")
        print("  Run train_model.py first to train and save the model.")

load_model()

# ==========================================
# ROUTES
# ==========================================

@app.route("/")
def index():
    """Serve the main UI page."""
    return render_template("index.html")


@app.route("/graph-theory")
def graph_theory():
    """Serve the Graph Theory Foundation educational project."""
    return render_template("graph_theory.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict
    Body (JSON): { "text": "..." }
    Returns:     { "prediction": "AI"|"Human", "ai_prob": float, "human_prob": float, "confidence": float }
    """
    if model is None or vectorizer is None:
        return jsonify({
            "error": "Model not loaded. Please run train_model.py first."
        }), 503

    data = request.get_json(force=True)
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided."}), 400

    if len(text) < 20:
        return jsonify({"error": "Text is too short. Please enter at least 20 characters."}), 400

    # Vectorise & predict
    vec         = vectorizer.transform([text])
    prediction  = int(model.predict(vec)[0])
    proba       = model.predict_proba(vec)[0]

    human_prob  = float(proba[0]) * 100
    ai_prob     = float(proba[1]) * 100
    confidence  = max(human_prob, ai_prob)

    label = "AI Generated" if prediction == 1 else "Human Written"

    return jsonify({
        "prediction" : label,
        "ai_prob"    : round(ai_prob,    2),
        "human_prob" : round(human_prob, 2),
        "confidence" : round(confidence, 2),
        "is_ai"      : prediction == 1
    })


@app.route("/status")
def status():
    """Health-check endpoint."""
    return jsonify({
        "model_loaded": model is not None,
        "status": "ready" if model is not None else "model_missing"
    })


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    print("\n====================================")
    print("   AI Content Detector — Flask App  ")
    print("====================================")
    print("Open your browser at: http://127.0.0.1:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
