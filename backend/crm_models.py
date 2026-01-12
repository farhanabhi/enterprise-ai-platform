from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    industry = Column(String)

    leads = relationship("Lead", back_populates="client")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="new")
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="leads")
    interactions = relationship("Interaction", back_populates="lead")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    note = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    lead_id = Column(Integer, ForeignKey("leads.id"))

    lead = relationship("Lead", back_populates="interactions")
