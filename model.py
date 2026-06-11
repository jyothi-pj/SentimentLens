import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import re

# Load dataset
df = pd.read_csv("Reviews.csv")

# Use 'Score' column to create sentiment labels
# Scores 1-2 = negative, 3 = neutral, 4-5 = positive
def get_sentiment(score):
    if score <= 2:
        return "negative"
    elif score == 3:
        return "neutral"
    else:
        return "positive"

df = df.dropna(subset=["Text", "Score"])
df["sentiment"] = df["Score"].apply(get_sentiment)

# Clean text
def clean_text(text):
    text = re.sub(r"<.*?>", "", str(text))
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.lower().strip()

df["clean_text"] = df["Text"].apply(clean_text)

# Sample for faster training (use full data if time permits)
df_sample = df.sample(n=min(500000, len(df)), random_state=42)

X = df_sample["clean_text"]
y = df_sample["sentiment"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000, solver="lbfgs")
model.fit(X_train_vec, y_train)

# Evaluate
print("=== Model Performance ===")
print(classification_report(y_test, model.predict(X_test_vec)))

# Save model & vectorizer
joblib.dump(model, "sentiment_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model saved successfully!")
