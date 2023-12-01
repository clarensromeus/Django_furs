from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("update/<int:blog_id>/", views.update_post, name="update"),
    path('delete', views.delete_post, name="delete"),
    path('post/<int:blog_id>', views.get_one_post, name="one_post"),
]
