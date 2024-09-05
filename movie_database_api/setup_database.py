from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///movie_database.db"  # Use your preferred database URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()

Base.metadata.create_all(engine)

print("Database setup complete.")
