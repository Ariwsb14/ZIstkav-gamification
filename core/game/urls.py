from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
   path('',views.LettersView.as_view(), name='letters'),
]