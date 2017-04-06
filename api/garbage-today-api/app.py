from chalice import Chalice

from chalicelib.models import Post
from chalicelib.serializers import ImageResultSchema, AutoCompleteSchema

from chalicelib import connection  # init global connection

app = Chalice(app_name="garbage-today-api")


@app.route("/search/{term}")
def search(term):
    """
    Basic search endpoint 
    """
    # TODO: actually use that term, why not?
    posts = Post.search().execute().hits
    schema = ImageResultSchema(many=True)
    results = schema.dump(posts)
    return results.data


@app.route("/complete/{term}")
def complete(term):
    """
    Autocomplete 
    """
    # get suggestions
    s = Post.search()
    completion = {'field': 'autosuggest'}
    response = s.suggest('suggest', term, completion=completion).execute_suggest()
    result = response.suggest[0]
    suggestions = result.options

    # transform/serialize
    schema = AutoCompleteSchema(many=True)
    results = schema.dump(suggestions)
    return results.data


@app.route("/")
def home():
    """
    All the endpoints - self documenting 
    """
    # TODO: can we get app.routes without a circular import?
    return {
        '/': 'This page (index)',
        'search/{term}': 'Posts',
        'complete/{term}': 'Autocomplete'
    }
