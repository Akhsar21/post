from django.conf import settings
from rest_framework import serializers
from .models import Post

POST_ACTION_OPTION = settings.POST_ACTION_OPTION

class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in POST_ACTION_OPTION:
            raise serializers.ValidationError("This is not a valid action for posts")
        return value

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    # def validate_content(self, value):
    #     if len(value) > MAX_POST_LENGTH:
    #         raise serializers.ValidationError("This post is too long")
    #     return value
