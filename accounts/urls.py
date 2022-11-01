from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
  path('index/', views.index, name='index'),
  path('signup/', views.signup, name='signup'),
  path('<int:pk>/detail/', views.detail, name='detail')
]
