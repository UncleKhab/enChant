from django.contrib import admin



# Register your models here.
from .models import Tweet, TweetLike, Profile, User

admin.site.register(Tweet)
admin.site.register(TweetLike)
admin.site.register(Profile)
admin.site.register(User)