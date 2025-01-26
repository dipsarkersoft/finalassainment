from django.db import models
from django.contrib.auth.models import User
from mango.models import MangoModels
from profiles.constant import Delivery_type
# Create your models here.


class OrderModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mango = models.ForeignKey(MangoModels, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    delivery_status=models.CharField(max_length=100,choices=Delivery_type,default='Pending')
    order_date=models.DateTimeField(auto_now_add=True)
    total_price=models.IntegerField(default=0,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    deliveryPostCode=models.IntegerField(null=True,blank=True)
    deliveryPhone=models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.mango.name

