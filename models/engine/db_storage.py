import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    def __init__(self):
        """Create engine and session for database interaction."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        # Connection string for MySQL
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', pool_pre_ping=True)
        self.__session = None

    def all(self):
        """Query all objects from the database."""
        objs = []
        objs.extend(self.__session.query(Review).all())
        return objs

    def new(self, obj):
        """Add the object to the session."""
        self.__session.add(obj)

    def save(self):
        """Commit changes to the session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the session."""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Reload the session."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine))
        self.__session = Session()

    def close(self):
        """Close the current SQLAlchemy session."""
        self.__session.close()
