from rest_framework.response import Response
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostGetDeleteUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"


class UpVoteApi(APIView):
    def post(self, request, postId):
        post = Post.objects.get(id=postId)
        user = request.user
        vote = Vote.objects.filter(user=user, post=post).all()
        if not vote:
            vote = Vote(user=user, post=post)
            vote.save()
        return Response(status=200)


class UnVoteApi(APIView):
    def post(self, request, postId):
        post = Post.objects.get(id=postId)
        user = request.user
        try:
            vote = Vote.objects.get(user=user, post=post)
            vote.delete()
        except Vote.DoesNotExist as e:
            print('u need to like it before', e)
        return Response(status=200)


class Analytics(APIView):
    def get(self, request, *args, **kwargs):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        votes = Vote.objects.filter(upvote_day__lte=date_to, upvote_day__gte=date_from)
        return Response(votes.count())


class Seen(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, *args):
        users_list = list(User.objects.all())
        last_seen = []
        for user in users_list:
            last_seen.append(user.last_login)
        return Response(last_seen)
