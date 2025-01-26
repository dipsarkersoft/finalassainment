from rest_framework import serializers
from .models import CategoriesModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CategoriesModel
        fields='__all__'
