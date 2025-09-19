from fastapi import FastAPI
from app.database import Base, engine
from app.models.model import *
from app.routers import auth, users, apikeys, usage, billing

app = FastAPI(title="API Contratos Sociais")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(apikeys.router)
app.include_router(usage.router)
app.include_router(billing.router)

@app.get("/")
def root():
    return {"message": "API rodando 🚀"}