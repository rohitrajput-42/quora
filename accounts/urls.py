from django.urls import path
from accounts.views import Login, UserRegisterView, logout

urlpatterns = [
    path('register/', UserRegisterView, name = 'register'),
    path('login/', Login, name = "login"),
    path('logout/', logout, name= "logout")
]