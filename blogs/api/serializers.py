from django.conf import settings
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from blogs.models import Post

POST_ACTION_OPTION = settings.POST_ACTION_OPTION


class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in POST_ACTION_OPTION:
            raise serializers.ValidationError(
                "This is not a valid action for posts")
        return value


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'likes', 'title',
                  'content', 'thumbnail', 'created']

    def get_likes(self, obj):
        return obj.likes.count()

    # def validate_content(self, value):
    #     if len(value) > MAX_POST_LENGTH:
    #         raise serializers.ValidationError("This post is too long")
    #     return value


class PostLikeSerializer(serializers.ModelSerializer):
    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)
