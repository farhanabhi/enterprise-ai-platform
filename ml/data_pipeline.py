import pandas as pd
from sqlalchemy.orm import Session
from backend.crm_models import Lead, Interaction


def build_lead_dataset(db: Session):
    leads = db.query(Lead).all()
    rows = []

    for lead in leads:
        interaction_count = db.query(Interaction).filter(
            Interaction.lead_id == lead.id
        ).count()

        rows.append({
            "lead_id": lead.id,
            "interaction_count": interaction_count,
            "status": lead.status
        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Binary target: 1 = converted, 0 = not converted
    df["converted"] = df["status"].apply(
        lambda x: 1 if x == "converted" else 0
    )

    return df[["interaction_count", "converted"]]
