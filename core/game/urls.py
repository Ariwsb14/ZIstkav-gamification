from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
   # path('letters/',views.LettersView.as_view(), name='letters'),
   # path('letters/<int:pk>/',views.SingleLetterView.as_view(), name='single_letter'),
   # path('journals/<int:pk>/',views.SingleJournalView.as_view(),name='single_journal'),
   path('',views.FileLettersView.as_view(), name='file_letters'),
   path('letter/<int:pk>' , views.FileSingleLetterView.as_view() , name='file_single_letter'),
   path('journls',views.FileJournalsView.as_view(), name='file_journals'),
   path('journal/<int:pk>',views.FileSingleJOurnalView.as_view(), name='file_single_journal')

]