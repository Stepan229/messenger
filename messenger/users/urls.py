from django.urls import path
from .views import *
# , UserDetail, UserList, UserDelete, UserDeleteAll


urlpatterns = [
    path("login/", login1, name="login"),
    path('api/register/', AuthViewSet.as_view({'post': 'register'}), name='user-register'),
    path('api/user/', UserViewSet.as_view({'get': 'get_user'}), name='user-user'),
    path('api/login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
    path('api/logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
    path('api/confirm-email/', ValidateOTP.as_view({'post': 'confirm_email'}), name='user-confirm-email'),

]