from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from rest_framework import routers

urlpatterns = []

v1_router = routers.DefaultRouter()
v1_router.register(r"follow", FollowViewSet, basename="follow")
v1_router.register(r"posts", PostViewSet, basename="post")
v1_router.register(r"groups", GroupViewSet, basename="group")
v1_router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment"
)
v1_router.register(
    r"posts/(?P<post_id>\d+)/comments/(?P<comment_id>\d+)",
    CommentViewSet,
    basename="comment",
)
