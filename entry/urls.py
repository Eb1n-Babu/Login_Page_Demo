from django.urls import path
from .views import Home, SignUp, Login

urlpatterns = [
    path('',Home,name='home'),
    path('SignUp/',SignUp,name='signup'),
    path('Login/',Login,name='login'),
]


