from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through="TweetLike")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "likes" : self.likes.count(),
            "timestamp": self.timestamp
        }

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    description = models.TextField(max_length=256, blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "followers": self.followers,
            "following": self.following,
            "description" : self.description
        }