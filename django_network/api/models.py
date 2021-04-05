from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    pass

class Post(models.Model):
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        to="auth.User",
        related_name="posts",
        on_delete=models.CASCADE,
        null=True
    )

    votes = models.ManyToManyField(
        to="auth.User",
        through="Vote",
        related_name="votes_all"
    )

    @property
    def amount_upvotes(self):
        return self.votes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["creation_date"]


class Vote(models.Model):
    post = models.ForeignKey(
        to=Post,
        related_name="votes_post",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        to="auth.User",
        related_name="votes_user",
        on_delete=models.CASCADE,
        null=True
    )
    upvote_day = models.DateField(auto_now_add=True)
