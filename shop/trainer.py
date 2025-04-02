import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from gensim.models import Word2Vec
import numpy as np
import nltk
from nltk.tokenize import word_tokenize

# Télécharger les ressources nécessaires de NLTK
nltk.download('punkt')

# Chargement des données
df = pd.read_csv('training/data/data.csv')
X = df['comment-mg'].values  # phrases en malgache
y = df['sentiment'].values  # (1 pour positif, 0 pour négatif)


# Fonction pour la représentation Bag of Words
def get_bow_representation(X_train, X_test):
    vectorizer = CountVectorizer()
    X_train_transformed = vectorizer.fit_transform(X_train)
    X_test_transformed = vectorizer.transform(X_test)
    return X_train_transformed, X_test_transformed, vectorizer


# Fonction pour la représentation TF-IDF
def get_tfidf_representation(X_train, X_test):
    vectorizer = TfidfVectorizer()
    X_train_transformed = vectorizer.fit_transform(X_train)
    X_test_transformed = vectorizer.transform(X_test)
    return X_train_transformed, X_test_transformed, vectorizer


# Fonction pour la représentation Word2Vec
def get_word2vec_representation(X_train, X_test, vector_size=100):
    # Tokenisation des phrases
    tokenized_train = [word_tokenize(sentence.lower()) for sentence in X_train]
    tokenized_test = [word_tokenize(sentence.lower()) for sentence in X_test]

    # Entraînement du modèle Word2Vec
    w2v_model = Word2Vec(sentences=tokenized_train, vector_size=vector_size, window=5, min_count=1, workers=4)

    # Fonction pour obtenir la représentation moyenne d'une phrase
    def get_sentence_vector(sentence_tokens):
        vectors = []
        for token in sentence_tokens:
            if token in w2v_model.wv:
                vectors.append(w2v_model.wv[token])
        if len(vectors) > 0:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(vector_size)

    # Transformation des données
    X_train_transformed = np.array([get_sentence_vector(tokens) for tokens in tokenized_train])
    X_test_transformed = np.array([get_sentence_vector(tokens) for tokens in tokenized_test])

    return X_train_transformed, X_test_transformed, w2v_model


# Fonction pour entraîner et évaluer le modèle
def train_and_evaluate(X_train, X_test, y_train, y_test, representation_name):
    print(f"\n=== Evaluation avec {representation_name} ===")

    # Entraînement du modèle Random Forest
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)

    # Prédictions et évaluation
    y_pred = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Matrice de confusion:")
    print(confusion_matrix(y_test, y_pred))

    return model


# Séparation des données en train et test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entraînement avec les différentes représentations
# 1. Bag of Words
X_train_bow, X_test_bow, bow_vectorizer = get_bow_representation(X_train, X_test)
bow_model = train_and_evaluate(X_train_bow, X_test_bow, y_train, y_test, "Bag of Words")

# 2. TF-IDF
X_train_tfidf, X_test_tfidf, tfidf_vectorizer = get_tfidf_representation(X_train, X_test)
tfidf_model = train_and_evaluate(X_train_tfidf, X_test_tfidf, y_train, y_test, "TF-IDF")

# 3. Word2Vec
X_train_w2v, X_test_w2v, w2v_model = get_word2vec_representation(X_train, X_test)
w2v_model_rf = train_and_evaluate(X_train_w2v, X_test_w2v, y_train, y_test, "Word2Vec")


# Fonction pour prédire avec n'importe quel modèle
def predict_class(model, vectorizer, new_phrase, representation_type):
    if representation_type == "Word2Vec":
        tokens = word_tokenize(new_phrase.lower())
        new_phrase_transformed = np.array([get_sentence_vector(tokens)])
    else:
        new_phrase_transformed = vectorizer.transform([new_phrase])

    prediction = model.predict(new_phrase_transformed)

    if prediction == 1:
        print(f"L'avis : '{new_phrase}' est un avis positif.")
    else:
        print(f"L'avis : '{new_phrase}' est un avis négatif.")


# Exemple d'utilisation avec TF-IDF
new_review = "Tsara"
print("\nPrédiction avec TF-IDF:")
predict_class(tfidf_model, tfidf_vectorizer, new_review, "TF-IDF")

# Sauvegarde des modèles
dump(bow_model, 'bow_model.joblib')
dump(bow_vectorizer, 'bow_vectorizer.joblib')
dump(tfidf_model, 'tfidf_model.joblib')
dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
dump(w2v_model_rf, 'w2v_model_rf.joblib')
dump(w2v_model, 'w2v_model.joblib')