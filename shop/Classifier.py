import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class Classifier:
    def __init__(self):
        self.model = joblib.load('shop/model_saved.joblib')
        self.vectorizer = joblib.load('shop/vectorizer.joblib')

    def analyze_sentiment(self, text):
        text_transformed = self.vectorizer.transform([text])

        prediction = self.model.predict(text_transformed)
        return prediction[0]    # Predict sentiment (0 for negative, 1 for positive)