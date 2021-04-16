from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', index, name="index"),
    path('login/',login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout, name="logout"),
    path('profile/<int:profile_id>', profile, name="profile"),
    path('edit/', edit_profile, name="edit"),
    path('search/', search, name="search"),
]
