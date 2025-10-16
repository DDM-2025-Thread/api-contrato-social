import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models.model import *
from app.routers import auth, users, apikeys, usage, billing

app = FastAPI(title="API Contratos Sociais")

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

origins_config = {
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": [
        "Authorization", 
        "Content-Type",
        "Accept",
        "Origin",
        "User-Agent",
        "X-Requested-With"
    ],
}

if ENVIRONMENT == "development":
    origins_config["allow_origins_regex"] = r"http://localhost:\d+"
else:
    origins_config["allow_origins"] = [
        "https://seusite.com.br",
        "https://app.seusite.com.br",
    ]
app.add_middleware(CORSMiddleware, **origins_config)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(apikeys.router)
app.include_router(usage.router)
app.include_router(billing.router)

@app.get("/")
def root():
    return {"message": "API rodando 🚀"}