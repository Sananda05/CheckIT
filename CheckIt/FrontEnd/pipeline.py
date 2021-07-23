from django.contrib.auth.models import User
from .models import UserProfile

def update_user_social_data(strategy, *args, **kwargs):
  print("Got it!")
  response = kwargs['response']
  backend = kwargs['backend']
  user = kwargs['user']

  if response['picture']:
    url = response['picture']
    userProfile_obj = UserProfile()
    userProfile_obj.user = user
    userProfile_obj.picture = url
    userProfile_obj.save()

def save_picture ( backend, user, response, *args, **kwargs):
    print("Got it!")
    url = response['image'].get('url')
    userProfile_obj = UserProfile()

    if url:
        userProfile_obj.user = user
        userProfile_obj.picture = url
        userProfile_obj.save()