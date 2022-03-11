from django.contrib import messages
from django.shortcuts import redirect,render
from .forms import SignupForm,ProfileForm,PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.views import (
  LoginView,LogoutView,logout_then_login,PasswordChangeView as AuthPasswordChangeView)

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required


#URLS : URL 접근(메소드상관없이) > 해당 URL에 대한 view호출
#views : url에 맞게 호출된 view가 사용. 
#>메소드를 판단,db접근,

def logout(request):
  messages.success(request,'로그아웃 되었습니다')
  return logout_then_login(request)
  #로그아웃하면 바로 리턴페이지로 보내버리겠다!

#get으로 요청이 왔다 > 빈폼을 담은 html파일 랜더링 > 빈폼입력 후 제출 > 그러면 동일한 url로 post요청 > post로 요청이 왔다 > form객체에 해당 요청의 post메서드값을 담음 >  그 form에 유효성 검사를 진행
#>form이 성공하면 내용을 db에 담음(form.save(),즉, post의 요청처리가 된 것임) > 환영합니다 메세지와 함께 리다이렉트 
def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    #signupform의 인스턴스 생성
    if form.is_valid(): 
      signed_user = form.save()

      auth_login(request,signed_user)
      #signed_user를 바로 로그인처리

      signed_user.send_welcome_email()
      messages.success(request,"회원가입을 환영합니다")
      
      next_url=request.GET.get('next','/')
      #Get메소드로 들어왔을 때, next라는 인자가 있으면 그걸 가져오고, 없으면 그냥 /를 가져온나

      return redirect(next_url)
    
  else:
    form = SignupForm()

  return render(request,'accounts/signup_form.html',{'form':form})

login = LoginView.as_view(template_name='accounts/login_form.html')

@login_required
def profile_edit(request):
  if request.method == "POST":
    form = ProfileForm(request.POST,request.FILES,instance=request.user)
    #request.Post,request.Files라고 되어 있어야 post메서드와 files를 받을 수 있음
     
    #인스턴스 설정부분 질문
    if form.is_valid():
      form.save()
      messages.success(request,"프로필을 수정/저장했습니다")
      return redirect('profile_edit')
  else:
    form = ProfileForm(instance=request.user)

  return render(request,"accounts/profile_edit_form.html",{"form":form})



class PasswordChangeView(LoginRequiredMixin,AuthPasswordChangeView):
  success_url = reverse_lazy("password_change")
  template_name = 'accounts/password_change_form.html'
  form_class = PasswordChangeForm

  def form_valid(self, form):
    messages.success(self.request,"암호를 변경했습니다.")
    return super().form_valid(form)

password_change = PasswordChangeView.as_view()