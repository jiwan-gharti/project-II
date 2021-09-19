import json
import random
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import TemplateView, View
from .models import FeaturedSlider,  OrderItem, Product, SecondLevelCategory, ShippingAddress
from django.contrib import messages
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from django.template.loader import render_to_string

# Create your views here.

def homepage(request):
    FirstSlideProduct    =  Product.objects.order_by("?").distinct()[:8]
    featureItems         =  FeaturedSlider.objects.distinct("name")

    context = {
        "FirstSlideProduct"   :  FirstSlideProduct,
        "featureItems"        :  featureItems
    }
    return render (request, 'mainapp/homepage.html',context)

def details(request,pk):
    singleProduct = Product.objects.get(pk = pk)
    context = {
        "singleProduct" : singleProduct,
    }
    return render(request, 'mainapp/details.html', context)


def Cart(request):
    if request.method == "POST":
        detail_item_id = request.POST.get("detail_item_id")
        item = get_object_or_404(Product, pk = detail_item_id)
        data = OrderItem.objects.filter(user = request.user, item = item)
        if data.exists():
            first_data = data[0]
            # first_data.quantity 
            # first_data.save()
            messages.success(request, 'Already Added At Cart!!!')
        else:
            data = OrderItem.objects.create(user = request.user, item = item)
            data.save()
            messages.success(request, 'Item Added At Cart!!!')
            # print(detail_item_id)
    
    cart_items = OrderItem.objects.filter(user = request.user)
    
    context = {
        "cart_items" : cart_items
    }
    return render(request, "mainapp/cart.html", context)

def RemoveCart(request):
    if request.method == "POST":
        remove_item_id = request.POST.get("remove_cart_id")
        item = get_object_or_404(OrderItem, pk = remove_item_id)
        print()
        item.delete()
        messages.warning(request, "Item Deleted From Cart!!!")
        return redirect("/cart/")


class ContactUs(TemplateView):
    template_name = 'mainapp/contactus.html'

class AboutUs(TemplateView):
    template_name = 'mainapp/aboutus.html'

class ShoppingPage(View):
    def get(self,request):
        return render(request, 'mainapp/shopping_page.html')
     

# def ShoppingPage1(request,slug):
#     # print(slug)
#     print(request.headers)
#     search_key = request.GET.get("search-keys")
#     sort_key = request.GET.get("sort")
#     query_exists = True if len(request.GET) > 0 else False
#     min_value = request.GET.get("price_min")
#     max_value = request.GET.get("price_max")
#     # h2l = request.POST.get("h2l")

#     data = request.GET.getlist("condition[]")

#     print(search_key)
    # if slug != "search":
    #     search_categories = Product.objects.filter(Q(category__second_level_category__product_category__icontains = slug) | 
    #                                                     Q(category__brand_name__icontains = slug)
    
    #                                      )                                          
    # else:
    #     search_categories = Product.objects.filter( Q(name__icontains = search_key) | Q(description__icontains = search_key) |
    #                                                 Q(category__brand_name__icontains = search_key) | 
    #                                                 Q(category__description__icontains = search_key) |
    #                                                 Q(category__second_level_category__first_level_category__first_level_category__icontains = search_key)
    #                                                 )
    
    
#     if sort_key is not None:
#         if sort_key == "price_asc":
#             search_categories = search_categories.order_by("price")
#         elif sort_key == "price_desc":
#             search_categories = search_categories.order_by("-price")

#     if max_value:
#         search_categories = search_categories.filter(price__lte = max_value)
#     if min_value:
#         search_categories = search_categories.filter(price__gte = min_value)

#     # if len(data) > 0:
#     #     print("data > 0")
#     #     all_products =Product.objects.filter(Q(category__second_level_category__product_category__in = data) | 
#     #                                                     Q(category__brand_name__in = data))
#     #     t = render_to_string("ajax/product-filter-list.html",{'data':all_products})
           
#     #     return JsonResponse({"data": t},safe=False)
#     # else:
#     #     all_products = Product.objects.all().order_by('?')


    # context = {
    #     'second_level_search_cactegories':search_categories,
    #     'search_key':search_key,
    #     'query_exists':query_exists,
    #     'get_full_path' : request.get_full_path(),
    # }
    # return render(request, 'mainapp/shopping_page.html',context)



@login_required
def CheckoutPage(request):
    if request.method == "POST":
        forms = CheckoutForm(request.POST or None)
        try:
            orderitems = OrderItem.objects.filter(user = request.user, ordered = False)
            if orderitems.exists():
                if forms.is_valid():
                    first_name  = forms.cleaned_data.get("first_name")
                    last_name = forms.cleaned_data.get("last_name")
                    email = forms.cleaned_data.get("email")
                    phone_number = forms.cleaned_data.get("phone_number")
                    shipping_country = forms.cleaned_data.get("shipping_country")
                    shipping_district = forms.cleaned_data.get("shipping_district")
                    shipping_address2 = forms.cleaned_data.get("shipping_address2")
                    shipping_zip = forms.cleaned_data.get("shipping_zip")
                    payment_option = forms.cleaned_data.get("payment_option")

                    shipping_address = ShippingAddress.objects.create(
                        user = request.user,
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        phone_number = phone_number,
                        country = shipping_country,
                        city_address = shipping_district,
                        street_address = shipping_address2,
                        zip = shipping_zip,
                        payment_option = payment_option,
                        
                    )
                    shipping_address.save()
                    return redirect("/payment/")
                else:
                    print("Form Is Invalid!!!")
            else:
                messages.warning(request,"No Items Found In The cart!!")
                # return redirect("/checkout/")
                # print("There is no order")
        


               
        except ObjectDoesNotExist:
            print("Exception Here........................")
            messages.info(request,"There Is No Item Found In The cart!!")

    else:
        forms = CheckoutForm()

    context = {
        'forms':forms
    }
    return render(request, "mainapp/checkoutpage.html", context)
    
class WishlistPage(TemplateView):
    template_name = 'mainapp/wishlist.html'


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(action)

    item = get_object_or_404(Product, pk = productId)

    order_items = OrderItem.objects.filter(user = request.user, item = item)
    if order_items.exists():
        order_item = order_items[0]
        
        if action == "add":
            order_item.quantity += 1
            order_item.save()
        elif action == 'remove':
            if int(order_item.quantity) > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
                messages.warning(request, "Item Deleted From Cart!!!")    
    return JsonResponse('This is the Response From server!!', safe = False)

@login_required
def PaymentView(request):
    orderItems = OrderItem.objects.filter(user = request.user, ordered = False)
    context = {
        'orderItems': orderItems
    }
    print(orderItems)
    return render(request, "mainapp/payment.html", context)

@csrf_exempt
def ShoppingPage1(request,slug):
    search_key = request.GET.get("search-keys")
    if slug != "search":
            all_products = Product.objects.filter(Q(category__second_level_category__product_category__icontains = slug) | 
                                                        Q(category__brand_name__icontains = slug)
    
                                         )                                          
    else:
        all_products = Product.objects.filter( Q(name__icontains = search_key) | Q(description__icontains = search_key) |
                                                Q(category__brand_name__icontains = search_key) | 
                                                Q(category__description__icontains = search_key) |
                                                Q(category__second_level_category__first_level_category__first_level_category__icontains = search_key)
                                                )
    
    print(request.headers.get('X-Requested-With', "HTTPS"))
    is_ajax = request.headers.get('X-Requested-With', "HTTPS")
    if is_ajax == 'XMLHttpRequest':
        # if request.is_ajax
        # print(request.GET.getlist("condition[]"))
        data = request.GET.getlist("condition[]")
        min_price =  request.GET.get('min_price')
        max_price = request.GET.get("max_price")
        # print(min_price, max_price)
        
        radio_filter = request.GET.get("radio_search")
        # print(radio_filter)




        
        # print(request.GET)
        # print(request.GET.getlist("condition[]"))
        # json_data = json.loads(request.body)
        # # print(json_data)
        # data = json_data['condition']
        # print(data)
        # data = json.loads(request.body)
        # # print(data['condition'])
        # print(data)
        # print(type(data))
        
    
        
        
    
        if len(data) > 0:
            print("data > 0")
            all_products =Product.objects.filter(Q(category__second_level_category__product_category__in = data) | 
                                                            Q(category__brand_name__in = data))
        
        # else:
        #     all_products = Product.objects.all().order_by('?')
        # print(all_products)
        
        if min_price:
            all_products = all_products.filter(price__gte = min_price)
        if max_price:
            all_products = all_products.filter(price__lte = max_price)
        if radio_filter:
            if radio_filter == "under25":
                all_products = all_products.filter(price__lte = 25)
            if radio_filter == "25to50":
                all_products = all_products.filter(price__gte = 25, price__lt = 50)
            if radio_filter == "50to100":
                all_products = all_products.filter(price__gte = 50, price__lt = 100)
            if radio_filter == "100t0200":
                all_products = all_products.filter(price__gte = 100, price__lt = 200)
            if radio_filter == "200toabove":
                all_products = all_products.filter(price__gte = 200)
                print("radio value",radio_filter)
        
        t = render_to_string("ajax/product-filter-list.html",{'data':all_products})   
        return JsonResponse({"data": t},safe=False)
    else:
        context = {
        'second_level_search_cactegories':all_products,
        # 'search_key':search_key,
        # 'query_exists':query_exists,
        # 'get_full_path' : request.get_full_path(),
    }
        return render(request, 'mainapp/shopping_page.html',context)

    context = {
        'second_level_search_cactegories':all_products,
        # 'search_key':search_key,
        # 'query_exists':query_exists,
        # 'get_full_path' : request.get_full_path(),
    }
    return render(request, 'mainapp/shopping_page.html',context)
    return
    # return JsonResponse("HTTP Request !!!!",safe=False)