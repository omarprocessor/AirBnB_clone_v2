from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Create an engine and session for the database."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB')

        # Create engine and bind it to session
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if os.getenv('HBNB_ENV') == 'test':
            self.__drop_all()

        self.reload()

    def __drop_all(self):
        """Helper method to drop all tables during testing."""
        from models import Base  # Import here to avoid circular import
        Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects or filtered by class."""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            from models import Base  # Import here to avoid circular import
            objs = self.__session.query(Base).all()

        result = {}
        for obj in objs:
            result[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return result

    def new(self, obj):
        """Add new object to the session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes in the session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session."""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Create all tables in the database and initialize session."""
        from models import Base  # Import here to avoid circular import
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
