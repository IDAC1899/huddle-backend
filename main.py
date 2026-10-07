import os
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

# Controllers
from controllers.users import router as UsersRouter
from controllers.events import router as EventsRouter
from controllers.rsvps import router as RsvpsRouter
from controllers.comments import router as CommentsRouter
from controllers.likes import router as LikesRouter

# the sections shown in swagger, in this order
tags_metadata = [
    {"name": "Users", "description": "Sign up, sign in and the signed in user."},
    {"name": "Events", "description": "Browse, host, edit and delete events, plus your own events."},
    {"name": "RSVPs", "description": "Say you're going or maybe, switch between them, or cancel."},
    {"name": "Comments", "description": "Comment on events, with an optional photo."},
    {"name": "Likes", "description": "Like and unlike other people's comments."},
    {"name": "Health", "description": "Check the API is running."},
]

app = FastAPI(
    title="Huddle API",
    description="The API behind Huddle, a local events board for Bahrain. Sign in through **Authorize** with the token from `/api/login` to try the protected routes.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    # start with every section closed so the page is easy to scan
    swagger_ui_parameters={"docExpansion": "none"},
)

# ✅ Allow your React dev server(s) to call the API
origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Which sites can call this API
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # Allow all headers (e.g., Content-Type, Authorization)
)

# each router gets a tag so swagger groups its routes together
app.include_router(UsersRouter, prefix='/api', tags=["Users"])
app.include_router(EventsRouter, prefix='/api', tags=["Events"])
app.include_router(RsvpsRouter, prefix='/api', tags=["RSVPs"])
app.include_router(CommentsRouter, prefix='/api', tags=["Comments"])
app.include_router(LikesRouter, prefix='/api', tags=["Likes"])

@app.get('/health', tags=["Health"])
def health_check():
  return {'message': 'Api is running'}