# data/event_data.py
from datetime import datetime
from models.event import EventModel
from models.rsvp import RsvpModel
from models.comment import CommentModel
from models.like import LikeModel

# events to seed, each hosted by a user
events_list = [
    EventModel(title="Friday Night Padel", description="Casual doubles at the courts near Isa Town Mall. All levels welcome, we swap partners every game. Rackets available to borrow, just bring water.", area="Isa Town", starts_at=datetime(2026, 10, 9, 19, 0), capacity=10, user_id=1),
    EventModel(title="Bab Al Bahrain Photo Walk", description="Golden hour walk through Manama Souq with our cameras (phones count). We finish with karak by the gate.", area="Manama", starts_at=datetime(2026, 10, 10, 17, 0), capacity=6, user_id=2),
    EventModel(title="Board Game Night", description="Catan, Codenames and whatever you bring. Snacks are on me, we play until people get tired.", area="Riffa", starts_at=datetime(2026, 10, 11, 20, 0), capacity=8, user_id=3),
    EventModel(title="Pearling Path Walk", description="A slow walk along the Pearling Path, stopping at the old pearl merchants' houses on the way. Small group so everyone can hear the stories.", area="Muharraq", starts_at=datetime(2026, 10, 12, 16, 30), capacity=4, user_id=1),
    EventModel(title="Sunrise Run at Amwaj", description="An easy 5K along the lagoon before it gets hot. Nobody gets left behind, coffee after.", area="Amwaj", starts_at=datetime(2026, 10, 14, 5, 45), capacity=12, user_id=4),
    EventModel(title="Late Night Five-a-Side", description="Indoor pitch in Seef, we split teams on the night. Bring a white and a dark shirt.", area="Seef", starts_at=datetime(2026, 10, 16, 21, 30), capacity=10, user_id=5),
]

# rsvps link users to events (user_id + event_id)
rsvps_list = [
    RsvpModel(status="going", user_id=2, event_id=1),
    RsvpModel(status="maybe", user_id=3, event_id=1),
    RsvpModel(status="going", user_id=1, event_id=2),
    RsvpModel(status="going", user_id=2, event_id=4),
    RsvpModel(status="going", user_id=3, event_id=4),
    RsvpModel(status="going", user_id=4, event_id=4),
    RsvpModel(status="maybe", user_id=1, event_id=3),
    RsvpModel(status="going", user_id=5, event_id=5),
    RsvpModel(status="going", user_id=2, event_id=6),
    RsvpModel(status="going", user_id=3, event_id=6),
]

# comments on events
comments_list = [
    CommentModel(content="Can I bring a friend who's never played before?", user_id=2, event_id=1),
    CommentModel(content="Bringing my camera, see you at the gate!", user_id=1, event_id=2),
    CommentModel(content="Is there parking near the start?", user_id=3, event_id=4),
    CommentModel(content="Of course, beginners are welcome.", user_id=1, event_id=1),
    CommentModel(content="Where do we meet exactly?", user_id=2, event_id=5),
]

# likes link users to comments (user_id + comment_id)
likes_list = [
    LikeModel(user_id=1, comment_id=1),
    LikeModel(user_id=3, comment_id=1),
    LikeModel(user_id=2, comment_id=4),
]