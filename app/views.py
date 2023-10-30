from django.shortcuts import render,redirect
from . models import *
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

from .forms import *
class ProductView(View):
    def get(self,request):
     topwears = Product.objects.filter(category = 'TW')
     bottomwears = Product.objects.filter(category = 'BW')
     mobiles = Product.objects.filter(category = 'M')
     laptopes = Product.objects.filter(category = 'L')
     return render(request, "app/home.html",{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptopes':laptopes})
    
class ProductDetailView(View):
 def get(self,request, pk):
        product = Product.objects.get(pk = pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
          item_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user = request.user)).exists()
          return render(request,"app/productdetail.html",{'product':product,'item_already_in_cart':item_already_in_cart})
        else:
          return render(request,"app/productdetail.html",{'product':product,'item_already_in_cart':item_already_in_cart})

def add_to_cart(request):
      user = request.user
      product_id = request.GET.get('prod_id')
      product = Product.objects.get(id = product_id)
      Cart(user = user, product = product).save()
      return redirect('/cart/')

def show_cart(request):
      if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user = user)
            amount = 0.0
            shipping_amount = 70.0
            total_amount = 0.0
            cart_product = [prod for prod in Cart.objects.all() if prod.user == user]
            if cart_product:
                  for prod in cart_product:
                        tempamount = (prod.quantity * prod.product.discounted_price)
                        amount += tempamount
                        total_amount = amount + shipping_amount
                  return render(request,"app/addtocart.html",{'Cart':cart,'amount':amount, 'total_amount':total_amount})
            else:
               return render(request,"app/emptycart.html")    

def plus_cart(request):
       if request.method=='GET':
          prod_id = request.GET['prod_id']
          c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
          c.quantity += 1
          c.save()
          amount = 0.0
          shipping_amount = 70.0
          cart_product = [p for p in Cart.objects.all() if p.user == request.user]
          if cart_product:
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount
            data = {
            'quantity':c.quantity,
            'amount':amount,
            'totallamount': amount + shipping_amount,
            }
            return JsonResponse(data)

def minus_cart(request):
       if request.method=='GET':
          prod_id = request.GET['prod_id']
          c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
          c.quantity -= 1
          c.save()
          amount = 0.0
          shipping_amount = 70.0
          cart_product = [p for p in Cart.objects.all() if p.user == request.user]
          if cart_product:
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount
            data = {
            'quantity':c.quantity,
            'amount':amount,
            'totallamount': amount + shipping_amount,
            }
            return JsonResponse(data)


def remove_cart(request):
   if request.method=='GET':
          prod_id = request.GET['prod_id']
          c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
          c.delete()
          amount = 0.0
          shipping_amount = 70.0
          cart_product = [p for p in Cart.objects.all() if p.user == request.user]
          if cart_product:
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount
            data = {
            'amount':amount,
            'totallamount': amount + shipping_amount,
            }
            return JsonResponse(data)


def Mobile(request, data =None):
    if data == None:
          mobile = Product.objects.filter(category = 'M')
    elif data == 'redmi' or data == 'samsung':
          mobile = Product.objects.filter(category='M').filter(brand = data)
    elif data == 'below':
          mobile = Product.objects.filter(category='M', discounted_price__lt = 10000)

    elif data == 'above':
          mobile = Product.objects.filter(category = 'M').filter(discounted_price__gt = 10000)
    return render(request, 'app/mobile.html',{'mobile':mobile})

def laptop(request, data =None):
    if data == None:
          laptop = Product.objects.filter(category = 'L')
    elif data == 'HP' or data == 'Aasus':
          laptop = Product.objects.filter(category='L').filter(brand = data)
    elif data == 'below':
          laptop = Product.objects.filter(category='L', discounted_price__lt = 40000)

    elif data == 'above':
          laptop = Product.objects.filter(category = 'L').filter(discounted_price__gt = 40000)
    return render(request, 'app/laptop.html',{'laptops':laptop})

def Topwear(request, data =None):
    if data == None:
          topwear = Product.objects.filter(category = 'TW')
    elif data == 'Zara' or data == 'GUCCI':
          topwear = Product.objects.filter(category='TW').filter(brand = data)
    elif data == 'below':
          topwear = Product.objects.filter(category='TW', discounted_price__lt = 1000)

    elif data == 'above':
          topwear = Product.objects.filter(category = 'TW').filter(discounted_price__gt = 1000)
    return render(request, 'app/topwear.html',{'Topwear':topwear})
def Bottomwear(request, data =None):
    if data == None:
          bottomwear = Product.objects.filter(category = 'BW')
    elif data == 'Zara' or data == 'GUCCI':
          bottomwear = Product.objects.filter(category='BW').filter(brand = data)
    elif data == 'below':
          bottomwear = Product.objects.filter(category='BW', discounted_price__lt = 1000)

    elif data == 'above':
          bottomwear = Product.objects.filter(category = 'BW').filter(discounted_price__gt = 1000)
    return render(request, 'app/bottomwear.html',{'bottomwear':bottomwear})


class ProfileView(View):
    def get(request, self):
         form = CustomerProfileForm()
         return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    def post(request, self):
          form = CustomerProfileForm(request.POST)
          if form.is_valid():
                usr = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']

                reg = Customer(user=usr, name=name, locality=locality,
                city=city, state=state, zipcode=zipcode)
                reg.save()
                messages.success(request, 'Congratulation!! Profile Updated Succesfully')
                return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

class Customerregistration(View):
      def get(self,request):
            form = CustomerRegistrationForm()
            return render(request, 'app/customerregistration.html',{'form':form})
      
      def post(self, request):
          form = CustomerRegistrationForm(request.POST)
          if form.is_valid():
                messages.success(request, "Registration successfull")
                form.save()
          return render(request, 'app/customerregistration.html',{'form':form})

def address(request):
     address = Customer.objects.get(user = request.user)
     print(address)
     return render(request, 'app/address.html',{'address': address, 'active': 'btn-primary'})

# def checkout(request):
#  user = request.user
#  address = Customer.objects.filter(user = user)
#  cart_item = Cart.objects.filter(user = user)
#  amount = 0.0
#  shipping_amount = 70.0
#  total_amount = 0.0
#  cart_product = [prod for prod in Cart.objects.all() if prod.user == user]
#  if cart_product:
#       for prod in cart_product:
#             tempamount = (prod.quantity * prod.product.discounted_price)
#             amount += tempamount
#             total_amount = amount + shipping_amount
#       # print("total amount",total_amount)
                  
#  return render(request, 'app/checkout.html',{'cart_item':cart_item,'total_amount':total_amount,'add':address})


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    shipping_amount = 70.0
    totalamount = 0.0

    for item in cart_items:
        item.product_amount = item.quantity * item.product.discounted_price
        totalamount += item.product_amount

    totalamount += shipping_amount

    return render(request, 'app/checkout.html',{'cart_item':cart_items,'total_amount':totalamount,'add':add})
        

def payment_done(request):
    user = request.user
    custid = request.GET.get("custid")
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(
            user=user, customer=customer, product=c.product, quantity=c.quantity
        ).save()
        c.delete()
    return redirect("/orders/")

def orders(request):
     obj = OrderPlaced.objects.filter(user=request.user)
     return render(request, 'app/orders.html',{"obj":obj})

def search_product(request):
     return render(request, 'app/app/home.html')

def buy_now(request):
     return render(request, 'app/buynow.html')

def change_password(request):
     return render(request, 'app/changepassword.html')
