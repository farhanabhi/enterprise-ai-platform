from sqlalchemy.orm import Session
from backend.analytics.kpis import (
    lead_conversion_rate,
    average_interactions_per_lead,
    lead_status_distribution
)


def build_dashboard(db: Session):
    return {
        "kpis": {
            "lead_conversion_rate": lead_conversion_rate(db),
            "avg_interactions_per_lead": average_interactions_per_lead(db)
        },
        "charts": {
            "lead_status_distribution": lead_status_distribution(db)
        }
    }
