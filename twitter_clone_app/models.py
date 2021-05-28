from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def registration_val(self, post_data):
    errors = {}
    if not EMAIL_REGEX.match(post_data['email']):
      errors['email'] = 'Email is not valid'
    if post_data['password'] != post_data['confirm_password']:
      errors['password'] = 'Your password and Confirm Password do not match'
    print('gets inside registration val function')
    return errors
  def authenticate(self, email, password):
    users = self.filter(email=email)
    if not users:
      return False
    user = users[0]
    return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  objects = UserManager()

  def __str__(self):
    return f"{self.first_name} {self.last_name} {self.email}"

class TweetManager(models.Manager):
  def validate_tweet(self, tweet_text):
    errors = {}
    if len(tweet_text) < 2:
      errors['length'] = 'Tweets must be at least 2 characters'
    if len(tweet_text) > 280:
      errors['length'] = f"Tweets can be a max of 281 characters. This tweet is {len(tweet_text)}"
    return errors

class Tweet(models.Model):
  text = models.CharField(max_length=280)
  user = models.ForeignKey(User, related_name="tweets", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  objects = TweetManager()

class Comment(models.Model):
  text = models.CharField(max_length=280)
  user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
  tweet = models.ForeignKey(Tweet, related_name="comments", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)