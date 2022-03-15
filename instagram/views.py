from xml.etree.ElementTree import Comment
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CommentForm
from django.contrib import messages
from .models import Tag, Post
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta



@login_required
def comment_new(request,post_pk):

  post = get_object_or_404(Post,pk=post_pk)

  if request.method =="POST":
    form = CommentForm(request.POST,request.FILES)
    if form.is_valid():
      comment = form.save(commit = False)
      comment.post = post
      comment.author = request.user
      comment.save()
      if request.is_ajax():
        return render(request,"instagram/_comment.html",{
          "comment":comment,
        })
      return redirect(comment.post)
      #comment.post > 코멘트의 post 객체 > 해당 post의 url로 이동
  else:
    form = CommentForm()
  return render(request,"instagram/comment_form.html",{"form":form,})


@login_required
def post_new(request):
  if request.method == "POST":
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():

      post = form.save(commit = False)
      post.author = request.user
      post.save()
      #post모델에는 필수필드들이 있음
      #근데, forms.에서 제출된 값은 그 필수 필드들을 모두 채워주는 것이 아님(일부에 대한 정보만 제출)
      #그 상태에서 바로 save(commit=True)를 해버리면 필수필드가 없다고 에러가 발생

      
      post.tag_set.add(*post.extract_tag_list())
      #*args문법을 사용해, m2m필드인 tag_set에 list전체(tag_list전체)를 넣어준 것임
      #m2m필드는 먼저 db가 저장이 되고난 후(post.save()이후)에 저장이 될 수 있음. m2m필드의 특성에 기인한 건데, m2m필드는 테이블간의 관계를 기록하는 별도의 테이블이 또 필요하기 떄문이라고 함..
        



      messages.success(request,"포스팅을 저장했습니다")
      return redirect(post)
      #return rdirect(post)가 가능한 이유 : Post의 get_absolute_url이 설정되어 있음 > post는 Post모델의 인스턴스인데, get_absolute_url이 인스턴스의 url을 찾아줌

  else:
    form = PostForm()
  return render(request,"instagram/post_form.html",{"form":form,
  })

#~post/4 와같은 식으로 애초에 pk를 받아서 옴
def post_detail(request,pk):
  post=get_object_or_404(Post,pk=pk)
  #pk를 url로 받는데, pk=pk인 Post모델의 행(instance)을 가져와라

  comment_form = CommentForm()

  return render(request,"instagram/post_detail.html",{"post":post,"comment_form":comment_form})
  #위의 post를 html에 전달

@login_required
def post_like(request,pk):
  post=get_object_or_404(Post,pk=pk)
  #pk를 url로 받는데, pk=pk인 Post모델의 행(instance)을 가져와라
  post.like_user_set.add(request.user)
  messages.success(request,f"포스팅 {post.pk}를 좋아합니다!.")

  redirect_url = request.META.get("HTTP_REFERER","root")
  return redirect(redirect_url)
  #위의 post를 html에 전달

@login_required
def post_unlike(request,pk):
  post=get_object_or_404(Post,pk=pk)
  #pk를 url로 받는데, pk=pk인 Post모델의 행(instance)을 가져와라
  post.like_user_set.remove(request.user)
  messages.success(request,f" 포스팅 {post.pk}의 좋아요를 취소합니다!")

  redirect_url = request.META.get("HTTP_REFERER","root")
  return redirect(redirect_url)
  #위의 post를 html에 전달




def user_page(request,username):
  page_user = get_object_or_404(get_user_model(),username=username,is_active = True)
  #모델에서, 조건에 맞는 object를 대려옴
  #is_active : 접근이 허용된 사람만 보겠다!
  post_list = Post.objects.filter(author=page_user)
  post_list_count = post_list.count() #쿼리를 던지는 것. len(post_list)를 하면, 메모리에 던지는 과정이라 post가 많아지면 속도가 느려질 수 있음

  if request.user.is_authenticated : 
    is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
  else:
    is_follow = False

  return render(request,"instagram/user_page.html",{"page_user":page_user,"post_list":post_list,"post_list_count":post_list_count,"is_follow":is_follow})

@login_required
def index(request):
  # timesince = timezone.now() - timedelta(days=3)
  # 날짜범위를 추가하려면, post_list에 다음을 추가
  # .filter(created_at_gte=timesince)
  #timesince보다 만들어진 시기가 뒤쪽일 경우만 가져와라!

  post_list = Post.objects.all()\
    .filter(Q(author=request.user)|
      Q(author__in=request.user.following_set.all()))
  #포스트의 author = user로 묶여있음 > request.user로 비교해도 ㄱㅊ음
  #내 게시글or팔로우 하고 있는 유저들의 게시글을 post_list로 담아서 보냄

  suggested_user_list = get_user_model().objects.all().exclude(pk=request.user.pk).\
  exclude(pk__in=request.user.following_set.all())[:3]
  #pk=user.pk인 애들을 제외하겠다
  #이미 follow된 애들을 제외를 시키겠다
  #pk__in : =뒤에 오는 애들을 배제

  request.user.following_set.all()

  comment_form = CommentForm()

  return render(request,"instagram/index.html",{
    "suggested_user_list":suggested_user_list,"post_list":post_list,"comment_form":comment_form
  })