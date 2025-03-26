from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
   path('letters/',views.LettersView.as_view(), name='letters'),
   path('letters/<int:pk>/',views.SingleLetterView.as_view(), name='single_letter'),
]