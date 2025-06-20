from django.urls import path

from user.views import CreateUserView, CreateTokenView, LogoutView, UserMeView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", UserMeView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
