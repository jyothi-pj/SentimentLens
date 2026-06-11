# Sentiment Analysis of E-Commerce Product Reviews

## 📌 Project Overview

With the rapid growth of e-commerce platforms, customers rely heavily on product reviews before making purchasing decisions. However, manually reading hundreds or thousands of reviews is time-consuming and inefficient.

This project presents an AI-powered sentiment analysis system that automatically extracts product reviews from e-commerce websites, analyzes customer sentiment using Machine Learning, provides confidence scores, explains predictions through important keywords, and generates intelligent product recommendations.

The system helps users quickly understand overall customer opinion and make informed purchasing decisions without reading every review individually.

---

## 🎯 Objectives

* Automatically extract product reviews from e-commerce websites.
* Classify reviews into Positive, Neutral, and Negative sentiments.
* Provide prediction confidence scores.
* Explain sentiment predictions using important keywords.
* Generate automated product recommendations.
* Reduce manual effort in analyzing large numbers of reviews.

---

## 🚀 Features

### Review Extraction

* Extracts customer reviews directly from Amazon product pages.
* Uses Playwright for browser automation and scraping.

### Sentiment Analysis

* Classifies reviews into:

  * Positive
  * Neutral
  * Negative

### Explainable AI (XAI)

* Displays top influential words responsible for sentiment prediction.

### Confidence Score

* Shows model confidence percentage for every prediction.

### Product Recommendation Engine

* Generates recommendations based on overall sentiment distribution.
* Provides reasons for recommendations.

### Interactive Web Interface

* User-friendly Flask-based web application.
* Displays sentiment summary using visual cards.

---

## 🛠 Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Flask (Python)

### Machine Learning

* Scikit-Learn
* Logistic Regression
* TF-IDF Vectorization

### Data Processing

* Pandas
* Regular Expressions (Regex)

### Web Scraping

* Playwright
* Beautifulsoup
* request

### Model Storage

* Joblib

---

## 📂 Project Structure

```text
Sentiment-Analysis-Ecommerce-Reviews/
│
├── app.py
├── model.py
├── scraper.py
├── amazon_login.py
├── Reviews.csv
├── sentiment_model.pkl
├── tfidf_vectorizer.pkl
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## 📊 Dataset

Dataset Used: Reviews.csv

The dataset contains:

* Review Text
* Review Score (1–5)

### Sentiment Mapping

| Rating Score | Sentiment |
| ------------ | --------- |
| 1 - 2        | Negative  |
| 3            | Neutral   |
| 4 - 5        | Positive  |

---

## ⚙️ Machine Learning Pipeline

### 1. Data Preprocessing

* Remove HTML tags
* Remove special characters
* Convert text to lowercase
* Remove unnecessary spaces

### 2. Feature Extraction

TF-IDF Vectorization

```python
TfidfVectorizer(
    max_features=5000,
    stop_words='english'
)
```

### 3. Model Training

Logistic Regression Classifier

```python
LogisticRegression(
    max_iter=1000,
    solver='lbfgs'
)
```

### 4. Model Evaluation

Evaluation Metrics:

* Precision
* Recall
* F1-Score
* Accuracy

---

## 🔄 System Workflow

1. User enters Amazon product URL.
2. Reviews are scraped using Playwright.
3. Reviews are cleaned and preprocessed.
4. TF-IDF converts text into numerical vectors.
5. Logistic Regression predicts sentiment.
6. Confidence score is calculated.
7. Explainable AI identifies important keywords.
8. Recommendation engine generates final recommendation.
9. Results are displayed through the Flask web interface.

---

## 💡 Explainable AI

The system improves transparency by displaying influential keywords responsible for predictions.

Example:

Review:

```text
The product quality is excellent and worth buying.
```

Prediction:

```text
Positive (96%)
```

Important Words:

```text
excellent, quality, worth
```

---

## 📈 Recommendation Generation

The recommendation engine analyzes all extracted reviews.

### Recommended

Generated when positive reviews dominate.

### Not Recommended

Generated when negative reviews dominate.

### Neutral / Mixed Reviews

Generated when sentiments are balanced.

---

## ▶️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/sentiment-analysis-ecommerce-reviews.git

cd sentiment-analysis-ecommerce-reviews
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright

```bash
pip install playwright

playwright install
```

---

## ▶️ Train the Model

```bash
python model.py
```

Generated Files:

```text
sentiment_model.pkl
tfidf_vectorizer.pkl
```

---

## ▶️ Amazon Login Setup

Run:

```bash
python amazon_login.py
```

Login to Amazon manually once.

The session will be stored in:

```text
amazon_profile/
```

---

## ▶️ Run Application

```bash
python app.py
```

Open Browser:

```text
http://127.0.0.1:5000
```

Paste an Amazon product URL and click Analyze.

---

## 📋 Sample Output

### Product Summary

```text
Positive Reviews : 75%
Neutral Reviews  : 10%
Negative Reviews : 15%
```

### Final Recommendation

```text
Recommended
```

Reason:

```text
Customers highlighted positive aspects such as quality, value, and performance.
```

---

## 🔍 Future Enhancements

* Support Flipkart review extraction.
* Support Snapdeal review extraction.
* Add review summarization using Large Language Models.
* Add visualization dashboards.
* Deploy on cloud platforms.
* Real-time sentiment monitoring.
* Multi-language sentiment analysis.
* Deep Learning models (LSTM, BERT, RoBERTa).

---

## 🎓 Academic Relevance

This project demonstrates practical applications of:

* Machine Learning
* Natural Language Processing (NLP)
* Explainable AI (XAI)
* Sentiment Analysis
* Web Scraping
* Flask Web Development

---

## 👨‍💻 Contributors

Project developed as part of an academic mini-project/major project on:

**Sentiment Analysis of E-Commerce Product Reviews**

---

## 📜 License

This project is intended for educational and research purposes.
