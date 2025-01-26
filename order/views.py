from .models import OrderModel
from .selializers import OrderSerializer
from mango.models import MangoModels
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profiles.permission import IsBuyerAndSeller,IsSeller
from rest_framework.views import APIView
from mango.serializers import ReviewSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from mango.models import MangoReviewModel
from mango.models import MangoReviewModel
from sslcommerz_lib import SSLCOMMERZ
import uuid
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import os
import environ


env = environ.Env()
environ.Env.read_env()
F_URL=env('FRONT_URL')
B_URL="https://mangosellingbackend.onrender.com/order/payment/"
S_ID=env('STORE_ID')
S_PASS=env('STORE_PASS')


def generate_unique_code():

    unique_code = uuid.uuid4().hex.upper()[:12]
    return f"TRAN-{unique_code}"





class OrderCreatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
         
         
        
         orders = [] 
         emdata=[]
         total=0 
         for product in request.data:
         
            serializer = OrderSerializer(data=product)
            if serializer.is_valid():
                qty = serializer.validated_data['quantity']
                mango=serializer.validated_data['mango']
                # print(serializer.validated_data)
                

                try:
                    qu_mango = MangoModels.objects.get(id=mango.id)
                    
                    if qty > qu_mango.quantity:
                        return Response(
                            {"message": f"Not enough  mango ID {mango.id}"}
                            
                        )

                   
                    qu_mango.quantity -= qty
                    qu_mango.save()
                    total_price = qu_mango.price * qty
                    order = serializer.save(user=request.user,total_price=total_price)
                    orders.append(order)
                    total+=order.mango.price*order.quantity
                    emdata.append({
                        'id':order.id,
                        'name':order.mango,
                        'price':order.mango.price,
                        'qty':order.quantity,
                        'total':order.mango.price*order.quantity
                        })

                    #print(order.user.email)
                    # print(order.mango.price)
                    #print(order.quantity*order.mango.price)
                    # print(dir(order))
                    

                except MangoModels.DoesNotExist:
                    return Response({"message": f"Mango ID {mango.id} not found."})
            else:
                return Response(serializer.errors)
         if orders:
              e_sub='Your Order Completed'
              
              e_body=render_to_string('sendemailcreate.html',
                      {  
                       'order':emdata,
                       'total':total                                     
                            })
              
              
              

              email=EmailMultiAlternatives(e_sub,'',to=[request.user.email])
              email.attach_alternative(e_body,'text/html')
              email.send()   

         
         return Response({
             "message": "Orders created successfully.",
             "status":'Sucess'
             
                  
            },
          
        )
  



class OrderListView(APIView):
    permission_classes=[IsBuyerAndSeller]

    def get(self,request):       
         data= OrderModel.objects.all().order_by('-order_date')
                     
         if self.request.user.userprofile.account_type=='Buyer':
            res= data.filter(user=self.request.user)
            serializer=OrderSerializer(res,many=True)
            return Response(
                {
                    'data':serializer.data,
                    'messages':'Your All Order'
                }
            ) 
         else:
            serializer=OrderSerializer(data,many=True)
            return Response(
                {
                    'data':serializer.data,
                    'messages':'Your All Order'
                }
                ) 
              
class OrderUpdateDeleteView(APIView):
    permission_classes=[IsSeller]

    def put(self,request,pk):
         
         try:
            is_order=OrderModel.objects.get(pk=pk)
         except OrderModel.DoesNotExist:
              return Response({
                'message':'Order not found'
            })
         serializer=OrderSerializer(is_order,data=request.data)

         if serializer.is_valid():           
            serializer.save()           
            if  serializer.validated_data.get('delivery_status') == "Completed":
                e_sub='Your Order Completed'
                total_price = is_order.mango.price * is_order.quantity
                e_body=render_to_string('sendOrderemail.html',{
                    'order':is_order,
                    'total_price':total_price                                      
                            })
                

                email=EmailMultiAlternatives(e_sub,'',to=[is_order.user.email])
                email.attach_alternative(e_body,'text/html')
                email.send() 

            return Response({
                        'message':'Order Update Sucess',
                        'data':serializer.data,
                        'status':'sucess'
                    })
         return Response(serializer.errors)
         
                
    def delete(self,request,pk):
        try:
            is_order=OrderModel.objects.get(pk=pk)
        except OrderModel.DoesNotExist:
              return Response({
                'message':'Order not found'
            })
        is_order.delete()
        return Response({
                'message':'Order Deleted Sucessfull',
                'status':'sucess'
            })


class ReviewCreteView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            body=serializer.validated_data['body']
            mango=serializer.validated_data['mango']  
                             
            is_buy=OrderModel.objects.filter(user=request.user,mango=mango).exists()


            if not is_buy:
                return Response({
                    'messages': 'Please Buy This Mnago First Than Review.'
                    })
            already_reviewed = MangoReviewModel.objects.filter(reviewer=request.user, mango=mango).exists()
            if already_reviewed:
                return Response({
                    'message': 'You have already reviewed this mango.',
                    'status':'alreview'
                })
            
            serializer.save(reviewer=request.user)
            return Response({
                'message': 'Review Done',
                'status':'sucess',
                'data':serializer.data
                })
        return Response(serializer.errors)

class ReviewListView(APIView):
    def get(self, request):
       

        mango = request.query_params.get('mango', None)
        products = MangoReviewModel.objects.filter(mango=mango)
        if products:
            serializer = ReviewSerializer(products, many=True)
            return Response({
                'data':serializer.data,
                'message':"All Review "
            
            })
        else:
            return Response({
                'message':"No review Found"
            })



class PaymentView(APIView):

    def post(self,request):

        res=request.data
        trans_id=generate_unique_code()
    

        settings = { 'store_id': S_ID, 'store_pass': S_PASS, 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = res['totalammount']
        post_body['currency'] = "BDT"
        post_body['tran_id'] = trans_id

        post_body['success_url']=f"{B_URL}success/{trans_id}/"
        # post_body['success_url']=f"{B_URL}order/payment/success/{trans_id}"

        post_body['fail_url'] =f"{B_URL}failed/" 
        # post_body['fail_url'] =f"{B_URL}order/payment/failed/" 
        post_body['cancel_url'] =f"{B_URL}failed/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = request.user.email
        post_body['cus_phone'] =res['deliveryPhone']
        post_body['cus_add1'] = res['address']
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcz.createSession(post_body) 
        
        return Response({
            "message":"payment sucess",
            "data":response,
            'transId':trans_id
                     }) 






@csrf_exempt
async def paymentSucess(request, trans_id: str):
    return redirect(f'{F_URL}payment/sucess/{trans_id}')


@csrf_exempt
async def paymentfailed(request):
    return redirect(f'{F_URL}payment/failed')

