from django.db import models
from django.conf import settings

class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    places = [
    ("서울", "서울"),
    ("경기도", "경기도"),
    ("강원도", "강원도"),
    ("충청도", "충청도"),
    ("경상도", "경상도"),
    ("전라도", "전라도"),
    ]
    place = models.CharField(max_length=20, choices = places)
    themes = [
        ("Food", "Food"),
        ("Healing", "Healing"),
        ("activity", "activity"),
    ]
    theme = models.CharField(max_length=20, choices = themes)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_review')
    
    def __str__(self):
        return self.title
class Photo(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)

class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Search(models.Model):
    title = models.CharField(max_length=10)
    count = models.PositiveIntegerField(default=0)