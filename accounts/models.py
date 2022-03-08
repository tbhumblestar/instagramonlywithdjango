from django.contrib.auth.models import AbstractUser
from django.db import models



#class User(models.Model):
#이런식으로 user모델을 만들어줘도 되지만, 이렇게 하면 user모델이 활성된 user모델을 참조하는거라 에러가 날 수 있음
class User(AbstractUser):
  website_url = models.URLField(blank=True)
  bio = models.TextField(blank=True)