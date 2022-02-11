from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('online/', OnlineView.as_view(), name='online'),
    path('<str:username>/', UserView.as_view(), name='user'),
    path('', MainView.as_view(), name='main'),
]