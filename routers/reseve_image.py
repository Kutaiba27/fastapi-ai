from fastapi import Depends, APIRouter
from ..Dependencies.exctact_feature import extract_features, inventory_procuct
from typing import Annotated


router = APIRouter(prefix="/upload-files")


@router.post('/inventory-product')
async def upload_file(file: Annotated[dict, Depends(inventory_procuct)]):
    
    return {"req": file }

@router.post('/product-box-images')
async def product_box_images(file: Annotated[bool, Depends(extract_features)]):
    return {"result": file }
    