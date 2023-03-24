from rest_framework.exceptions import NotAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from api.serializers import (
    CommentsSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnlyPermission
from .GenericViewSet import CreateOrList


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            raise NotAuthenticated(
                "Действие доступно только аторизированным пользователям!")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        if self.request.user.is_authenticated:
            serializer.save(post_id=post_id, author=self.request.user)
        else:
            raise NotAuthenticated(
                "Действие доступно только аторизированным пользователям!")


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class FollowViewSet(
    CreateOrList
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission, IsAuthenticated)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ("=user__username", "=following__username")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()
