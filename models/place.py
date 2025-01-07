from sqlalchemy import Column, String, ForeignKey, Integer, Text, Float
from sqlalchemy.orm import relationship
from models.base_model import Base

class Place(Base):
    """Represents a place for a user to stay."""

    __tablename__ = 'places'

    id = Column(String(60), primary_key=True)
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)

    # Reference the User class as a string to avoid circular import
    city = relationship('City', back_populates='places')
    user = relationship('User', back_populates='places')
