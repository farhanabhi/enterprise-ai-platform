import joblib
from sklearn.linear_model import LogisticRegression
from ml.data_pipeline import build_lead_dataset
from backend.database import SessionLocal


MODEL_PATH = "ml/models/lead_conversion_model.pkl"


def train_model():
    db = SessionLocal()
    df = build_lead_dataset(db)
    db.close()

    if df.empty:
        print("No data available for training")
        return

    if df["converted"].nunique() < 2:
        print("Not enough class diversity to train model (need converted + non-converted)")
        return

    X = df[["interaction_count"]]
    y = df["converted"]

    model = LogisticRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved successfully")

if __name__ == "__main__":
    train_model()
