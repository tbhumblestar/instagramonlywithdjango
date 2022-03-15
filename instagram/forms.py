from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ["photo","caption","location"]
    widgets={
      "caption": forms.Textarea,
      #위젯을 사용해 어느정도 설정을 추가할 수 있음
      #원래 모델에서 caption이 charfield이다보니 한줄밖에 안되었엇음
    }

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['message']

    #부트스트랩에서 message창의 크기를 조절하기 위함.
    widgets = {
      "message" : forms.Textarea(attrs={"rows":2}),
    }
