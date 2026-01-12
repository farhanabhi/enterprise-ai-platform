from sqlalchemy.orm import Session
from backend.crm_models import Client, Lead, Interaction


def crm_summary(db: Session):
    total_clients = db.query(Client).count()
    total_leads = db.query(Lead).count()
    total_interactions = db.query(Interaction).count()

    lead_status_count = {}
    for lead in db.query(Lead).all():
        lead_status_count[lead.status] = lead_status_count.get(lead.status, 0) + 1

    return {
        "total_clients": total_clients,
        "total_leads": total_leads,
        "total_interactions": total_interactions,
        "lead_status_distribution": lead_status_count
    }

def generate_insights(summary: dict):
    insights = []

    if summary["total_leads"] == 0:
        insights.append("No leads available. Start generating leads.")
    elif summary["total_interactions"] < summary["total_leads"]:
        insights.append("Many leads have no interactions. Follow-ups are required.")

    if summary["lead_status_distribution"].get("new", 0) > 3:
        insights.append("High number of new leads. Consider prioritizing conversion.")

    if not insights:
        insights.append("CRM activity looks healthy.")

    return insights
