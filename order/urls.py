from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrderCreatView,OrderListView,OrderUpdateDeleteView,ReviewCreteView,ReviewListView,PaymentView,paymentSucess,paymentfailed
router=DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('create/',OrderCreatView.as_view(), name='order_create'),
    path('all/',OrderListView.as_view(), name='all_order'),
    path('update/<int:pk>',OrderUpdateDeleteView.as_view(), name='update_del'),
    path('review/',ReviewCreteView.as_view(), name='review'),
    path('review/list/',ReviewListView.as_view(), name='reviewlist'),
    path('payment/',PaymentView.as_view(), name='Payment_view'),
    path('payment/success/<str:trans_id>/', paymentSucess,name='Payment_red'),
    path('payment/failed/', paymentfailed,name='Payment_failed'),

]