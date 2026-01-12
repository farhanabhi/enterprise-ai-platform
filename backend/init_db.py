from backend.database import engine
from backend import models
from backend import crm_models
from backend.models import Base

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("All tables created successfully")
