from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend import schemas, crud
from backend.auth import create_access_token
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.auth import get_current_user
from backend import schemas, crud
from backend import crm_schemas, crm_crud
from backend import crm_crud





from backend.analytics.dashboard import build_dashboard
from backend.analytics.reports import crm_summary_report

from rag.ingest import ingest_documents
from rag.assistant import answer_question


app = FastAPI(
    title="Enterprise AI Platform",
    description="AI-powered ERP & Analytics System",
    version="0.1.0"
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "status": "Backend running successfully",
        "message": "Welcome to Enterprise AI Platform"
    }

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = crud.create_user(db, user.email, user.password)
    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticated_user = crud.authenticate_user(
        db, user.email, user.password
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={
            "sub": authenticated_user.email,
            "role": authenticated_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

from backend.auth import get_current_user

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You have access to this protected route",
        "user": current_user
    }

@app.get("/admin-only")
def admin_route(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": "Welcome Admin"}

@app.post("/crm/clients", response_model=crm_schemas.ClientResponse)
def create_client(
    client: crm_schemas.ClientCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crm_crud.create_client(db, client)


@app.get("/crm/clients")
def list_clients(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crm_crud.list_clients(db)


@app.post("/crm/leads", response_model=crm_schemas.LeadResponse)
def create_lead(
    lead: crm_schemas.LeadCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crm_crud.create_lead(db, lead)


@app.post("/crm/interactions", response_model=crm_schemas.InteractionResponse)
def add_interaction(
    interaction: crm_schemas.InteractionCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crm_crud.add_interaction(db, interaction)



@app.get("/analytics/dashboard")
def analytics_dashboard(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return build_dashboard(db)


@app.get("/analytics/reports/summary")
def analytics_report(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crm_summary_report(db)

@app.get("/ml/predict/lead/{lead_id}")
def predict_lead(
    lead_id: int,
    user: dict = Depends(get_current_user)
):
    from ml.predict import predict_lead_conversion  # 🔥 LAZY LOAD HERE

    probability = predict_lead_conversion(lead_id)

    return {
        "lead_id": lead_id,
        "conversion_probability": probability
    }


@app.get("/ml/explain/lead/{lead_id}")
def explain_lead(
    lead_id: int,
    user: dict = Depends(get_current_user)
):
    from ml.explain import explain_lead_prediction  # 🔥 LAZY LOAD

    explanation = explain_lead_prediction(lead_id)

    return {
        "lead_id": lead_id,
        "feature_contributions": explanation
    }


@app.post("/ai/ingest")
def ingest_ai_data(
    texts: list[str],
    user: dict = Depends(get_current_user)
):
    return ingest_documents(texts)


@app.post("/ai/assistant")
def ai_assistant(
    question: str,
    user: dict = Depends(get_current_user)
):
    answer = answer_question(question)
    return {"answer": answer}
