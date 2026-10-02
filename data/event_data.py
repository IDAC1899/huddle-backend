# data/event_data.py
from datetime import datetime
from models.event import EventModel
from models.rsvp import RsvpModel
from models.comment import CommentModel

# events to seed, each hosted by a user
events_list = [
    EventModel(title="Test event 1", description="test 123", area="Isa Town", starts_at=datetime(2026, 10, 9, 19, 0), capacity=10, user_id=1),
    EventModel(title="Test event 2", description="test 123", area="Manama", starts_at=datetime(2026, 10, 10, 18, 0), capacity=6, user_id=2),
    EventModel(title="Test event 3", description="test 123", area="Riffa", starts_at=datetime(2026, 10, 11, 20, 0), capacity=8, user_id=3),
    EventModel(title="Test event 4", description="test 123", area="Muharraq", starts_at=datetime(2026, 10, 12, 17, 0), capacity=4, user_id=1),
]

# rsvps link users to events (user_id + event_id)
rsvps_list = [
    RsvpModel(status="going", user_id=2, event_id=1),
    RsvpModel(status="maybe", user_id=3, event_id=1),
    RsvpModel(status="going", user_id=1, event_id=2),
    RsvpModel(status="going", user_id=2, event_id=4),
    RsvpModel(status="going", user_id=3, event_id=4),
    RsvpModel(status="going", user_id=4, event_id=4),
]

# comments on events
comments_list = [
    CommentModel(content="test 123", user_id=2, event_id=1),
    CommentModel(content="test 123", user_id=1, event_id=2),
    CommentModel(content="test 123", user_id=3, event_id=4),
]