from chalice import Chalice

from chalicelib.models import Post
from chalicelib.serializers import ImageResultSchema
from chalicelib import connection  # init global connection

app = Chalice(app_name="garbage-today-api")


@app.route("/search")
def search():
    """
    Basic search endpoint 
    """
    posts = Post.search().execute().hits
    schema = ImageResultSchema(many=True)
    results = schema.dump(posts)
    return results.data


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
