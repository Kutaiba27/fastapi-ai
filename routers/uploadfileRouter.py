from fastapi import Depends, APIRouter, File
from ..Dependencies.uploadFile import upload_file
from typing import Annotated


router = APIRouter(prefix="/upload-files")


@router.post('/add')
async def upload_file(file: Annotated[dict, Depends(upload_file)]):
    return {"req": file }
