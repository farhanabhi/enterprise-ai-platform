from sqlalchemy.orm import Session
from backend.crm_models import Client, Lead, Interaction


def crm_summary_report(db: Session):
    return {
        "total_clients": db.query(Client).count(),
        "total_leads": db.query(Lead).count(),
        "total_interactions": db.query(Interaction).count(),
        "generated_at": "system_runtime"
    }
