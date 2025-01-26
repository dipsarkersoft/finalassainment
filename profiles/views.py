from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
import os
import environ
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response
from .serializers import RegistrerSerializer,LoginSerializer,UpdateProfileSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


env = environ.Env()
environ.Env.read_env()
base_url="https://mangosellingbackend.onrender.com/"
base_front=env('FRONT_URL')

class UserRegisterView(APIView):
    serializer_class=RegistrerSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            token=default_token_generator.make_token(user)           
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            con_link=f"{base_url}active/{uid}/{token}"
            email_sub="Confirm Your Email"
            email_body=render_to_string('confirm_em.html',{
                'confirm_link':con_link
            })
            email=EmailMultiAlternatives(email_sub,'',to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            return Response ('Please Cheak Your Email And Confirm It')
        return Response(serializer.errors)


class UserByIDView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self,request, user_id):
    
        try:
            
            user_profile = UserProfile.objects.get(user_id=user_id)
            
            user = {
                'id': user_profile.user.id,
                'first_name': user_profile.user.first_name,
                'last_name': user_profile.user.last_name,
                'email': user_profile.user.email,
                'account_type': user_profile.account_type,
                'mobile_no': user_profile.mobile_no,
                'address': user_profile.address,
            }
            
            return Response({

                'status': 'success',
                'data': user

                })
    
        except UserProfile.DoesNotExist:
        
            return Response(
                {
            'status': 'error',
            'message': 'User profile not found'
              } 
              )
     
     
       

def active_user(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode('utf-8')
        user=User._default_manager.get(id=uid)
    except(User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect(f"{base_front}login")
        
    

class UserLoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']

            user=authenticate(username=username,password=password)

            if user:
                token,_=Token.objects.get_or_create(user=user)
                login(request,user)
                return Response(
                    {
                    'token':token.key,
                    'user_id':user.id,
                    'account_type':user.userprofile.account_type
                   
                })
            else:

                return Response({
                    'error':'Invalid Credintial'
                })
        return Response(serializer.errors)   


  
class UserUpdateView(APIView):
  
    permission_classes = [IsAuthenticated]
     
    
    def put(self,request):
        user=request.user
        qu_user=User.objects.get(id=user.id)
        
        email=request.data.get('email',qu_user.email)
        first_name=request.data.get('first_name',qu_user.first_name)
        last_name=request.data.get('last_name',qu_user.last_name)
        mobile_no=request.data.get('mobile_no',qu_user.userprofile.mobile_no)
        address=request.data.get('address',qu_user.userprofile.address)
        #print(email,address,mobile_no,last_name,first_name)

        
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.userprofile.mobile_no=mobile_no
        user.userprofile.address=address
        #print(user.userprofile.address)
        user.save()
        user.userprofile.save()
        
        return Response({
            "message": "User updated successfully.",
             'data':{
                   "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "mobile_no": user.userprofile.mobile_no,
                    "address": user.userprofile.address
             }
            
            })


        
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
        

