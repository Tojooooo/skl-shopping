from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump


def train_tfidf_model(X_train, X_test, y_train, y_test):
    # Création et transformation TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Entraînement du modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_tfidf, y_train)

    # Évaluation
    y_pred = model.predict(X_test_tfidf)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Matrice de confusion:")
    print(confusion_matrix(y_test, y_pred))

    # Sauvegarde
    dump(model, 'models/tfidf_model.joblib')
    dump(vectorizer, 'models/tfidf_vectorizer.joblib')
    print("Modèle TF-IDF sauvegardé dans models/")