from django.urls import path
from .views import home, update_post, Logout, login, register, delete_post, get_one_post, change_password


app_name = "blog"

urlpatterns = [
    path("", home.as_view(), name="home"),
    path("update/<int:pk>", update_post.as_view(), name="update"),
    path("delete/<int:pk>", delete_post.as_view(), name="delete"),
    path("one_post/<str:title>", get_one_post.as_view(), name="one_post"),
    path("login", login.as_view(), name="login"),
    path("register", register.as_view(), name="register"),
    path("change_password", change_password.as_view(), name="change_password"),
    path("logout", Logout.as_view(), name="logout")
]
