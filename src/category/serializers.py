import datetime

from django.conf import settings
from rest_framework import serializers

from src.category.models import Category, Tag

class CategorySerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    tag = serializers.JSONField(required=False)
    status = serializers.CharField(max_length=10)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Ecoupon` instance, given the validated data.
        """
        tag_data = None
        if 'tag' in validated_data:
            tag_data = validated_data.pop('tag', None)

        category = Category.objects.create(**validated_data)

        if tag_data:
            self.create_tag(category, tag_data)

        return category

    def update(self, instance, validated_data):
        """
        Create and return a new `Ecoupon` instance, given the validated data.
        """

        tag_data = None
        if 'tag' in validated_data:
            tag_data = validated_data.pop('tag', None)

        category = Category.objects.get(pk=instance.id)
        category.name = validated_data.get('name', instance.name)
        category.status = validated_data.get('status', instance.name)
        category.save()

        if tag_data:
            self.delete_tag(instance)
            self.create_tag(category, tag_data)

        return category

    def create_tag(self, category, data):
        for i in data:
            data = {
                'name': i,
                'news_id': category.id
            }

            Tag.objects.create(**data)

    def delete_tag(self, instance):
        Tag.objects.filter(news_id=instance.id).delete()


class CategoryListSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=10)
    tags = serializers.StringRelatedField(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)