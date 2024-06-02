from enum import Enum
from typing import Annotated
from fastapi import File, Query, APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()


class ModelName(str, Enum):
    alexnet = "alexnet"
    esnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

    @router.get("/api/{model_name}")
    def get_all(model_name: ModelName):
        if model_name is ModelName.alexnet:
            print("print ", model_name)
            return {"message": "true"}
        return {"messages": model_name}


@router.get("/query")
def query(query1: Annotated[str | None, Query(max_length=3)] = None):
    return {query1: query1}


@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}



