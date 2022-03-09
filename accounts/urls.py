from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name = 'signup'),
    #참고로 이 로그인의 주소는 accounts/login인데, 이게 settings.LOGIN_URL의 디폴트값임. 그래서 login_required같은 걸 사용했을 떄, accounts/login으로 이동되는 것임
]
