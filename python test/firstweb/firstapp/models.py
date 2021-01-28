from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article (models.Model):
    headline=models.CharField(null=True,blank=True,max_length=300)
    context=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.headline

class Profile(models.Model):
    user = models.OneToOneField(to=User, related_name="profile",on_delete=models.CASCADE)
    nickname = models.CharField(max_length=128,default="很懒的一个用户")
    phone = models.CharField(max_length=11,default="12138")
    address = models.CharField(max_length=256,default="用户很懒，没填写地址")
    abstract = models.TextField(default="用户很懒，没有描述")

    def __str__(self):
        return self.nickname


# from django.contrib.auth.models import AbstractUser
#
# class User(AbstractUser):
#     nickname = models.CharField(max_length=128,default="很懒的一个用户")
#     phone = models.CharField(max_length=11,default="12138")
#     address = models.CharField(max_length=256,default="用户很懒，没填写地址")
#     abstract = models.TextField(default="用户很懒，没有描述")
#
#     def __str__(self):
#         return self.nickname