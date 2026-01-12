import joblib
import pandas as pd
import shap
from backend.crm_models import Interaction
from backend.database import SessionLocal

MODEL_PATH = "ml/models/lead_conversion_model.pkl"


def explain_lead_prediction(lead_id: int):
    model = joblib.load(MODEL_PATH)

    db = SessionLocal()
    interaction_count = db.query(Interaction).filter(
        Interaction.lead_id == lead_id
    ).count()
    db.close()

    X = pd.DataFrame([{
        "interaction_count": interaction_count
    }])

    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    explanation = {
        "interaction_count": float(shap_values.values[0][0])
    }

    return explanation
