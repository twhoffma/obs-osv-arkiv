from haystack import indexes

import archive.models

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    published = indexes.BooleanField(model_attr='published')
    title = indexes.CharField(model_attr='title')
    era_from = indexes.CharField(model_attr='era_from', null=True)
    date_from = indexes.IntegerField(model_attr='date_from', null=True)
    era_to = indexes.CharField(model_attr='era_to', null=True)
    date_to = indexes.IntegerField(model_attr='date_to', null=True)
    origin_city = indexes.CharField(model_attr='origin_city', null=True)
    origin_country = indexes.CharField(model_attr='origin_country', null=True)
    artist = indexes.CharField(model_attr='artist', null=True)
    materials = indexes.MultiValueField(null=True)
    video_only = indexes.BooleanField()

    def prepare_materials(self, obj):
        return [x.name for x in obj.materials.all()]

    def prepare_video_only(self, obj):
        return obj.media.filter(media_type=archive.models.Media.MEDIA_TYPE_MOVIE).count() > 0

    def get_model(self):
        return archive.models.Item

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

