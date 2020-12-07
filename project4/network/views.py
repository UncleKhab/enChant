from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Tweet, TweetLike, Profile
from .forms import TweetForm


def index(request):
    return render(request, "network/index.html")

def tweet_list_view(request):
    """
    API VIEW
    RETURNS JSON DATA
    """
    queryString = Tweet.objects.all()
    tweets_list = [tweet.serialize() for tweet in queryString]
    if request.user.is_authenticated :
        user = request.user.username
    else:
        user = False

    data = {
        "user" : user,
        "response" : tweets_list
    }
    return JsonResponse(data)

def tweet_create_view(request):
    """
    API CREATE VIEW 
    """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        return render(request, "network/login.html")
    
    form = TweetForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        return JsonResponse(obj.serialize(), status=201) #201 Created Tweet
    if form.errors:
        return JsonResponse(form.errors, status=400) # 400 Error in Creation
    return render(request, 'network/form.html', context={"form": form})

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
