
from sqlalchemy import Boolean, Column, Integer, String, BLOB

from .databaseConnition import Base

class Features(Base):
   __tablename__ = 'features'
   
   id = Column(Integer, primary_key= True, autoincrement="auto", index= True)
   id_image = Column(String, nullable=False)
   keypoints = Column(BLOB, nullable=False)
   
   
class Users(Base):
   __tablename__ = 'users'
   
   id = Column(Integer, primary_key= True, autoincrement="auto", index= True)
   name = Column(String, nullable=False)
   email = Column(String, unique=True, nullable=False)
   password = Column(String, nullable=False)
   is_active = Column(Boolean, nullable=True, default = False)