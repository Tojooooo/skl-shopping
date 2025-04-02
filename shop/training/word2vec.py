from gensim.models import Word2Vec
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import os

nltk.download('punkt')


def train_word2vec_model(X_train, X_test, y_train, y_test):
    # Tokenisation
    tokenized_train = [word_tokenize(sentence.lower()) for sentence in X_train]
    tokenized_test = [word_tokenize(sentence.lower()) for sentence in X_test]

    # Entraînement Word2Vec
    w2v_model = Word2Vec(
        sentences=tokenized_train,
        vector_size=150,
        window=7,
        min_count=2,
        sg=1,
        workers=4
    )

    # Transformation des phrases en vecteurs
    def get_sentence_vector(tokens):
        vectors = [w2v_model.wv[word] for word in tokens if word in w2v_model.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(w2v_model.vector_size)

    X_train_w2v = np.array([get_sentence_vector(tokens) for tokens in tokenized_train])
    X_test_w2v = np.array([get_sentence_vector(tokens) for tokens in tokenized_test])

    # Entraînement du modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_w2v, y_train)

    # Évaluation test
    y_pred = model.predict(X_test_w2v)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Matrice de confusion:")
    print(confusion_matrix(y_test, y_pred))

    # Sauvegarde
    dump(model, 'models/w2v_rf_model.joblib')
    w2v_model.save('models/w2v_model.model')
    print("Modèles Word2Vec sauvegardés dans models/")