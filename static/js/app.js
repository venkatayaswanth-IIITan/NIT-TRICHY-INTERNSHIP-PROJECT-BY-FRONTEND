/* =============================================
   AI Content Detector — app.js
   Handles API calls & UI state updates
   ============================================= */

"use strict";

// ── DOM refs ──
const inputText      = document.getElementById("input-text");
const analyzeBtn     = document.getElementById("analyze-btn");
const btnText        = document.querySelector(".btn-text");
const btnSpinner     = document.getElementById("btn-spinner");
const btnIcon        = document.querySelector(".btn-icon");
const clearBtn       = document.getElementById("clear-btn");
const charCount      = document.getElementById("char-count");
const errorBanner    = document.getElementById("error-banner");
const errorText      = document.getElementById("error-text");
const resultsSection = document.getElementById("results-section");
const verdictBanner  = document.getElementById("verdict-banner");
const verdictIcon    = document.getElementById("verdict-icon");
const verdictTxt     = document.getElementById("verdict-text");
const confidenceVal  = document.getElementById("confidence-value");
const humanPct       = document.getElementById("human-pct");
const aiPct          = document.getElementById("ai-pct");
const humanBar       = document.getElementById("human-bar");
const aiBar          = document.getElementById("ai-bar");
const humanCard      = document.getElementById("human-card");
const aiCard         = document.getElementById("ai-card");
const gaugeFill      = document.getElementById("gauge-fill");
const gaugeThumb     = document.getElementById("gauge-thumb");

// ── Character Counter ──
inputText.addEventListener("input", () => {
  const len = inputText.value.length;
  charCount.textContent = len.toLocaleString();
  // Dim error on new input
  if (!errorBanner.hidden) showError(false);
});

// ── Clear Button ──
clearBtn.addEventListener("click", () => {
  inputText.value    = "";
  charCount.textContent = "0";
  resultsSection.hidden = true;
  showError(false);
  inputText.focus();
});

// ── Analyze Button ──
analyzeBtn.addEventListener("click", runAnalysis);

inputText.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runAnalysis();
});

async function runAnalysis() {
  const text = inputText.value.trim();

  // Client-side validation
  if (!text) {
    showError(true, "Please enter some text before analyzing.");
    return;
  }
  if (text.length < 20) {
    showError(true, "Text is too short. Please enter at least 20 characters.");
    return;
  }

  setLoading(true);
  showError(false);

  try {
    const response = await fetch("/predict", {
      method : "POST",
      headers: { "Content-Type": "application/json" },
      body   : JSON.stringify({ text }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(true, data.error || "An error occurred. Please try again.");
      return;
    }

    renderResults(data);

  } catch (err) {
    showError(true, "Network error. Make sure the Flask server is running.");
    console.error(err);
  } finally {
    setLoading(false);
  }
}

// ── Render Results ──
function renderResults(data) {
  const { is_ai, ai_prob, human_prob, confidence, prediction } = data;

  // Verdict banner
  verdictBanner.className = "verdict-banner " + (is_ai ? "is-ai" : "is-human");
  verdictIcon.textContent = is_ai ? "🤖" : "✍️";
  verdictTxt.textContent  = prediction;
  confidenceVal.textContent = confidence.toFixed(1) + "%";

  // Show results first (needed to animate bars)
  resultsSection.hidden = false;

  // Animate bars with a tiny delay for the transition to work
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      humanPct.textContent = human_prob.toFixed(1) + "%";
      aiPct.textContent    = ai_prob.toFixed(1)    + "%";
      humanBar.style.width = human_prob + "%";
      aiBar.style.width    = ai_prob    + "%";
      updateGauge(ai_prob);
    });
  });

  // Active card highlight
  humanCard.classList.toggle("active", !is_ai);
  aiCard.classList.toggle("active",    is_ai);

  // Scroll into view smoothly
  resultsSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Gauge ──
function updateGauge(aiProb) {
  // 0% = full human (left), 100% = full AI (right)
  const pct = aiProb; // directly maps

  // Gauge fill: from left (green) to right (purple) based on AI probability
  gaugeFill.style.width      = pct + "%";
  gaugeThumb.style.left      = pct + "%";

  if (pct >= 50) {
    gaugeThumb.style.borderColor = "#7c3aed";
    gaugeThumb.style.boxShadow   = "0 0 12px rgba(124,58,237,0.7)";
  } else {
    gaugeThumb.style.borderColor = "#10b981";
    gaugeThumb.style.boxShadow   = "0 0 12px rgba(16,185,129,0.7)";
  }
}

// ── Loading State ──
function setLoading(loading) {
  analyzeBtn.disabled   = loading;
  btnSpinner.hidden     = !loading;
  btnIcon.style.display = loading ? "none" : "";
  btnText.textContent   = loading ? "Analyzing..." : "Analyze Text";
}

// ── Error Banner ──
function showError(show, msg = "") {
  errorBanner.hidden = !show;
  if (show) errorText.textContent = msg;
}
