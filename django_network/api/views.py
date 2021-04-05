from rest_framework.response import Response
from typing import Dict, Any, List
import rest_framework
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models import Post, Vote
from .serializers import PostSerializer, UserSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)


class SignUp(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PostListGetApi(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateApi(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class PostGetDeleteUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"


class UpVoteApi(APIView):
    def post(self, request: rest_framework.request.Request, postId: int) -> rest_framework.response.Response:
        post = Post.objects.filter(id=postId).first()
        if post is None:
            return Response(status=404)
        user = request.user
        vote = Vote.objects.filter(user=user, post=post).first()
        if vote is None:
            vote = Vote(user=user, post=post)
            vote.save()
            print(user.last_activity)
            return Response(status=201)
        return Response("You have liked this post already.")


class UnVoteApi(APIView):
    def post(self, request: rest_framework.request.Request, postId: int) -> rest_framework.response.Response:
        post = Post.objects.filter(id=postId).first()
        if post is None:
            return Response(status=404)
        user = request.user
        vote = Vote.objects.filter(user=user, post=post).first()
        if vote is not None:
            vote.delete()
            return Response(status=201)
        return Response("You haven`t liked this post yet.")


class Analytics(APIView):
    def get(self, request: rest_framework.request.Request) -> rest_framework.response.Response:
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        votes = Vote.objects.filter(upvote_day__lte=date_to, upvote_day__gte=date_from)
        return Response(votes.count())


class Seen(APIView):
    permission_classes: List = [permissions.IsAdminUser]

    def get(self) -> rest_framework.response.Response:
        users_list: List = list(User.objects.all())
        last_seen: List = [user.last_login for user in users_list]
        return Response(last_seen)
