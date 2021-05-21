from rest_framework import serializers

from posts.models import Post, User, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')


    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date', )
        model = Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username',)
        model = User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        fields = ('id', 'post', 'author', 'text', 'created',)
        model = Comment
