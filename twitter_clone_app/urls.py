from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('tweet', views.tweet),
    path('add-tweet', views.add_tweet),
    path('feed', views.feed),
    path('edit/<int:tweet_id>', views.edit_tweet),
    path('modify-tweet', views.modify_tweet),
    path('add-comment', views.add_comment)
]