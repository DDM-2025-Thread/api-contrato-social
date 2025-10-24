from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserUpdateRequest
from app.models.enum import UserStatus

class UserService:
    def __init__(self, db):
        self.db = db
        self.user_repository = UserRepository(db)

    def find_one(self, username: str):
        user = self.user_repository.find_by_email(username)
        if not user:
            raise Exception("Usuário não encontrado")
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat()
        }
    
    def update(self, username: str, user_update: UserUpdateRequest):
        sent_data = user_update.model_dump(exclude_unset=True)
        update_data = {key: value for key, value in sent_data.items() if value is not None}

        if not update_data or all(value is None for value in update_data.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado válido fornecido para atualização. Pelo menos um campo deve ser preenchido."
            )
        
        user = self.user_repository.find_by_email(username)
        if not user:
            raise Exception("Usuário não encontrado")
        
        self.user_repository.update(user.id, update_data)
        return {
            "message": "Usuário atualizado com sucesso"
        }
    
    def soft_delete(self, username: str):
        user = self.user_repository.find_by_email(username)
        if not user:
            raise Exception("Usuário não encontrado")
        
        self.user_repository.soft_delete(user.id)
        return {
            "message": "Usuário deletado com sucesso"
        }
    
    def hard_delete(self, user_id: int):
        ok = self.user_repository.delete(user_id)
        if not ok:
            raise Exception("Usuário não encontrado")
        
        return {"message": f"Usuário com ID {user_id} foi permanentemente removido."}

    def reactivate(self, user_id: int):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        update_data = {
            "status": UserStatus.ACTIVE,
            "deleted_at": None
        }

        self.user_repository.update(user_id, update_data) 
        
        return {"message": f"Usuário com ID {user_id} foi reativado."}