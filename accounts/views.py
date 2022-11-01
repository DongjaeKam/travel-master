from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserModel
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

# 삭제할 것
def index(request):
  context = {
    'datas' : get_user_model().objects.all(),
    'user' : request.user,
  }
  return render(request, 'accounts/index.html', context)

# 로그인 페이지
@csrf_exempt
def login(request):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return render(request, 'accounts/login.html')
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


  #프로필 수정
def edit_profile(request):

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST ,instance=request.user)
        if form.is_valid():
            user = form.save()  
            user.profile_image =request.FILES['profile_image']
            user.save()
            return redirect('accounts:my_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }

    return render(request,'accounts/edit_profile.html',context)
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    context = {
      'form': form,
    }

    return render(request, 'accounts/change_password.html',context)