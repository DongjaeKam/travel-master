from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="review_create"),
    path("<int:pk>/delete/", views.delete, name="review_delete"),
    path("<int:pk>/detail/", views.detail, name="review_detail"),
]
