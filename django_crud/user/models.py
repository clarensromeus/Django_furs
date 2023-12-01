from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug


# Create your models here
class Profile(models.Model):
    phonenumber = models.IntegerField(
        unique=True, null=False, validators=[validate_slug])
    proffession = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # return a string representation queryset of the model
    def __str__(self):
        return "%s" % self.proffession
