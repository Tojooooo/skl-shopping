import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
from pathlib import Path

nltk.download('punkt')

base_dir = Path(__file__).resolve().parent
bow_model_path = base_dir / 'training' / 'models' / 'bow_model.joblib'
bow_vectorizer_path = base_dir / 'training' / 'models' / 'bow_vectorize.joblib'

tfidf_model_path = base_dir / 'training' / 'models' / 'tfidf_model.joblib'
tfidf_vectorizer_path = base_dir / 'training' / 'models' / 'tfidf_vectorize.joblib'

w2v_rf_model_path = base_dir / 'training' / 'models' / 'w2v_rf_model.joblib'
w2v_model_path = base_dir / 'training' / 'models' / 'w2v_model.model'


class Classifier:
    def __init__(self):
        self.bow_model = joblib.load(bow_model_path)
        self.bow_vectorizer = joblib.load(bow_vectorizer_path)

        self.tfidf_model = joblib.load(tfidf_model_path)
        self.tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)

        self.w2v_model = joblib.load(w2v_rf_model_path)
        self.word2vec_model = Word2Vec.load(str(w2v_model_path))

    def analyze_sentiment(self, text, method='word2vec'):
        if method == 'bow':
            text_transformed = self.bow_vectorizer.transform([text])
            prediction = self.bow_model.predict(text_transformed)
        elif method == 'tfidf':
            text_transformed = self.tfidf_vectorizer.transform([text])
            prediction = self.tfidf_model.predict(text_transformed)
        elif method == 'word2vec':
            tokens = word_tokenize(text.lower())
            vectors = [self.word2vec_model.wv[word] for word in tokens if word in self.word2vec_model.wv]
            vector = np.mean(vectors, axis=0) if vectors else np.zeros(self.word2vec_model.vector_size)
            prediction = self.w2v_model.predict([vector])
        else:
            raise ValueError("Invalid method. Choose 'bow', 'tfidf', or 'word2vec'")

        return prediction[0]  # 0 for negative, 1 for positive

    def get_sentiment_label(self, prediction):
        return "Positive" if prediction == 1 else "Negative"

if __name__ == '__main__':
    # test
    classifier = Classifier()

    text = "Azo ekena"

    bow_prediction = classifier.analyze_sentiment(text, method='bow')
    tfidf_prediction = classifier.analyze_sentiment(text, method='tfidf')
    w2v_prediction = classifier.analyze_sentiment(text, method='word2vec')

    print(f"BoW Prediction: {classifier.get_sentiment_label(bow_prediction)}")
    print(f"TF-IDF Prediction: {classifier.get_sentiment_label(tfidf_prediction)}")
    print(f"Word2Vec Prediction: {classifier.get_sentiment_label(w2v_prediction)}")

