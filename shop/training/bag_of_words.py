from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump
import base_dir

def train_bow_model(X_train, X_test, y_train, y_test):
    # Initialization
    vectorizer = CountVectorizer()
    X_train_bow = vectorizer.fit_transform(X_train)
    X_test_bow = vectorizer.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_bow, y_train)

    # Évaluation test
    y_pred = model.predict(X_test_bow)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Matrice de confusion:")
    print(confusion_matrix(y_test, y_pred))

    # Sauvegarde
    dump(model, base_dir.bow_model_path)
    dump(vectorizer, base_dir.bow_vectorizer_path)
    print("Modèle BoW sauvegardé dans models/")