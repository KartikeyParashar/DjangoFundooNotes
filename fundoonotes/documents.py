from django_elasticsearch_dsl import Index, Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from .models import Note

html_strip = analyzer(
    'html_strip',
    tokenizer='standard',
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
class NotesDocument(Document):
    title = fields.TextField(analyzer=html_strip)
    label = fields.ObjectField(properties={'name': fields.TextField()})

    class Index:
        name = 'index'  # Name of the Elastic Search index
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Note  # The model associated with this Document

        # The fields of the model you want to be indexed in Elastic Search
        fields = [
            'note',
            'reminder',
            'is_archive',
            'is_trashed',
        ]
