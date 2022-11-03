
from random import randint
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserModel
from .forms import CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText

global code
global password_user

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
  
  if request.user.is_authenticated:
    
    return render(request, 'articles/index.html')

  else:

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
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
    'followers': user.followers.all(), 
    'followings': user.followings.all(),
    'reviews': user.review_set.all(),
  }

  return render(request,'accounts/detail.html', context)

# 회원가입
def signup(request):
  if request.method == 'POST':
    sign_form = CustomUserModel(request.POST, request.FILES)
    if sign_form.is_valid():
      sign = sign_form.save()
      auth_login(request, user=sign)
      return redirect('articles:index')
  else:
    sign_form = CustomUserModel()

  context = {
    'sign_form' : sign_form,
  }
  
  return render(request, 'accounts/signup.html', context)


#프로필 수정
@login_required
def edit_profile(request,pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user == user:

      if request.method == 'POST':
          form = CustomUserChangeForm(request.POST ,instance=request.user)
          if form.is_valid():
              user = form.save()  

              try:
                user.profile_image =request.FILES['image']
                user.save()
              except:
                print('error')


              return redirect('accounts:index')

      else:
          form = CustomUserChangeForm(instance=request.user)
      
      context = {
          'form': form,
      }

      return render(request,'accounts/edit_profile.html',context)
    else:
      return render(request,'articles/index.html')

@login_required
def change_password(request,pk):

    user = get_user_model().objects.get(pk=pk)

    if request.user == user:

      if request.method == 'POST':
          form = PasswordChangeForm(request.user, request.POST)
          if form.is_valid():
              user = form.save()
              update_session_auth_hash(request, user)  # Important!
              messages.success(request, 'Your password was successfully updated!')
              return redirect('accounts:edit_profile', user.pk)
          else:
              messages.error(request, 'Please correct the error below.')
      else:
          form = PasswordChangeForm(request.user)

      context = {
        'form': form,
      }

      return render(request, 'accounts/change_password.html',context)
    else:
      return render(request,'articles/index.html')

# follow
@login_required
def follow(request, pk):
  user = get_user_model().objects.get(pk=pk)

  if request.user != user:
    if request.user not in user.followers.all():
      user.followers.add(request.user)
      is_following = True
    else:
      user.followers.remove(request.user)
      is_following = False

  data = {
    'isFollowing': is_following,
    'followers': user.followers.all().count(),
    'followings': user.followings.all().count(),
  }

  return JsonResponse(data)

@csrf_exempt

def find_password(request,step):

    global code
    global password_user

    if step == 1:

      context = {

        'step': 1,

      }

      return render(request,'accounts/find_password.html',context)
    
    elif step == 2 :

      code = str(10000000 + randint(1,89999999))   
      
      if request.method == 'POST':
        
        email = request.POST['email']
        
        print('email : ' + email )

        password_user = get_user_model().objects.get(email = email)

        # 세션 생성
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # TLS 보안 시작
        s.starttls()
        # 로그인 인증()
        
        s.login('TravelMasterSTMP2022', 'plqkcjzguzvxkqqn')
        # 보낼 메시지 설정
        
       
        code = str(10000000 + randint(1,89999999))

        msg = MIMEText('인증 코드 : '+ code )
        msg['Subject'] = '여행 석사 메일 인증 메시지'
        
        # 메일 보내기
        if request.POST['email']:
          s.sendmail("TravelMasterSTMP2022@gmail.com", request.POST['email'] , msg.as_string())
        
        # 세션 종료
        s.quit()

      context = {

        'step': 2,

      }

      return render(request,'accounts/find_password.html',context)


    elif step == 3  :
      _code= request.POST['code']     

      if _code == code :
        print('됬다. 인증 성공!')
        redirect('accounts:find_password',4)      
      else :
        context = {

        'step': 2,

        }

        return render(request,'accounts/find_password.html',context) 
        

      context = {

        'step': 3,

      }

      return render(request,'accounts/find_password.html',context)


    elif step == 4 :

      if request.POST['password1'] == request.POST['password2']:
        password_user.set_password(request.POST['password1'])
        password_user.save()
        print('비밀번호 변경 가능')
        return redirect('accounts:login')
      else :
        print('비밀번호 변경 불가')

        context = {

        'step': 2,

        }

        return render(request,'accounts/find_password.html',context)

      
