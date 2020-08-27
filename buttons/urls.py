from django.urls import path
from .views import IndexView, MovieView, CreateButtonBox, UpdateButtonBox

app_name = 'buttons'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movie/<int:pk>/', MovieView.as_view(), name='movie'),
    path('create_box/<int:pk>/<action>/', CreateButtonBox.as_view(), name='create_box'),
    path('update_box/<int:pk>/<action>/', UpdateButtonBox.as_view(), name='update_box'),
    ]
