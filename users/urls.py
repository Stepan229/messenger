from django.urls import path
from .views import *
# , UserDetail, UserList, UserDelete, UserDeleteAll


urlpatterns = [
    path("login1/", login1, name="login"),
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='user-register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
]