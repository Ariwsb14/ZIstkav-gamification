from django.urls import path 
from .views import LoginPageView ,  CreateUserView 

app_name = 'accouonts'
urlpatterns = [
    path('signup/',CreateUserView.as_view(),name='signup'),
    path('login/',LoginPageView.as_view(),name='login')

]