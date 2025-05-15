from rest_framework import serializers

from .models import Article


class ArticlesListSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField(read_only=True)

    def get_text(self, obj) -> str:
        return f'{obj.text[:150]}...'

    class Meta:
        model = Article
        fields = ('id', 'title', 'slug', 'text', 'image', 'created_date', 'updated_date')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('slug',)
