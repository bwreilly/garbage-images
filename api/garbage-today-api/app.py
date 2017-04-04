import os

from chalice import Chalice
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import Search
from aws_requests_auth.aws_auth import AWSRequestsAuth

app = Chalice(app_name="garbage-today-api")


ES_HOST = os.environ.get('ES_HOST')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')


def search_client():
    auth = AWSRequestsAuth(aws_access_key=AWS_ACCESS_KEY,
                           aws_secret_access_key=AWS_SECRET_KEY,
                           aws_token=AWS_SESSION_TOKEN,
                           aws_host=ES_HOST,
                           aws_region='us-west-1',
                           aws_service='es')

    return Elasticsearch(
        hosts=[{'host': ES_HOST, 'port': 443}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        http_auth=auth
    )


@app.route("/search")
def search():
    """
    Basic search endpoint 
    """
    client = search_client()
    return Search(using=client).execute().to_dict()


@app.route("/complete")
def complete():
    """
    Autocomplete 
    """
    return {}  # TODO


@app.route("/")
def index():
    """
    All the endpoints - self documenting 
    """
    return {}  # TODO: can we get app.routes without a circular import?
