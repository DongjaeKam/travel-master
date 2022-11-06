from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="review_create"),
    path("<int:pk>/delete/", views.delete, name="review_delete"),
    path("<int:pk>/detail/", views.detail, name="review_detail"),
    path("<int:pk>/update/", views.update, name="review_update"),
    path("search/", views.search, name="search"),
    path("searchfail/", views.searchfail, name="searchfail"),
    path("<int:pk>/comment_create/", views.comment_create, name="comment_create"),
    path("<int:review_pk>/comment_delete/<int:comment_pk>/delete", views.comment_delete, name="comment_delete"),
    path("<int:review_pk>/comment_update/<int:comment_pk>/update", views.comment_update, name="comment_update"),
    path("<int:pk>/like/", views.like, name='like'),
    path("list/", views.list, name="list"),
    path("maps2/", views.maps2, name="maps2"),
    path("maps/<str:y>/<str:x>/", views.maps, name="maps"),
]