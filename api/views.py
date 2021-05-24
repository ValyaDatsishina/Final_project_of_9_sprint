from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView

from api.serializers import PostSerializer, UserSerializer, CommentSerializer
from posts.models import User, Post, Comment


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    posts = Post.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, pk, pk_comment=None):
        post = get_object_or_404(self.posts, id=pk)
        if pk_comment is None:
            comments = post.comments
            serializer = self.serializer_class(comments, many=True)
            return Response(serializer.data)
        else:
            comment = get_object_or_404(self.queryset, post=post, id=pk_comment)
            serializer = self.serializer_class(comment, many=False)
            return Response(serializer.data)

    def create(self, request, pk):
        post = get_object_or_404(self.posts, id=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk, pk_comment):
        post = get_object_or_404(self.posts, id=pk)
        comment = get_object_or_404(self.queryset, post=post, id=pk_comment)
        if request.user == comment.author:
            serializer = self.serializer_class(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, pk_comment):
        post = get_object_or_404(self.posts, id=pk)
        comment = get_object_or_404(self.queryset, post=post, id=pk_comment)
        if request.user == comment.author:
            comment.delete()
            return Response('Коммент удален!')
        return Response(status=status.HTTP_403_FORBIDDEN)
