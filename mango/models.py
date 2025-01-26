from django.db import models
from categories.models import CategoriesModel
from django.contrib.auth.models import User
# Create your models here.

class MangoModels(models.Model):
    name=models.CharField(max_length=100)
    categories=models.ForeignKey(CategoriesModel,on_delete=models.CASCADE)
    description=models.TextField()
    price=models.IntegerField()
    quantity=models.IntegerField()
    image=models.URLField(max_length=100,null=True,blank=True)


    def __str__(self):
        return f"{self.name}"





class MangoReviewModel(models.Model):
    mango=models.ForeignKey(MangoModels,on_delete=models.CASCADE)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
       return f"Mango:: {self.mango.name}  Review By :: {self.reviewer.first_name}"  
