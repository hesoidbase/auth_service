from fastapi import APIRouter
from app.models import users_model as UserModels

router = APIRouter()
RegisterUser = UserModels.RegisterUser

@router.post("/auth/register")
async def register_user(register_user_data: RegisterUser):
    print(register_user_data.email)


