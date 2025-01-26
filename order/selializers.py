from rest_framework import serializers
from .models import OrderModel
from mango.models import MangoModels
from mango.serializers import MangoSerializer

class OrderSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(many=False)
    class Meta:
        model=OrderModel
        fields='__all__'
        read_only_fields = ['user']

        

    
            


        

