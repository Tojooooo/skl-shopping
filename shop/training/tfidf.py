from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump
import base_dir

def train_tfidf_model(X_train, X_test, y_train, y_test):
    # Initialisation
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_tfidf, y_train)

    # test
    y_pred = model.predict(X_test_tfidf)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Matrice de confusion:")
    print(confusion_matrix(y_test, y_pred))

    # Sauvegarde
    print(base_dir.tfidf_model_path)
    dump(model, base_dir.tfidf_model_path)
    dump(vectorizer, base_dir.tfidf_vectorizer_path)
    print("Modèle TF-IDF sauvegardé dans models/")