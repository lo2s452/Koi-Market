from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.schemas.user import CurrentUser

router = APIRouter()


@router.get("/me", response_model=CurrentUser)
def me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user
