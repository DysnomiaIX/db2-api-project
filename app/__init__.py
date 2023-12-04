from litestar import Litestar

from app.controlers import AuthorController, BookController, ClientController, LibraryController
from app.database import sqlalchemy_config

app = Litestar([AuthorController, BookController, ClientController, LibraryController], debug=True, plugins=[sqlalchemy_config])
