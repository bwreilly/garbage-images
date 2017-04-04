from chalice import Chalice

from chalicelib.models import Post
from chalicelib import connection  # init global connection

app = Chalice(app_name="garbage-today-api")


@app.route("/search")
def search():
    """
    Basic search endpoint 
    """
    s = Post.search().execute()
    return s.to_dict()


@app.route("/complete")
def complete():
    """
    Autocomplete 
    """
    return {}  # TODO


@app.route("/")
def home():
    """
    All the endpoints - self documenting 
    """
    return {}  # TODO: can we get app.routes without a circular import?
