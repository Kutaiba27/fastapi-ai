from fastapi import Depends, APIRouter
from ..Dependencies.exctact_feature import extract_features, upload_file
from typing import Annotated


router = APIRouter(prefix="/upload-files")


@router.post('/add')
async def upload_file(file: Annotated[dict, Depends(upload_file)]):
    
    return {"req": file }

@router.post('/product-box-images')
async def product_box_images(file: Annotated[dict, Depends(extract_features)]):
    return {"req": file }
    