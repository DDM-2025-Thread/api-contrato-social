import os
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.model import User, Roles, UserStatus , ApiCost
from app.core.security import hash_password
from dotenv import load_dotenv

print("--- Iniciando Script de Seeding ---")
loaded = load_dotenv()
if loaded:
    print(".env carregado com sucesso.")
else:
    print("AVISO: Arquivo .env não encontrado ou vazio.")

SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")

if SUPER_ADMIN_PASSWORD is None:
    raise RuntimeError("Environment variable SUPER_ADMIN_PASSWORD is not set")
SUPER_ADMIN_PASSWORD = str(SUPER_ADMIN_PASSWORD)

Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

try:
    admin_user = db.query(User).filter(User.email == SUPER_ADMIN_EMAIL).first()

    if admin_user:
        if admin_user.role != Roles.SUPER_ADMIN:
            admin_user.role = Roles.SUPER_ADMIN
            db.commit()
    else:
        admin_user = User(
            email=SUPER_ADMIN_EMAIL,
            name="Super Admin",
            password_hash=hash_password(SUPER_ADMIN_PASSWORD),
            status=UserStatus.ACTIVE,
            role=Roles.SUPER_ADMIN
        )
        db.add(admin_user)
        db.commit()

    cost_setting = db.query(ApiCost).filter(ApiCost.id == 1).first()
    if not cost_setting:
        print("Configuração de custo padrão (1 centavo) não encontrada. Criando...")
        default_cost = ApiCost(
            id=1,
            cost_per_request=0.01,
            updated_by_id=admin_user.id
        )
        db.add(default_cost)
        db.commit()
finally:
    db.close()