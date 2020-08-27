from django.contrib import admin

from .models import Movie, UserProxy, ButtonBox

admin.site.register(Movie)
admin.site.register(UserProxy)
admin.site.register(ButtonBox)
