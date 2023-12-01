from django.db import models
from django.contrib.auth.models import User


# Create your models here
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # return a string representation queryset of the model
    def __str__(self):
        return "%s" % self.title
