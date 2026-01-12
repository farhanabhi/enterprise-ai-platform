from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    industry: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    industry: Optional[str] = None

    class Config:
        from_attributes = True


class LeadCreate(BaseModel):
    title: str
    client_id: int


class LeadResponse(BaseModel):
    id: int
    title: str
    status: str
    client_id: int

    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    note: str
    lead_id: int


class InteractionResponse(BaseModel):
    id: int
    note: str
    lead_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
