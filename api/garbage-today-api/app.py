from chalice import Chalice
from elasticsearch_dsl import Q

from chalicelib.models import Post
from chalicelib.serializers import ImageResultSchema, AutoCompleteSchema

from chalicelib import connection  # init global connection

app = Chalice(app_name="garbage-today-api")


# TODO: always return an array or a real error

@app.route("/search/{term}")
def search(term):
    """
    Basic search endpoint 
    """
    s = Post.search()

    term = term or '*'
    query = Q("multi_match", query=term, fields=['name', 'tags'], zero_terms_query='all')
    s = s.query(query)
    posts = s.execute().hits
    schema = ImageResultSchema(many=True)
    results = schema.dump(posts)
    return results.data


@app.route("/complete/{term}")
def complete(term):
    """
    Autocomplete 
    """
    s = Post.search()
    completion = {'field': 'autosuggest', 'size': 10}
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
