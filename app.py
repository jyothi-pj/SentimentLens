from flask import Flask, render_template, request, jsonify
import joblib
import re
from scraper import scrape_reviews

app = Flask(__name__)

# Load trained model
model = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


def clean_text(text):
    text = re.sub(r"<.*?>", "", str(text))
    text = re.sub(r"read\s*more", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def clean_display_text(text):
    text = str(text)
    text = re.sub(r"read\s*more", "", text, flags=re.IGNORECASE)
    text = text.replace("…", "").replace("...", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Explainable AI — important words influencing prediction
def get_top_words(review, sentiment):
    vec = vectorizer.transform([review])
    feature_names = vectorizer.get_feature_names_out()
    coefs = model.coef_

    class_index = list(model.classes_).index(sentiment)
    weights = coefs[class_index]

    indices = vec.nonzero()[1]
    word_scores = [(feature_names[i], weights[i]) for i in indices]

    word_scores = sorted(word_scores, key=lambda x: abs(x[1]), reverse=True)

    return [w[0] for w in word_scores[:3]]


def analyze_sentiment(reviews):
    results = []

    reviews = list(dict.fromkeys(reviews))
    reviews = reviews[:15]

    for review in reviews:
        cleaned = clean_text(review)
        vec = vectorizer.transform([cleaned])

        sentiment = model.predict(vec)[0]
        confidence = max(model.predict_proba(vec)[0])

        display_review = clean_display_text(review)

        explanation = get_top_words(cleaned, sentiment)

        results.append({
            "review": display_review[:200] + "..." if len(display_review) > 200 else display_review,
            "sentiment": sentiment,
            "confidence": round(confidence * 100, 1),
            "explanation": explanation
        })

    return results


# Explainable AI Recommendation
def generate_recommendation(results):
    score = 0
    positive_words = []
    negative_words = []

    for r in results:
        if r["sentiment"] == "positive":
            score += 1
            positive_words.extend(r["explanation"])
        elif r["sentiment"] == "negative":
            score -= 1
            negative_words.extend(r["explanation"])

    if score > 0:
        recommendation = "Recommended"
        reason_words = list(set(positive_words))[:5]
        reason = "Customers highlighted positive aspects like: " + ", ".join(reason_words)

    elif score < 0:
        recommendation = "Not Recommended"
        reason_words = list(set(negative_words))[:5]
        reason = "Customers reported issues related to: " + ", ".join(reason_words)

    else:
        recommendation = "Neutral / Mixed Reviews"
        reason = "Both positive and negative feedback found."

    return recommendation, reason


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json.get("url", "")

    if not url:
        return jsonify({"error": "Please provide a product URL"}), 400

    product_name, reviews = scrape_reviews(url)

    if not reviews:
        return jsonify({"error": "Could not extract reviews. Try another product URL."})

    results = analyze_sentiment(reviews)

    sentiments = [r["sentiment"] for r in results]
    total = len(sentiments)

    summary = {
        "positive": round(sentiments.count("positive") / total * 100, 1),
        "negative": round(sentiments.count("negative") / total * 100, 1),
        "neutral": round(sentiments.count("neutral") / total * 100, 1),
        "overall": max(set(sentiments), key=sentiments.count),
        "total": total
    }

    recommendation, reason = generate_recommendation(results)

    return jsonify({
        "product_name": product_name,
        "results": results,
        "summary": summary,
        "recommendation": recommendation,
        "reason": reason
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)