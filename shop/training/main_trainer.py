import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from bag_of_words import train_bow_model
from tfidf import train_tfidf_model
from word2vec import train_word2vec_model

base_dir = Path(__file__).resolve().parent
csv_file_path = base_dir / 'data' / 'avis.csv'

df = pd.read_csv(csv_file_path, delimiter=';')
X = df['phrase'].values
y = df['label'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("=== Entraînement Bag of Words ===")
train_bow_model(X_train, X_test, y_train, y_test)

print("\n=== Entraînement TF-IDF ===")
train_tfidf_model(X_train, X_test, y_train, y_test)

print("\n=== Entraînement Word2Vec ===")
train_word2vec_model(X_train, X_test, y_train, y_test)