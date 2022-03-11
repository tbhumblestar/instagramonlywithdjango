from wsgiref.validate import validator
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.validators import RegexValidator


#class User(models.Model):
#이런식으로 user모델을 만들어줘도 되지만, 이렇게 하면 user모델이 활성된 user모델을 참조하는거라 에러가 날 수 있음
class User(AbstractUser):
  website_url = models.URLField(blank=True)
  bio = models.TextField(blank=True)
  phone_number = models.CharField(validators=[RegexValidator(r"^010-?[0-9]\d{3}-?[0-9]\d{4}")],max_length=13,blank=True)
  

  class GenderChoices(models.TextChoices):
    MAle = "M","남성" #"M"은 실제 DB에 저장되는 값, "남성"은 설명
    FEMALE = "W","여성"
    THIRD = "MW", "지금은 21세기니까.."
  gender = models.CharField(choices=GenderChoices.choices,max_length=2,blank=True)

  avatar = models.ImageField(blank=True,upload_to="accounts/avatar/%Y/%m",help_text = "48px * 48px 크기의 png/jpg파일을 업로드 해주세요")

  def send_welcome_email(self):
    
    subject = render_to_string("accounts/welcome_email_subject.txt",{"user":self})
    content = render_to_string("accounts/welcome_email_content.txt",{"user":self})
    #두번쨰 인자의 값들을 넘겨준 값을 반영한, 첫번쨰 인자의 경로에 있는 파일의 내용을 str로 반환

    sender_email = settings.WELCOME_EMAIL_SENDER
    send_mail(subject,content,sender_email,[self.email],fail_silently=False)