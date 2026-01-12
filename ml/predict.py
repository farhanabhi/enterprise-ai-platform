import joblib
import pandas as pd
from backend.crm_models import Interaction
from backend.database import SessionLocal

MODEL_PATH = "ml/models/lead_conversion_model.pkl"


def predict_lead_conversion(lead_id: int):
    model = joblib.load(MODEL_PATH)

    db = SessionLocal()
    interaction_count = db.query(Interaction).filter(
        Interaction.lead_id == lead_id
    ).count()
    db.close()

    X = pd.DataFrame([{
        "interaction_count": interaction_count
    }])

    probability = model.predict_proba(X)[0][1]

    return round(float(probability), 3)
