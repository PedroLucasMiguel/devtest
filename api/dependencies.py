from db import config

# Database dependencie
# This function yields a single db connection that closes after being used
def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()
