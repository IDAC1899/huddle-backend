from .base import BaseModel

# import the modules (not the classes) so every model registers with Base
from . import user
from . import event
from . import rsvp

__all__ = ["BaseModel"]