from pathlib import Path

base_dir = Path(__file__).resolve().parent

bow_model_path = base_dir / 'models' / 'bow_model.joblib'
bow_vectorizer_path = base_dir / 'models' / 'bow_vectorize.joblib'

tfidf_model_path = base_dir / 'models' / 'tfidf_model.joblib'
tfidf_vectorizer_path = base_dir / 'models' / 'tfidf_vectorize.joblib'

w2v_rf_model_path = base_dir / 'models' / 'w2v_rf_model.joblib'
w2v_model_path = base_dir / 'models' / 'w2v_model.model'