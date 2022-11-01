from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserModel
from django.contrib.auth import login as auth_login

# Create your views here.
# 삭제할 것
def index(request):
  context = {
    'datas' : get_user_model().objects.all(),
    'user' : request.user,
  }
  return render(request, 'accounts/index.html', context)

# 개인 프로필 페이지
def detail(request,pk):
  user = get_user_model().objects.get(pk = pk)
  context = {
    'user': user,
  }
  return render(request,'accounts/detail.html', context)

# 회원가입
def signup(request):

  if request.method == 'POST':
    sign_form = CustomUserModel(request.POST, request.FILES)
    if sign_form.is_valid():
      sign = sign_form.save()
      auth_login(request, user=sign)
      return redirect('accounts:index')
  
  else:
    sign_form = CustomUserModel()

  context = {
    'sign_form' : sign_form,
  }
  
  return render(request, 'accounts/signup.html', context)