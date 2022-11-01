from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
  path('index/', views.index, name='index'),
  path('',views.login,name ='login'),
  path('logout/', views.logout, name='logout'),
  path('signup/', views.signup, name='signup'),
  path('<int:pk>/detail/', views.detail, name='detail'),
  path('<int:pk>/edit_profile/', views.edit_profile, name='edit_profile'),
  path('change_password/', views.change_password, name='change_password'),
  path('<int:pk>/follow/', views.follow, name='follow'),
]