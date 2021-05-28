from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

def index(request):
  return render(request, 'index.html')

def register(request):
  if request.method == "POST":
    errors = User.objects.registration_val(request.POST)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect("/")
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
  return redirect('/')

def login(request):
  if request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']
    if not User.objects.authenticate(email, password):
      messages.error(request, 'Email and Password do not match')
      return redirect("/")
    user = User.objects.get(email=email)
    request.session['user_id'] = user.id
    return redirect("/tweet")
  return redirect('/')

def logout(request):
  del request.session['user_id']
  return redirect('/')

def tweet(request):
  if 'user_id' not in request.session:
    print('GETS HERE: USER NOT LOGGED IN')
    return HttpResponse("<h1>You must be logged in to get to the tweet page</h1>")
  user = User.objects.get(id=request.session['user_id'])
  context = {
    "user": user
  }
  return render(request, 'tweet.html', context)

def add_tweet(request):
  tweet_text = request.POST['tweet_text']
  errors = Tweet.objects.validate_tweet(tweet_text)
  if len(errors) > 0:
    for key, val in errors.items():
      messages.error(request, val)
    return redirect('/tweet')
  user = User.objects.get(id=request.session['user_id'])
  Tweet.objects.create(text=tweet_text, user=user)
  return redirect('/feed')

def feed(request):
  all_tweets = Tweet.objects.all()
  context = {
    "all_tweets": all_tweets
  }
  return render(request, 'feed.html', context)

def edit_tweet(request, tweet_id):
  tweet_to_edit = Tweet.objects.get(id=tweet_id)
  context = {
    "tweet": tweet_to_edit
  }
  return render(request, 'edit-tweet.html', context)

def modify_tweet(request):
  if request.method == "POST":
    tweet_id = request.POST['tweet_id']
    new_text = request.POST['tweet_text']
    errors = Tweet.objects.validate_tweet(new_text)
    if len(errors) > 0:
      for key, val in errors.items():
        messages.error(request, val)
      return redirect('/tweet')
    tweet_to_edit = Tweet.objects.get(id=tweet_id) 
    tweet_to_edit.text = new_text
    tweet_to_edit.save()
    return redirect('/feed')

def add_comment(request):
  comment_text = request.POST['comment_text']
  tweet_id = request.POST['tweet_id']
  user = User.objects.get(id=request.session['user_id'])
  tweet = Tweet.objects.get(id=tweet_id)
  Comment.objects.create(text=comment_text, user=user, tweet=tweet)
  return redirect('/feed')