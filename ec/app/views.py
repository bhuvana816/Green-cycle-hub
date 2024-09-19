from django.shortcuts import render
from urllib import request
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
import razorpay
from . models import Product
from django.db.models import Count
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.shortcuts import render
from . models import Customer,Cart
from django.shortcuts import get_object_or_404, redirect
from .models import Product, PlasticItem, Cart
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,'app/home.html')

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())
    
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product

class CategoryTitle(View):
    def get(self, request, val):
        # Get the product that matches the title (or return 404 if not found)
        product = Product.objects.filter(title=val).first()
        
        # Handle the case where the product is not found
        if not product:
            return render(request, "app/productdetail.html", {
                'error': "Product not found."
            })

        # Fetch other products in the same category
        related_titles = Product.objects.filter(category=product.category).values('title')

        # Context to pass to the template
        context = {
            'product': product,
            'title': related_titles
        }

        return render(request, "app/productdetail.html", context)

 
    
from django.shortcuts import render
from django.views import View
from .models import PlasticItem

class CategoryPlasticView(View):
    def get(self, request, val):
        # Fetch plastic items based on the category type (e.g., 'pet', 'hdpe', etc.)
        plastic_items = PlasticItem.objects.filter(type=val)
        # Fetch the title (in this case, it's the plastic type display value)
        title = PlasticItem.objects.filter(type=val).values('type').distinct()
        return render(request, 'app/categoryplastic.html', {'plastic_items': plastic_items, 'title': title})
    
    
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", {'product': product})
    
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import PlasticItem

class PlasticProductDetail(View):
    def get(self, request, pk):
        # Use get_object_or_404 to handle cases where the item doesn't exist
        plastic_item = get_object_or_404(PlasticItem, pk=pk)
        return render(request, "app/plasticproductdetail.html", {'plastic_item': plastic_item})
    
    
    


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register SuccessFully")
        else:
            messages.warning(request,"Error! User Registration Failed")
        return render(request,'app/customerregistration.html',locals())
    
    

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Error! Profile Save Failed")
        return render(request,'app/profile.html',locals())


   
def address(request):
    add=Customer.objects.filter(user=request.user)
    return  render(request,'app/address.html',locals())
    
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
            
        else:
            messages.warning(request,"Error! Profile Update Failed")
        return redirect("address")
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product, PlasticItem

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, PlasticItem, Cart

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, PlasticItem, Cart

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    plastic_item_id = request.GET.get('plastic_id')

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        cart_items = Cart.objects.filter(user=user, product=product)
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            Cart.objects.create(user=user, product=product, quantity=1)
    
    elif plastic_item_id:
        plastic_item = get_object_or_404(PlasticItem, id=plastic_item_id)
        cart_items = Cart.objects.filter(user=user, plastic_item=plastic_item)
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            Cart.objects.create(user=user, plastic_item=plastic_item, quantity=1)

    return redirect('cart')



def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    # Separate products and plastic items
    products = cart_items.filter(product__isnull=False)
    plastic_items = cart_items.filter(plastic_item__isnull=False)

    # Calculate total amount and total supercoins
    total_amount = sum(item.product.discounted_price * item.quantity for item in products)
    total_supercoins = sum(item.total_supercoins for item in plastic_items)
    
    # Calculate final amount
    final_amount = total_amount - total_supercoins

    context = {
        'products': products,
        'plastic_items': plastic_items,
        'total_amount': total_amount,
        'total_supercoins': total_supercoins,
        'final_amount': final_amount,  # Pass final_amount to the template
    }

    return render(request, 'app/addtocart.html', context)




from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart

def update_plastic_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        new_quantity = int(request.POST.get('contributed_quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()
        
        return redirect('cart')  # Redirect to cart page
    
    
    
# views.py
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart

def add_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({'quantity': cart_item.quantity, 'total_cost': cart_item.total_cost})

def reduce_quantity(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity goes to 0
    return JsonResponse({'quantity': cart_item.quantity if cart_item.quantity > 0 else 0, 'total_cost': cart_item.total_cost})

def remove_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return JsonResponse({'status': 'Item removed'})



from django.http import JsonResponse
from .models import PlasticItem, Cart

# Increase plastic item quantity
def add_plastic_quantity(request, item_id):
    cart_item = Cart.objects.get(id=item_id, user=request.user, plastic_item__isnull=False)
    cart_item.quantity += 1
    cart_item.save()
    data = {
        'quantity': cart_item.quantity,
        'total_supercoins': cart_item.get_total_supercoins(),  # Ensure this method exists in your Cart model
    }
    return JsonResponse(data)

# Decrease plastic item quantity
def reduce_plastic_quantity(request, item_id):
    cart_item = Cart.objects.get(id=item_id, user=request.user, plastic_item__isnull=False)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        return JsonResponse({'quantity': 0})
    data = {
        'quantity': cart_item.quantity,
        'total_supercoins': cart_item.get_total_supercoins(),  # Ensure this method exists
    }
    return JsonResponse(data)

# Remove plastic item from cart
def remove_plastic_item(request, item_id):
    cart_item = Cart.objects.get(id=item_id, user=request.user, plastic_item__isnull=False)
    cart_item.delete()
    return JsonResponse({'status': 'Item removed'})


from django.http import JsonResponse
from .models import Cart
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart, Product, PlasticItem

def update_cart(request, id):
    quantity_change = int(request.GET.get('quantity_change', 0))
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    
    if cart_item.product:
        if quantity_change > 0:
            cart_item.quantity += quantity_change
        elif quantity_change < 0:
            cart_item.quantity += quantity_change
            if cart_item.quantity <= 0:
                cart_item.delete()
                return JsonResponse(get_cart_summary(request))
    elif cart_item.plastic_item:
        if quantity_change > 0:
            cart_item.quantity += quantity_change
        elif quantity_change < 0:
            cart_item.quantity += quantity_change
            if cart_item.quantity <= 0:
                cart_item.delete()
                return JsonResponse(get_cart_summary(request))
    cart_item.save()
    return JsonResponse(get_cart_summary(request))

def remove_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return JsonResponse(get_cart_summary(request))

def get_cart_summary(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items if item.product) \
                   + sum(item.quantity * item.plastic_item.supercoins_for_basic_quantity for item in cart_items if item.plastic_item)
    total_supercoins = sum(item.total_supercoins for item in cart_items if item.plastic_item)
    return {
        'total_amount': total_amount,
        'total_supercoins': total_supercoins,
        'success': True
    }
    
    
    
class Checkout(View):
    def get(self, request):
        user = request.user
        
        # Fetch user address and cart items
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        
        # Initialize amounts
        total_amount = 0
        total_supercoins = 0
        
        # Calculate total amount for products
        for item in cart_items.filter(product__isnull=False):
            product_value = item.quantity * item.product.discounted_price
            total_amount += product_value
        
        # Calculate total supercoins for plastic items
        for item in cart_items.filter(plastic_item__isnull=False):
            total_supercoins += item.total_supercoins
        
        # Final amount calculation (after subtracting supercoins)
        final_amount = total_amount - total_supercoins
        
        # Add shipping fee (assuming a flat rate of Rs. 40)
        shipping_fee = 40
        total_with_shipping = final_amount + shipping_fee
        razoramount = int(total_with_shipping * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_reptid_12"}
        payment_response = client.order.create(data=data)
        
        order_id = payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created':
            payment = razorpay.Payment(
                user=user,
                amount= final_amount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
           

        # Pass data to the template
        context = {
            'add': add,
            'cart_items': cart_items,
            'total_amount': total_amount,
            'total_supercoins': total_supercoins,
            'final_amount': final_amount,
            'shipping_fee': shipping_fee,
            'total_with_shipping': total_with_shipping,
        }

        return render(request, 'app/checkout.html', context)



