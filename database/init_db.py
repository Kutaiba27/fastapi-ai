from .databaseConnition import engine, Base
from .models import Features, Users
def init_db():
   Base.metadata.create_all(bind=engine)

init_db()