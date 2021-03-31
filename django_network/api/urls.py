from django.urls import path
from .views import (
    PostListGetApi,
    PostCreateApi,
    PostGetDeleteUpdateApi,
    UpVoteApi,
    UnVoteApi,
    Analytics,
    Seen,
    SignUp
)


urlpatterns = [
    path("news/", PostListGetApi.as_view(), name="posts"),
    path("news/create/", PostCreateApi.as_view(), name="new_post"),
    path(
        "news/<int:id>/",
        PostGetDeleteUpdateApi.as_view(),
        name="post_detail"),
    path(
        "news/<int:postId>/upvote/",
        UpVoteApi.as_view(),
        name="upvote"
    ),
    path(
        "news/<int:postId>/unvote/",
        UnVoteApi.as_view(),
        name="unvote"
    ),
    path("api/analytics/", Analytics.as_view(), name="analytics"),
    path("register/", SignUp.as_view(), name="sign up"),
    path("seen/", Seen.as_view(), name='seen'),
]
