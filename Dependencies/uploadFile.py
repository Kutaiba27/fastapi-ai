import base64
from fastapi import File, Form, UploadFile
from typing import Annotated
from PIL import Image

async def upload_file(file: Annotated[list[UploadFile], File() ], title: Annotated[str,Form()] ):
   # file_bytes = await Image.open(file)

   # encoded_file = base64.b64encode(file_bytes)

   return {
      "file": file[1].filename,
      "title": title
   }