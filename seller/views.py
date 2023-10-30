from django.shortcuts import render, redirect
from app.models import Product
# Create your views here.

def add_product(request):
    if request.method == 'POST':
        title = request.POST['title']
        selling_price = request.POST['selling_price']
        discounted_price = request.POST['discounted_price']
        description = request.POST['description'] 
        brand = request.POST['brand']
        category = request.POST['category']
        product_image = request.FILES['image']

        product = Product.objects.create(
        title = title,
        selling_price = float(selling_price),
        discounted_price = float(discounted_price),
        description = description,
        brand = brand,
        category = category,
        product_image = product_image,
    )
        product.save()
        return redirect('/')

    return render(request,"app/add_product.html")