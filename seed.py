# seed.py

from sqlalchemy.orm import sessionmaker
from data.user_data import user_list
from data.event_data import events_list, rsvps_list, comments_list, likes_list
from config.environment import DATABASE_URL
from sqlalchemy import create_engine
from models.base import Base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# This seed file is a separate program that can be used to "seed" our database with some initial data.
try:
    print("Recreating database...")
    # Dropping (or deleting) the tables and creating them again is for convenience. Once we start to play around with
    # our data, changing our models, this seed program will allow us to rapidly throw out the old data and replace it.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("seeding the database...")
    db = SessionLocal()

    # users first, everything else belongs to a user
    db.add_all(user_list)
    db.commit()

    # events next, rsvps and comments belong to an event
    db.add_all(events_list)
    db.commit()

    db.add_all(rsvps_list)
    db.commit()

    db.add_all(comments_list)
    db.commit()

    # likes last, they belong to a comment
    db.add_all(likes_list)
    db.commit()

    db.close()

    print("Database seeding complete! 👋")
except Exception as e:
    print("An error occurred:", e)