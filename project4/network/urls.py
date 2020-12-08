
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("list/<str:query>", views.tweet_list_view, name="list_view"),
    path("profile/<int:query>", views.profile_view, name="profile_view"),
    path("create/", views.tweet_create_view, name="create_view")
]
