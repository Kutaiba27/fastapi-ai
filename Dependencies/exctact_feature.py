import base64
from io import BytesIO
import io
from PIL import Image
from fastapi import Body, File, HTTPException, UploadFile, Depends
from typing import Annotated
import numpy as np
from pydantic import BaseModel
from sqlalchemy.orm import Session
import cv2
from fastapi.encoders import jsonable_encoder

from ..AI.ai import model
from ..AI.ai_func import  counting, crop_object, get_all_features_from_db, prdict
from ..database.databaseConnition import get_db
from ..AI.sift_algrothim import saveImage

def read_imagefile(file: bytes) -> Image.Image:
   try:
      image = Image.open(BytesIO(file))
      image.verify()  # Verify that it is, in fact, an image
      image = Image.open(BytesIO(file))  # Reopen the image after verification
      return image
   except (IOError, SyntaxError) as e:
      raise ValueError("Invalid image file")


async def inventory_procuct(
   file: Annotated[UploadFile, File(...) ],
   db: Annotated[Session, Depends(get_db)]
   ):
   
   try:
      content = await file.read()
      image = Image.open(BytesIO(content))
      imag_arr = np.array(image)
      result = prdict(model, imag_arr)
      list_of_object = crop_object(result, imag_arr)
      database_features = get_all_features_from_db(db)
      count = counting(list_of_object, database_features)
      return count
   except Exception as e:
      return {"error": str(e)}

   
class ImageUpload(BaseModel):
   images: list[str]
   idProduct: str
async def extract_features(
   image_upload:ImageUpload,
   db: Annotated[Session, Depends(get_db)]
   ):
   print("sssssssssss")
   for image_str in image_upload.images:
      try:
         decode_image = base64.b64decode(image_str)
         image_buffer = BytesIO(decode_image)
         image = Image.open(image_buffer)
         image = image.convert("RGB")
         np_arr = np.array(image)
         recve_image = cv2.cvtColor(np_arr, cv2.COLOR_RGB2GRAY)
         
         if recve_image is None:
            raise ValueError("Could not decode the image")
         saveImage(recve_image, image_upload.idProduct, db)
      except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
      
   print("dddddddddddddddddddddddd")
   
   return {
      "data": True
   }