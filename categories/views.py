from django.shortcuts import render
from rest_framework import viewsets 
from .models import CategoriesModel
from .serializers import CategorySerializer
from profiles.permission import IsSeller
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response





class AllCategory(APIView):

    def get(self, request):
        data = CategoriesModel.objects.all()
        serializer = CategorySerializer(data, many=True)
        return Response(serializer.data)
    
    

class CategoryDetail(APIView):


    def get(self, request, id):

        try:

            category = CategoriesModel.objects.get(id=id)

            serializer = CategorySerializer(category)
            
            return Response(serializer.data)
        
        except CategoriesModel.DoesNotExist:
          
            return Response({"error": "Category not found."})





class CreateCategory(APIView):
    permission_classes=[IsSeller]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class UpdelCategory(APIView):
    def put(self, request,id):
        

        try:
            mango = CategoriesModel.objects.get(id=id)
        except CategoriesModel.DoesNotExist:
            return Response({'error': 'Categories not found'})

        serializer = CategorySerializer(mango, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

    def delete(self,request,id):
        
        try:
             mango = CategoriesModel.objects.get(id=id)
        except CategoriesModel.DoesNotExist:
            return Response({'error': 'Mango not found'})
        mango.delete()
        return Response({'message': 'Mango deleted successfully'})

        
    
   

        
