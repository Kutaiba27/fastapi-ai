from fastapi import APIRouter, Depends
from ..Dependencies.user import add_user
from typing import Annotated
from ..Dependencies.verfiyHeader import verify_key ,verify_token
from ..database import schemas
router = APIRouter(
    prefix="/users",
)


@router.post('/add-user',response_model= schemas.User)
async def add_new_user(addu: Annotated[schemas.User, Depends(add_user)]):
    return addu
