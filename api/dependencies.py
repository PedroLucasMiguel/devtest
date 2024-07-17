from db import config

# Database dependencie
def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()
