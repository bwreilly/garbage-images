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

    key_name = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    post = index(key_name, bucket_name)

    return "Indexed post: " + json.dumps(post.to_dict(), indent=2)


def index(key, bucket):
    from connection import default
    from models import Post

    name, ext = os.path.splitext(key)
    tags = name.split('-')
    domain = settings.AWS_CLOUDFRONT_DOMAIN
    url = urlparse.urljoin('https://' + domain, key)
    post = Post(name=name, tags=tags, image_url=url, image_type=ext)

    # TODO: grab metadata

    # overwrite identical files
    post.meta.id = get_hash(key, bucket)

    # TODO: this is gonna replace the image data rather than merge it, which is probably closer to what I want
    post.save(using=default)
    return post
