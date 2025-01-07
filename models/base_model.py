from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()  # Create the base class for SQLAlchemy


class BaseModel:
    id = Column(
        String(60),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes from kwargs."""
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def save(self):
        """Add the object to the session and commit changes."""
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert the object to a dictionary."""
        obj_dict = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

        if '_sa_instance_state' in obj_dict:
            del obj_dict['_sa_instance_state']
        return obj_dict

    def delete(self):
        """Delete the object from storage."""
        from models import storage
        storage.delete(self)
