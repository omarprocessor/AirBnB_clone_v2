from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship(
        "City",
        back_populates="state",
        cascade="all, delete-orphan"
    )


@property
def cities(self):
    """Returns the list of City objects linked to this State"""
    from models import storage
    from models.city import City
    return [city for city in storage.all(City).values() if city.state_id == self.id]
