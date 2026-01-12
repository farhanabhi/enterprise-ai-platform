from sqlalchemy.orm import Session
from backend.crm_models import Client, Lead, Interaction


def create_client(db: Session, data):
    client = Client(
        name=data.name,
        email=data.email,
        phone=data.phone,
        industry=data.industry
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def list_clients(db: Session):
    return db.query(Client).all()


def create_lead(db: Session, data):
    lead = Lead(
        title=data.title,
        client_id=data.client_id
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def add_interaction(db: Session, data):
    interaction = Interaction(
        note=data.note,
        lead_id=data.lead_id
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction
