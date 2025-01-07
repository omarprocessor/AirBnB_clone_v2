from sqlalchemy import Column, String, Integer, DateTime, ForeignKey  # Import DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

# In models/reviews.py or equivalent
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    text = Column(String(1024), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)  # Adjust to match user.id type
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
