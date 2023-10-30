from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as auth_views 
from .forms import *

from  app.api.api import *

urlpatterns = [
    path('', ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name='product-detail'),
    path('add-to-cart/',views.add_to_cart, name = "add-to-cart"),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('registration/', views.Customerregistration.as_view(), name='customerregistration'),

    path('login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name='login'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('mobile/', views.Mobile, name='mobile'),
    path('mobile/<slug:data>/', views.Mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),

    path('topwear/', views.Topwear, name='topwear'),
    path('topwear/<slug:data>/', views.Topwear, name='topweardata'),

    path('bottomwear/', views.Bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.Bottomwear, name='bottomweardata'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='payment_done'),

    path('searchproduct/',views.search_product),

    path('buy/', views.buy_now, name='buy-now'),
    path('changepassword/', views.change_password, name='changepassword'),


    # api
    path('registeruser/',register_user, name= "register_user"),
    path('userlogin/',user_login, name= "user_login"),
    path('userlogout/',user_logout, name= "user_logout"),

    path('addcustomer/',add_customer),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
