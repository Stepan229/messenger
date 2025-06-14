from django.urls import path
from .views import *
# , UserDetail, UserList, UserDelete, UserDeleteAll


urlpatterns = [
    path("login/", login1, name="login"),
    path('api/register/', AuthViewSet.as_view({'post': 'register'}), name='user-register'),
    path('api/login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
    path('api/logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
]