
from fastapi import FastAPI
from .AI.ai import load_model
from .configurations.env_config import Settings
from .routers import reseve_image, user_router
from functools import lru_cache

app = FastAPI()

@lru_cache
def get_env()-> Settings:
    return Settings()

info: Settings = get_env()


# # class ImageUpload(BaseModel):
#     front: str
#     back: str

# @app.post('/upload')
# def upload_file(images: ImageUpload):
    # front_image_data = io.BytesIO(base64.b64decode(images.front))
#     back_image_data = io.BytesIO(base64.b64decode(images.back))
#     front_path = f"files/front1_.jpg"
#     back_path = f"files/back1_.jpg"
#     front_image = Image.open(front_image_data)
#     back_image = Image.open(back_image_data)
    
#     # front_image.save(front_path)
#     # back_image.save(back_path)
#     return {
#         "file": "hello"
#     }


app.include_router(user_router.router)
app.include_router(reseve_image.router)
