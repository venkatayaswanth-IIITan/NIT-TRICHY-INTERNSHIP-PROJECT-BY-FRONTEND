# ==========================================
# AI CONTENT DETECTOR — TRAINING SCRIPT
# Run this once to train & save the model.
# ==========================================
# pip install pandas numpy scikit-learn xgboost joblib
# ==========================================

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# ==========================================
# LOAD DATASET
# ==========================================

DATASET_PATH = "dataset.csv"

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset not found at '{DATASET_PATH}'.\n"
        "Please place your dataset.csv file in this directory.\n"
        "Expected columns: 'text' (string) and 'label' (0=Human, 1=AI)."
    )

print("Loading dataset...")
df = pd.read_csv(DATASET_PATH)

X = df["text"].astype(str)
y = df["label"]

print(f"  Total samples : {len(df)}")
print(f"  Human (0)     : {(y == 0).sum()}")
print(f"  AI    (1)     : {(y == 1).sum()}")

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================================
# TF-IDF VECTORIZATION
# ==========================================

print("\nVectorizing text (TF-IDF)...")
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

# ==========================================
# XGBOOST MODEL
# ==========================================

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)

print("Training XGBoost model...")
model.fit(X_train_vec, y_train)

# ==========================================
# EVALUATION
# ==========================================

predictions = model.predict(X_test_vec)
accuracy    = accuracy_score(y_test, predictions)

print(f"\n{'='*40}")
print(f"  Accuracy : {round(accuracy * 100, 2)}%")
print(f"{'='*40}")
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=["Human", "AI"]))

# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs("model", exist_ok=True)

joblib.dump(model,      "model/xgboost_ai_detector.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("Model saved → model/xgboost_ai_detector.pkl")
print("Vectorizer saved → model/tfidf_vectorizer.pkl")
print("\nTraining complete! You can now run: python app.py")
