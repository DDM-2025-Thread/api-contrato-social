from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db):
        self.db = db
        self.user_repository = UserRepository(db)

    def find_one(self, username: str):
        user = self.user_repository.find_by_email(username)
        if not user:
            raise Exception("User not found")
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat()
        }