from sqlalchemy.orm import Session
from backend.crm_models import Lead, Interaction


def lead_conversion_rate(db: Session):
    total_leads = db.query(Lead).count()
    converted = db.query(Lead).filter(Lead.status == "converted").count()

    if total_leads == 0:
        return 0.0

    return round((converted / total_leads) * 100, 2)


def average_interactions_per_lead(db: Session):
    total_leads = db.query(Lead).count()
    total_interactions = db.query(Interaction).count()

    if total_leads == 0:
        return 0.0

    return round(total_interactions / total_leads, 2)


def lead_status_distribution(db: Session):
    distribution = {}

    leads = db.query(Lead).all()
    for lead in leads:
        distribution[lead.status] = distribution.get(lead.status, 0) + 1

    return distribution
