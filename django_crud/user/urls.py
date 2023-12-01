
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout_user", views.logOut, name="logout_user"),
    path("profile", views.profile, name="profile"),
    path("register", views.register, name="register"),
    path("createprofile", views.create_profile, name="createprofile"),
    path("updateprofile", views.update_profile, name="updateprofile"),
    path("change_pasword", views.change_password, name="change_password"),
    path("users_searching/<username>",
         views.users_by_username, name="users_searching"),
    path("searching", views.search_user, name="searching"),
    path("allusers", views.all_users, name="allusers"),
]
