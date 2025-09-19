from fastapi import FastAPI
from app.database import Base, engine
import app.models.model

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Api rodando"}