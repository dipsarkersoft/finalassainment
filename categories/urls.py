from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AllCategory,CreateCategory,UpdelCategory,CategoryDetail


router=DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreateCategory.as_view(),name='create'),
    path('update/<int:id>', UpdelCategory.as_view(),name='updatedel'),
    path('all/', AllCategory.as_view(),name='all_category'),
    path('<int:id>/', CategoryDetail.as_view(),name='all_category'),
   

]