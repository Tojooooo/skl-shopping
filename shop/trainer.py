import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

df = pd.read_csv('data.csv')

X = df['comment-mg'].values  # phrases am teny gasy
y = df['sentiment'].values   # (1 pour positif, 0 pour négatif)

vectorizer = TfidfVectorizer()
X_transformed = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.3, random_state=42)

# Entraînement d'un modèle de classification (Naive Bayes)
model = MultinomialNB()
model.fit(X_train, y_train)

# Prédictions sur le jeu de test
y_pred = model.predict(X_test)

# Evaluation de l'accuracy
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

def predict_class(new_phrase):
    new_phrase_transformed = vectorizer.transform([new_phrase])

    # Prédiction de la classe (0 ou 1)
    prediction = model.predict(new_phrase_transformed)

    if prediction == 1:
        print(f"L'avis : '{new_phrase}' est un avis positif.")
    else:
        print(f"L'avis : '{new_phrase}' est un avis négatif.")

# Exemple d'utilisation : prédire la classe d'une nouvelle phrase
new_review = "Tsara"
predict_class(new_review)
# A la fin de l'entrainement
dump(model, 'model_saved.joblib')
dump(vectorizer, 'vectorizer.joblib')