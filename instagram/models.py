from tkinter import CASCADE
from django.urls import reverse,reverse_lazy
from django.db import models
from django.conf import settings
import re

## 여러가지 모델에 공통되는 부분(created_at / updated_at)을 미리 빼놓아서, 재사용성을 증가시켜놓은 것임
# class Basemodel(models.Model):
#   created_at = models.DateTimeField(auto_now_add=True)
#   #생성될때 자동으로 모델에 데이터가 추가
#   updated_at = models.DateTimeField(auto_now=True)
#   #수정될때 자동으로 모델의 데이터가 수정됨
    




class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="my_post_set")
  #author이 account의 user와 묶여있여있음 >> user모델의 메소드나 클래스 변수에 관여가능함 >> post = Post()라면, post.author.name 이런것도 가능함(post > post의 author > user의 name)
  #참고로 account의 user모델이 현재 활성화된 user모델이 되는데, 이 파일의 Post모델도 현재활성화된 유저모델과 foreignkey를 맺고 있어서 둘이 묶여있는 것임
  #related_name : 모델명소문자_set이 자동으로 지정됨
  #>post_set이 밑에 m2필드와 충돌이 발생 > 다른걸로 수정해줌



  photo = models.ImageField(upload_to="instagram/post/%Y/%m")
  caption = models.CharField(max_length=500)
  tag_set = models.ManyToManyField('Tag',blank=True)
  location = models.CharField(max_length=100)
  

  like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='like_post_set')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  


  def __str__(self):
    return self.caption

  def extract_tag_list(self):
    tag_name_list =  re.findall(r'#([a-zA-Z\dㄱ-힣]+)',self.caption)
    tag_list = []
    for tag_name in tag_name_list:
      tag,_ = Tag.objects.get_or_create(name=tag_name)
      tag_list.append(tag)
    return tag_list


  def is_like_user(self,user):
    return self.like_user_set.filter(pk=user.pk).exists()

  #get_absolute_url 는 reverse함수를 통해 모델의 개별 데이터 url을 문자열로 반환
  def get_absolute_url(self):
    # return reverse('instagram:post_detail', kwargs={'pk': self.pk})
    #args를 사용해 다음과 같이도 가능
    return reverse('instagram:post_detail', args=[self.pk])

  class Meta:
    ordering = ['-id']
  #post의 배열순서가 id값의 역순으로 > 최신순으로!

  

class Tag(models.Model):
  name = models.CharField(max_length=50,unique=True)

  def __str__(self):
    return self.name


class Comment(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ['-id']




#좋아요 > manytomanyfield정의방법

# 1. post모델에 m2m필드생성
# #like_user_set = models.ManyToManyField(settings.Auth_USER_MODEL,blank=True)

#2번방법 : 별도의 모델 생성 
# class LikeUser(models.Model):
#   post=models.ForeignKey(Post,on_delete=CASCADE)
#   user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
  #하나의 좋아요 > 누가, 어느 포스팅에 했는지가 기록되는 것임

#3번째 방법. 2에서 생성한 모델을 post모델에서 m2m필드에 사용해달라고(관계를 맺어달라고) 하는 것



