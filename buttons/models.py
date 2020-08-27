from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class UserProxy(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=150)

    users = models.ManyToManyField(User, through='ButtonBox')

    def __str__(self):
        return self.name


class ButtonBox(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    seen = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    watch = models.BooleanField(default=False)

    def __str__(self):
        text = 'Current status - Seen: {} Fav: {} Watchlist: {}'.format(self.seen, self.favorite, self.watch)
        return text


