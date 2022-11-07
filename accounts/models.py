from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    profile_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="image/profile_image", null=False)
    rank = models.IntegerField(default=0)
# class User_rank(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    