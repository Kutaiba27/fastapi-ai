from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
   database_url:str
   name:str
   password:int
   model_config = SettingsConfigDict(env_file='config.env')