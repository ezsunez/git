from django.db import models

# Create your models here.
class Difficulty (models.Model):
    dtag=models.CharField(null=False,max_length=300)

class Article (models.Model):
    title=models.CharField(null=True,blank=True,max_length=300)
    context=models.TextField(null=True,blank=True)
    pub_date=models.DateTimeField(auto_now_add=True)
    difficulty=models.ForeignKey('Difficulty',on_delete=models.CASCADE,default=1)


    # def __str__(self):
    #     return self.title
    # def s(self):
    #     return self.id



