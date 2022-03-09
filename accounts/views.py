from django.contrib import messages
from django.shortcuts import redirect,render
from .forms import SignupForm
from django.contrib.auth.views import LoginView

#URLS : URL 접근(메소드상관없이) > 해당 URL에 대한 view호출
#views : url에 맞게 호출된 view가 사용. 
#>메소드를 판단,db접근,



#get으로 요청이 왔다 > 빈폼을 담은 html파일 랜더링 > 빈폼입력 후 제출 > 그러면 동일한 url로 post요청 > post로 요청이 왔다 > form객체에 해당 요청의 post메서드값을 담음 >  그 form에 유효성 검사를 진행
#>form이 성공하면 내용을 db에 담음(form.save(),즉, post의 요청처리가 된 것임) > 환영합니다 메세지와 함께 리다이렉트 
def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    #signupform의 인스턴스 생성
    if form.is_valid(): 
      signed_user = form.save()
      signed_user.send_welcome_email()
      messages.success(request,"회원가입을 환영합니다")
      
      next_url=request.GET.get('next','/')
      #Get메소드로 들어왔을 때, next라는 인자가 있으면 그걸 가져오고, 없으면 그냥 /를 가져온나

      return redirect(next_url)
    
  else:
    form = SignupForm()

  return render(request,'accounts/signup_form.html',{'form':form})

  