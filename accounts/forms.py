from cProfile import label
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserModel(UserCreationForm):
  class Meta:
    model = get_user_model()
    fields = [
      'username',
      'profile_name',
      'password1',
      'password2',
      'email',
      'first_name',
      'last_name',
      'profile_image',
    ]

    labels = {
      'username' : '로그인 아이디',
      'profile_name' : '닉네임',
      'password1' : '비밀번호',
      'password2' : '비밀번호 확인',
      'email' : '이메일 ',
      'first_name' : '이름',
      'last_name' : '성',
      'profile_image' : '프로필 이미지',
    }