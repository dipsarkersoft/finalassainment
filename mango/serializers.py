from rest_framework import serializers
from .models import MangoModels,MangoReviewModel
from categories.serializers import CategorySerializer

class MangoSerializer(serializers.ModelSerializer):
    # categories=CategorySerializer()
    class Meta:
        model=MangoModels
        fields='__all__'



class ReviewSerializer(serializers.ModelSerializer):

    reviewer = serializers.StringRelatedField(many=False)
    
    class Meta:
        model=MangoReviewModel
        fields='__all__'
        read_only_fields = ['reviewer']

        