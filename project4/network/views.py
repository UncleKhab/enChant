import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Tweet, TweetLike, Profile
from .forms import TweetForm


def index(request):
    return render(request, "network/index.html")

def tweet_list_view(request, query):
    """
    API VIEW
    RETURNS A LIST WITH TWEETS
    WHEN CALLING YOU NEED TO SPECIFY THE LIST YOU WANT
    Available lists: all, following
    """
    user=request.user
    if query == "all":
        querySet = Tweet.objects.all()
    if query == "following":
        if not user.is_authenticated:
            return render(request, "network/login.html")
        users_followed = Profile.objects.get(user=request.user).following.all()
        querySet = Tweet.objects.filter(user__in=users_followed)
    paginator = Paginator(querySet, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    tweets_list = [tweet.serialize() for tweet in page_obj]
    if request.user.is_authenticated :
        user = request.user.username
    else:
        user = False

    data = {
        "user" : user,
        "response" : tweets_list
    }
    return JsonResponse(data)

def profile_view(request, query):
    """
    API VIEW
    RETURNS THE USERS PROFILE DATA AND TWEETS
    """
    if not user.is_authenticated:
        return render(request, "network/login.html")
    user = request.user.username
    profile_user = User.objects.get(pk=query)
    profile = Profile.objects.get(user=profile_user)
    
    if user in profile.following.all():
        following = True
    else:
        following = False
    
    if request.user == profile_user:
        sameUser = True
    else:
        sameUser = False
    
    data={
        "user": user,
        "profile": profile.serialize(),
        "following": following,
        "sameUser": sameUser
    }
    return JsonResponse(data)
@csrf_exempt
def tweet_create_view(request):
    """
    API CREATE VIEW 
    """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        return render(request, "network/login.html")
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    content = data['content']
    tweet = Tweet(user=user, content=content)
    if len(content) > 256 :
        return JsonResponse({"error": "The Tweet exceeds the Maximum Length of 256 characters"})
    
    tweet.save()
    return JsonResponse({"message": "Post Created"}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
