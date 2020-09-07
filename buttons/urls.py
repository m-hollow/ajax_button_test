from django.urls import path
#from .views import IndexView, MovieView, CreateButtonBox, UpdateButtonBox
from .views import IndexView, MovieView, mark_seen_view, mark_fav_view, mark_watch_view

# app_name = 'buttons'
# urlpatterns = [
#     path('', IndexView.as_view(), name='index'),
#     path('movie/<int:pk>/', MovieView.as_view(), name='movie'),
#     path('create_box/<int:pk>/<action>/', CreateButtonBox.as_view(), name='create_box'),
#     path('update_box/<int:pk>/<action>/', UpdateButtonBox.as_view(), name='update_box'),
#     ]

app_name = 'buttons'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movie/<int:pk>/', MovieView.as_view(), name='movie'),
    path('ajax/mark_seen/', mark_seen_view, name='mark_seen'),
    path('ajax/mark_fav/', mark_fav_view, name='mark_fav'),
    path('ajax/mark_watch/', mark_watch_view, name='mark_watch'),

]
