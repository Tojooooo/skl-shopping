import pandas as pd
import nltk
import string
import joblib
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Téléchargement des stopwords si ce n'est pas déjà fait
nltk.download('stopwords')

# Exemple de dataset (tu peux utiliser un fichier CSV au lieu de cette liste)
# df = pd.read_csv("documents_comment.csv",delimiter=";") 
# X = df["Comments"]
# y = df["type"]

# # Nettoyage des textes
# def preprocess_text(text):
#     text = text.lower()  # Mise en minuscule
#     text = text.translate(str.maketrans("", "", string.punctuation))  # Suppression des ponctuations
#     words = text.split()
#     words = [word for word in words if word not in stopwords.words('french')]  # Suppression des stopwords
#     return " ".join(words)

# # Appliquer le prétraitement
# df["commentaire_clean"] = df["Comments"].apply(preprocess_text)

# # Séparation des données
# X_train, X_test, y_train, y_test = train_test_split(df["commentaire_clean"], df["type"], test_size=0.2, random_state=42)

# # 🔹 Option 1 : Modèle avec Bag of Words (BoW)
# bow_model = Pipeline([
#     ("vectorizer", CountVectorizer()),  # BoW
#     ("classifier", LogisticRegression())  # Régression Logistique
# ])

# # 🔹 Option 2 : Modèle avec TF-IDF (Word Embedding)
# tfidf_model = Pipeline([
#     ("vectorizer", TfidfVectorizer()),  # TF-IDF
#     ("classifier", RandomForestClassifier(n_estimators=100))  # Random Forest
# ])

# # Entraînement des modèles
# bow_model.fit(X_train, y_train)
# tfidf_model.fit(X_train, y_train)

# # Évaluation des modèles
# y_pred_bow = bow_model.predict(X_test)
# y_pred_tfidf = tfidf_model.predict(X_test)



# print("🔹 Bag of Words Model")
# print(classification_report(y_test, y_pred_bow))

# print("🔹 TF-IDF Model")
# print(classification_report(y_test, y_pred_tfidf))

# joblib.dump(bow_model,"bow_model.plk")
# joblib.dump(tfidf_model,"tfidf_model.plk")

# 🔥 Tester avec un nouveau commentaire


print(f"\nPrédiction BoW: {pred_bow}")
print(f"Prédiction TF-IDF: {pred_tfidf}")
