# NIT Trichy Internship Projects — Web Platform

A unified Flask web platform hosting **two NIT Trichy internship projects** under one server.

## 🌐 Live Demo

> **Deployed on Render:** [https://nit-trichy-detector.onrender.com](https://nit-trichy-detector.onrender.com)

| Project | Live URL |
|---------|----------|
| 🤖 AI Content Detector | [https://nit-trichy-detector.onrender.com/](https://nit-trichy-detector.onrender.com/) |
| 📐 Graph Theory Platform | [https://nit-trichy-detector.onrender.com/graph-theory](https://nit-trichy-detector.onrender.com/graph-theory) |

---

## 📁 Project Structure

```
AI CONTENT DETECTION/
│
├── app.py                        # Flask server — routes for both projects
├── train_model.py                # ML training script (run once locally)
├── requirements.txt              # Runtime dependencies (Flask, gunicorn, XGBoost…)
├── requirements-train.txt        # Training-only dependencies (adds pandas)
├── Procfile                      # Render/Heroku start command
├── runtime.txt                   # Python version for Render
├── vercel.json                   # Vercel config (not recommended — see note)
├── .gitignore                    # Excludes dataset, cache, IDE files
├── README.md                     # This file
│
├── dataset.csv                   # Training data — place here before training (gitignored)
│
├── model/                        # Committed after training (needed for deployment)
│   ├── xgboost_ai_detector.pkl   # Trained XGBoost model
│   └── tfidf_vectorizer.pkl      # Fitted TF-IDF vectorizer
│
├── templates/
│   ├── index.html                # AI Content Detector UI
│   └── graph_theory.html         # Graph Theory Platform UI
│
├── static/
│   ├── css/
│   │   ├── style.css             # AI Detector styles (dark glassmorphism)
│   │   └── graph-theory.css      # Graph Theory styles
│   └── js/
│       └── app.js                # AI Detector frontend logic
│
└── frontend-project/             # Original cloned repo (untouched)
    ├── index.html
    ├── style.css
    ├── README.md
    └── PROJECT OVERVIEW.pdf
```

---

## 🚀 Local Setup

### 1. Install Runtime Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the AI Model (Local Only)

> ⚠️ Place your `dataset.csv` in the project root first.
>
> **Required columns:**
> | Column | Type | Description |
> |--------|------|-------------|
> | `text` | string | The text content |
> | `label` | int | `0` = Human Written, `1` = AI Generated |

Install training dependencies:
```bash
pip install -r requirements-train.txt
```

Run training:
```bash
python train_model.py
```

This saves:
- `model/xgboost_ai_detector.pkl`
- `model/tfidf_vectorizer.pkl`

### 3. Run Locally

```bash
python app.py
```

Open → **http://127.0.0.1:5000**

Or with gunicorn (same as Render):
```bash
gunicorn app:app
```

---

## ☁️ Deploy on Render (Recommended)

> Render is used instead of Vercel because ML dependencies (XGBoost + scikit-learn) exceed Vercel's 500MB Lambda limit.

### Render Configuration

| Setting | Value |
|---------|-------|
| **Platform** | [render.com](https://render.com) |
| **Service Type** | Web Service |
| **Runtime** | Python 3 |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | Free |

### Files Required for Render

#### `Procfile`
```
web: gunicorn app:app
```

#### `runtime.txt`
```
3.11.0
```

#### `requirements.txt`
```
flask>=2.3.0
gunicorn>=21.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
joblib>=1.3.0
numpy>=1.24.0
```

### Deploy Steps

**Step 1** — Train model locally and commit it:
```bash
# Place dataset.csv in project root, then:
python train_model.py

git add model/
git commit -m "Add trained model files"
git push origin main
```

**Step 2** — Connect repo on Render:
1. Go to [dashboard.render.com](https://dashboard.render.com) → **New + → Web Service**
2. Connect GitHub repo: `venkatayaswanth-IIITan/NIT-TRICHY-INTERNSHIP-PROJECT-BY-FRONTEND`
3. Fill in the configuration above
4. Click **"Create Web Service"**

**Step 3** — Auto-deploy on every push:
```bash
git add .
git commit -m "your message"
git push origin main
# Render automatically redeploys!
```

---

## 🌐 Flask Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | AI Content Detector UI |
| `/graph-theory` | GET | Graph Theory Platform UI |
| `/predict` | POST | Prediction API (JSON) |
| `/status` | GET | Model health check |

---

## 🔌 Prediction API

**Endpoint:** `POST /predict`

**Request:**
```json
{ "text": "The text you want to analyze..." }
```

**Response:**
```json
{
  "prediction": "AI Generated",
  "is_ai": true,
  "ai_prob": 94.72,
  "human_prob": 5.28,
  "confidence": 94.72
}
```

**Error Responses:**
```json
{ "error": "Text is too short. Please enter at least 20 characters." }
{ "error": "Model not loaded. Please run train_model.py first." }
```

**Test with curl:**
```bash
curl -X POST https://nit-trichy-detector.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Paste your text here to check if it is AI generated or human written."}'
```

---

## 🧠 Project 1 — AI Content Detector

Detects whether text was written by a human or generated by AI.

### Model Details

| Parameter | Value |
|-----------|-------|
| Algorithm | XGBoost Classifier |
| Vectorizer | TF-IDF |
| Max Features | 10,000 |
| N-gram Range | (1, 2) |
| Stop Words | English |
| Estimators | 300 |
| Max Depth | 6 |
| Learning Rate | 0.1 |
| Objective | `binary:logistic` |
| Eval Metric | `logloss` |
| Train/Test Split | 80% / 20% |
| Random State | 42 |

### UI Features
- Dark glassmorphism design with animated gradient orbs
- Real-time prediction with animated probability bars
- Human vs AI confidence gauge slider
- Character counter + `Ctrl+Enter` keyboard shortcut
- Project switcher — navigate between both NIT Trichy projects
- Full error handling
- Fully responsive (mobile-friendly)

---

## 📐 Project 2 — Graph Theory Foundation Platform

Educational web platform for mastering Graph Theory at NIT Trichy.

**Source Repo:** [NIT-TRICHY-INTERNSHIP-PROJECT-BY-FRONTEND](https://github.com/venkatayaswanth-IIITan/NIT-TRICHY-INTERNSHIP-PROJECT-BY-FRONTEND)

### Features
- Interactive side navigation with NIT Trichy branding
- Structured learning roadmap (basics → advanced)
- Curated resources, articles, and reference books
- Video tutorials in multiple languages
- GATE MCQs and Previous Year Questions (PYQs)
- AI chatbot for Graph Theory doubt resolution
- Direct faculty contact — Prof. Pavan, CSE Dept., NIT Trichy
- Responsive design for desktop, tablet, and mobile

### Technologies
- HTML5, CSS3
- React 17 (via CDN)
- Babel (JSX via CDN)
- Vanilla JavaScript

---

## 🔗 Navigation Between Projects

| From | To | How |
|------|----|-----|
| AI Detector (`/`) | Graph Theory (`/graph-theory`) | Click "Graph Theory Platform" card |
| Graph Theory (`/graph-theory`) | AI Detector (`/`) | Click "AI Detector" pill (top-right) |
| Graph Theory sidebar | AI Detector | Bottom link in side nav |

---

## ⚠️ Deployment Notes

> **Cold Starts**: Render's free tier spins down after 15 min inactivity.
> First request after idle may take 30–60 seconds to wake up.

> **Model Files**: The `model/` folder (`.pkl` files) must be committed to GitHub
> before deploying — otherwise predictions return a 503 error.
> The `.gitignore` is configured to allow model files.

> **Vercel Not Recommended**: XGBoost + scikit-learn = ~860MB, exceeds Vercel's 500MB limit.

---

## 📦 All Dependencies

**Runtime (`requirements.txt`):**
```
flask>=2.3.0
gunicorn>=21.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
joblib>=1.3.0
numpy>=1.24.0
```

**Training only (`requirements-train.txt`):**
```
pandas>=2.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
joblib>=1.3.0
numpy>=1.24.0
```

Install runtime:
```bash
pip install -r requirements.txt
```

Install for training:
```bash
pip install -r requirements-train.txt
```

---

## 🎓 Acknowledgements

- **National Institute of Technology, Tiruchirappalli (NIT Trichy)**
- **Computer Science & Engineering Department**
- Course Instructor: [Prof. Pavan](https://www.nitt.edu/home/academics/departments/cse/faculty/pavan/)
- Graph Theory Frontend: [venkatayaswanth-IIITan](https://github.com/venkatayaswanth-IIITan)

---

**Made with ❤️ for NIT Trichy Internship 2025**
