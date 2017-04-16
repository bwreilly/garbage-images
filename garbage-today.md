# Creating an image app with ElasticSearch, S3, Lambda, React

## What, why?

1. I have all these images on all these computers
2. Constantly trying to find a good one for my purposes
3. Existing solutions suck for search, sorry
	- imgur fails to find my image for `arcade river game` and gives me garbage for `old computer`
	- giffy only does gifs and it's search is much worse and it's slow as fuck
	- I'm better at curating this than most of the internet apparently
4. What this is replacing (image of me using alfred)
5. Because I can

## New tools for lazy application developers 
	
Back before we had these platform services, speedily building this app would look like this.

- Grab a familiar framework like Django
- Build out a bunch of API views (likely with DRF)
- A DB for auth maybe since not everyone should get to upload
- But most of the writing is gonna be via ES so do that somehow
- Hook up some storage solution so images go in the right place, can be retrieved
- Include something (`redis-queue`, `celery`) to do async indexing
- Build out a frontend, host that somewhere
- Host the backend somewhere, Heroku to get all these services up and running fast
	- Elasticsearch
	- Redis/RabbitMQ
	- Django/WSGI
	- Postgresql
- Pay money 24/7 for a server that is barely in use 

This is how I made [garbage.today](https://garbage.today)

- Defined a couple of API endpoints with Chalice
- Made a really basic indexer function in Lambda
- Made an S3 bucket that fires events to that indexer
- Hooked up an ElasticSearch service
- Wrote the worlds simplest/dumbest SPA with `create-react-app`

### The bad

The user experience AWS IAM - which is what you need to deal with if you are using their services - is not good. If it was designed by humans, I get the impression that they envisioned their users as having wronged them personally in some way.

This could be a post in itself, but let's review the seemingly dozens of ways you can cobble together a `role` with `permissions` in this world.

- Sorta construct one in Lambda when you create the thing
- Generate one automatically when you create a lambda function and hack it
- Modify the ACL on the resource itself (ES, S3)
- Write your own in any of these places (enjoy these enormous docs-as-prose)
- Their "builder"

The fact they need a simulator is a good indication that they've failed to capture user intention in the various places used to configure access rights.



## TODO:

- A better build system - update the whole project as needed
- A CI that hooks into the repo and automatically tests and deploys
- Dev/QA/Prod
- Somehow use python 3.5+