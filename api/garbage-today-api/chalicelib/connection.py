from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import RequestsHttpConnection, Elasticsearch
# from elasticsearch_dsl.connections import connections

from settings import *

auth = AWSRequestsAuth(aws_access_key=AWS_ACCESS_KEY,
                       aws_secret_access_key=AWS_SECRET_KEY,
                       aws_token=AWS_SESSION_TOKEN,
                       aws_host=ES_HOST,
                       aws_region='us-west-1',
                       aws_service='es')

default = Elasticsearch(hosts=[{'host': ES_HOST, 'port': 443}],
                        use_ssl=True,
                        verify_certs=True,
                        connection_class=RequestsHttpConnection,
                        http_auth=auth, timeout=20)
