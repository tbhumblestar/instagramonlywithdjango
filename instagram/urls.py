from django.urls import path,re_path
from . import views

app_name = 'instagram'

urlpatterns = [
  path('',views.index,name='index'),
  path('post/new/',views.post_new,name='post_new'),
  path('post/<int:pk>/',views.post_detail,name='post_detail'),
  path('post/<int:pk>/like',views.post_like,name='post_like'),
  path('post/<int:pk>/unlike',views.post_unlike,name='post_unlike'),
  path('post/<int:post_pk>/comment/new',views.comment_new,name='comment_new'),
  
  re_path(r'^(?P<username>[\w.@+-]+)/$',views.user_page,name='user_page'),
  #정규표현식
  #r:이건 정규표현식이다 // ^ : 정규표현식의 맨 앞 // $정규표현식의 맨끝
  #?P : 바로뒤에오는 애에 정규표현식을 적용해서
  #[\w.@+-]+에 부합한다면(+는 개수가 1개이상을 의미)
  #<username>을 넘기겠다
  #\w : a-zA-Z0-9_
  #.@+- : 이거는 그냥 .@+- 암거나 들어와도 된다는 것임
  #참고 : https://wayhome25.github.io/django/2017/03/18/django-ep2-regx/
  
]