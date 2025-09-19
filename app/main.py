from fastapi import FastAPI
from app.database import engine, Base

import app.models.user
# import app.models.apikey
# import app.models.usage_log
# import app.models.billing
# import app.models.contract_analysis

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