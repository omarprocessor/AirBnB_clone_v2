from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
