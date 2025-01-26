from django.shortcuts import render
from rest_framework import viewsets
from .models import MangoModels
from .serializers import MangoSerializer
from profiles.permission import IsSeller
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from categories.models import CategoriesModel
from rest_framework.exceptions import NotFound

class MangoListView(APIView):

    def get(self, request):
        cat_id = request.query_params.get('cat_id', None)
        if cat_id:
            try:
                mango=MangoModels.objects.filter(categories_id=cat_id)
            except MangoModels.DoesNotExist:
                return Response({'message':"Category Not Found"})
        else:
            mango=MangoModels.objects.all()
        serializer=MangoSerializer(mango,many=True)
        return Response({
            'data':serializer.data,
            'message':'All Product '
        })    


class MangoCreateView(APIView):
    permission_classes=[IsSeller]
    serializer_class=MangoSerializer

    def post(self, request):
        serializer = MangoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'status':'sucess'
                }
                )
        return Response(
            ({
                'data': serializer.errors,
                'status':'sucess'
                }
                )
        )




class MangoDetailView(APIView):
   
    def get(self, request, id):
        try:
           
            mango = MangoModels.objects.get(id=id)
        except MangoModels.DoesNotExist:
          
            raise NotFound({'error': 'Mango not found'})
        
        serializer = MangoSerializer(mango)
        return Response({
            'data': serializer.data,
            'message': 'Mango details GEt successfully'
        })


class MangoUpDelView(APIView):
    permission_classes=[IsSeller]
    serializer_class=MangoSerializer


    def put(self, request,id):      
        try:
            mango = MangoModels.objects.get(id=id)
        except MangoModels.DoesNotExist:
            return Response({'error': 'Mango not found'})

        serializer = MangoSerializer(mango, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request,id):
        try:
             mango = MangoModels.objects.get(id=id)
        except MangoModels.DoesNotExist:
            return Response({'error': 'Mango not found'})
        mango.delete()
        return Response({'message': 'Mango deleted successfully'})


    

    

   

        




     