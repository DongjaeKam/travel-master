from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserModel
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# 삭제할 것
def index(request):
  context = {
    'datas' : get_user_model().objects.all(),
    'user' : request.user,
  }
  return render(request, 'accounts/index.html', context)

# 로그인 페이지
def login(request):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return render(request, 'accounts/login.html', context)
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃 페이지
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


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