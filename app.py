from flask import Flask, render_template, request

app = Flask(__name__)

# Your scoring function
def score_text(text: str) -> dict:
    reasons = []

    keywords = ["registration fee", "whatsapp only", "no interview", "instant selection", "guaranteed certificate"]
    for word in keywords:
        if word.lower() in text.lower():
            reasons.append(f"Keyword: '{word}'")

    score = len(reasons)0
    risk_level = "Low"
    if score >= 10:
        risk_level = "High"
    elif score >= 6:
        risk_level = "Medium"

    return {"risk_score": score, "risk_level": risk_level, "reasons": reasons}

def predict(text: str) -> dict:
    result = score_text(text)
    result["label"] = "Fake" if result["risk_level"] in ["High", "Medium"] else "Likely Genuine"
    return result

# Home page
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        text = request.form.get("internship_text")
        result = predict(text)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)