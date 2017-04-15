from __future__ import print_function

import json
from hashlib import sha1
import os
import urllib
import urlparse

import boto3
import settings


s3 = boto3.client('s3')


def get_hash(key_name, bucket_name):
    response = s3.get_object(Bucket=bucket_name, Key=key_name)
    body = response['Body']
    return sha1(body.read()).hexdigest()


def index_file(event, _):

    print("Received event: " + json.dumps(event, indent=2))

    from connection import default
    from models import Post

    key_name = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    # TODO: grab metadata

    print(default)

    name = os.path.splitext(key_name)[0]
    tags = name.split('-')
    domain = settings.AWS_CLOUDFRONT_DOMAIN
    url = urlparse.urljoin('https://' + domain, key_name)
    post = Post(name=name, tags=tags, image_url=url)

    # overwrite identical files
    post.meta.id = get_hash(key_name, bucket_name)
    post.save(using=default)
