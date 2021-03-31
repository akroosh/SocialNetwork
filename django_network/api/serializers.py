from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Vote


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password: str = serializers.CharField(write_only=True)

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ("id", "username", "password")


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["author", "title", "creation_date", "amount_upvotes"]


class VoteSerializer(serializers.ModelSerializer):

    post = PostSerializer
    post = serializers.ReadOnlyField(source="post.title")
    user = UserSerializer
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Vote
        fields = "__all__"
