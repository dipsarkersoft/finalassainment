from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MangoListView,MangoCreateView ,MangoUpDelView,MangoDetailView

router=DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('all/', MangoListView.as_view(), name='mango_list_with_query'),
    path('mangoCreate/',MangoCreateView.as_view(),name='mango_create'),
    path('mangoUpDel/<int:id>/',MangoUpDelView.as_view(),name='mangoUpDel'),
    path('<int:id>/',MangoDetailView.as_view(),name='mangodetailsbyid'),

    
   

]