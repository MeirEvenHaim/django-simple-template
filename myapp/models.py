from django.db import models
# Create your models here.



class Sloves(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(max_length = 15 , blank = True ,null = True)
    desc = models.TextField(max_length= 256)
    image = models.ImageField(null=True,blank=True,default='/placeholder.png')
    birth = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.desc