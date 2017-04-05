from elasticsearch_dsl import DocType, Text, Completion, Keyword, Date, Boolean, datetime, Index


ES_INDEX = 'images'


class Post(DocType):

    class Meta:
        index = ES_INDEX

    title = Text()
    tags = Text(
        multi=True,
        fields={'raw': Keyword(multi=True)}
    )
    autosuggest = Completion()
    created_at = Date()
    image_type = Text()
    image_url = Text()

    published = Boolean()

    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super(DocType, self).save(**kwargs)


index = Index(ES_INDEX)
index.doc_type(Post)
