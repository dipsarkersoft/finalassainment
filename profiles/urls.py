from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView,active_user,UserByIDView,UserLoginView,LogoutView,UserUpdateView


router=DefaultRouter()



urlpatterns = [
path('',include(router.urls)),
path('register/',UserRegisterView.as_view(),name='register'),
path('login/',UserLoginView.as_view(),name='login'),
path('updateProfile/',UserUpdateView.as_view(),name='updateProfile'),
path('logout/',LogoutView.as_view(),name='logout'),
path('active/<uid64>/<token>',active_user,name='activeuser'),
path('userID/<int:user_id>/',UserByIDView.as_view(),name='getuser')

]
