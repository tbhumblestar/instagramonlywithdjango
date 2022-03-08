from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


#17:30
class SignupForm(UserCreationForm):
  def __init__(self, *args , **kwargs ) -> None:
      super().__init__(*args, **kwargs)
      self.fields['email'].required = True
      self.fields['first_name'].required = True
      self.fields['last_name'].required = True
      
      #usercreationform을 오버라이딩해서 커스터마이징 한 것임


  class Meta(UserCreationForm.Meta):
    model = User
    #usercreationform은 원래 auth안에 있는 user에 의존이 있음. 그러나 우리는 .models에서 들고온 user임!!
    fields = ['username','email','first_name','last_name']

  #유효성 검사
  #clean_filed > 해당 field에 대해서 clean_field함수를 수행 >> 유효성검사에 사용할 수 있음
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if email:
      qs = User.objects.filter(email=email)
      if qs.exists():
        raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
    return email
  
  # #이메일 중복문제
  # def clean_email(self):
  #   email = self.cleaned_data.get('email')
  #   if email:



# #모델폼. 근데 암호에 알고리즘이 적용X
# class SignupForm(forms.ModelForm):
#   class Meta:
#     model=User #모델의 유저라는 모델을 참조
#     fields = ['username','password'] 
#     #폼에 사용할 모델의 필드

# 이렇게 하면 usercreationform이 바로 쓰여짐
# class SignupForm(UserCreationForm):
#   pass