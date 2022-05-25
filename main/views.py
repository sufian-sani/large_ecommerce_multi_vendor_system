from django.shortcuts import render, redirect, HttpResponse
from app_1.models import Products, Brand, Category
from checkout.models import Order_Table, Order_Table_2, Order_Table_3
from app_1.models import campaign_table, Brand, campaign_categories_percentage, campaign_product_table, Flash_Sell, attribute_connect_with_product, campaign_product_attribute
from app_1.models import Subcategory_1
from vendor_dashboard_app.models import vendor_registration_table
from datetime import datetime
from django.db.models import Q
#infinite Loading
from django.views.generic import ListView
from .forms import Upload_Deposit_slip
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from app_1.models import customer_review
from django.core import serializers
from django.http import JsonResponse
from main.models import home_benner, home_little_benner, home_bottom_benner, home_side_benner, Shop_now_page_benner
import json
from app_1.models import User
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password

from sslcommerz_sdk.enums import TransactionStatus

# TODO: create payment_handler.py file
from .payment_handler import payment_handler, store


def payment_success(request):
    return redirect('home')


@csrf_exempt
def payment_init_view(request):
    # TODO: Freeze the cart, see what cart freezing is
    session, created = payment_handler.get_or_create_session(
        store=store,
        tran_id="test",
        currency="BDT",
        total_amount=100,
        cus_name="test",
        cus_email="test@test.com",
        cus_add1="test",
        cus_city="test",
        cus_postcode="1234",
        cus_country="test",
        cus_phone="123456",
        success_url="<URL to redirect cutomer when transaction is successful>",
        fail_url="<URL to redirect cutomer when transaction is failed>",
        cancel_url="<URL to redirect cutomer when transaction is cancelled>",
        ipn_url="<URL of ipn_view>",
    )
    # TODO: Redirect customer to session.redirect_url


@csrf_exempt
def ipn_view(request):
    # TODO: Make this URL public, i.e accessible without logging in
    # TODO: Disable CSRF protection for this view
    # TODO: post_dict = {dict of request POST values}
    session, verified_right_now = payment_handler.verify_transaction(
        payload=post_dict,
    )
    if verified_right_now:
        if session.status == TransactionStatus.VALID:
            print(f"Tran ID: {session.tran_id} successful...")
            # TODO: Update order payment status in your database
        else:
            print("Transaction failed/cancelled!")
            # TODO: Unfreeze the cart sothat customer can modify/delete the cart



def handler404(request, exception):
    context = {}
    response = render(request, "boomboom_user/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "boomboom_user/500.html", context=context)
    response.status_code = 500
    return response



#Home
def home(request, template='boomboom_user/index.html', page_template='boomboom_user/cat_index.html'):
    
    Featured_Products = Products.objects.filter(make_star=True)[:8]
    
    all_benners = home_benner.objects.all()
    
    filter_all_cats = Category.objects.all()[:12]
    
    last_Flash_Sell = Flash_Sell.objects.last()
    
    all_home_little_benner = home_little_benner.objects.all()
    all_home_bottom_benner = home_bottom_benner.objects.all()
    
    all_home_side_benner = home_side_benner.objects.all()
    
    featured_brands = Brand.objects.filter(Featured_Brand=True)[:6]
    featured_vendor = vendor_registration_table.objects.filter(featured_vendor=True, vendor_activation=True)[:6]
    
    
    fil_campign_tbl = campaign_table.objects.filter(finish_campaign=False)
    fil_campign_tbl_cnt = fil_campign_tbl.count()
    
    
    get_campign_tbl = None
    allcampign_tbl = None
    
    
    if fil_campign_tbl_cnt == 1:
        get_campign_tbl = campaign_table.objects.get(finish_campaign=False)
    
    if fil_campign_tbl_cnt > 1:
        allcampign_tbl = fil_campign_tbl

    # category_home_side = Products.objects.filter(Subcategory_1__add_home=True).filter(make_star=True)[:5]

    subcats_home_side = Subcategory_1.objects.filter(add_home = True)[:8]

    # category_home_side_product_1 = Products.objects.filter(Subcategory_1=3).filter(make_star=True)[:5]
    # category_home_side_product_2 = Products.objects.filter(Subcategory_1=4).filter(make_star=True)[:5]
    # category_home_side_product_3 = Products.objects.filter(Subcategory_1=5).filter(make_star=True)[:5]
    # category_home_side_product_4 = Products.objects.filter(Subcategory_1=6).filter(make_star=True)[:5]
    # category_home_side_product_5 = Products.objects.filter(Subcategory_1=7).filter(make_star=True)[:5]
    # category_home_side_product_6 = Products.objects.filter(Subcategory_1=8).filter(make_star=True)[:5]
    #
    # print(category_home_side_product_1, category_home_side_product_2, category_home_side_product_3, category_home_side_product_4, category_home_side_product_5, category_home_side_product_6)

    # top_products = Products.objects.filter(Subcategory_1=8).filter(make_star=True)[:5]
    
    flash_sell = Products.objects.filter(flash_sell=True)[:4]
    
    json_flash_sell = serializers.serialize("json", flash_sell)
    
    Top_Product = Products.objects.filter(Review_Quantity__isnull=False).order_by('-Review_Quantity')[:5]
    print('Top_Product')
    print(Top_Product)

    
    # home_cat_prod = []
    # for i in filter_all_cats:
    #     filter_prod_cat = Products.objects.filter(Category=i).order_by('-MRP_Price')[:4]
    #     home_cat_prod.append(filter_prod_cat)
    
    context={
        'page_template': page_template,
        'Featured_Products':Featured_Products,
        'all_benners':all_benners,
        'filter_all_cats':filter_all_cats,
        'allcampign_tbl':allcampign_tbl,
        'get_campign_tbl':get_campign_tbl,
        # 'category_home_side_product_1':category_home_side_product_1,
        # 'category_home_side_product_2':category_home_side_product_2,
        # 'category_home_side_product_3':category_home_side_product_3,
        # 'category_home_side_product_4':category_home_side_product_4,
        # 'category_home_side_product_5':category_home_side_product_5,
        # 'category_home_side_product_6':category_home_side_product_6,
        'flash_sell':flash_sell,
        'json_flash_sell':json_flash_sell,
        'last_Flash_Sell':last_Flash_Sell,
        'all_home_little_benner':all_home_little_benner,
        'all_home_bottom_benner':all_home_bottom_benner,
        'all_home_side_benner':all_home_side_benner,
        'featured_brands':featured_brands,
        'featured_vendor':featured_vendor,
        'Top_Product':Top_Product,
        # 'category_home_side':category_home_side,
        'subcats_home_side':subcats_home_side,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)



class CategoriesListView(ListView):
    model = Category
    context_object_name = 'all_cat'
    paginate_by = 1
    template_name = 'boomboom_user/index.html'



#Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'boomboom_user/category_list.html',{'data':data})


#Brand
def brand_list(request, template='boomboom_user/brand_list.html', page_template='boomboom_user/infinte_loading_brand_list.html'):
    brand_list_get = Brand.objects.all()
    brnd_lst = True
    context = {'brand_list_get': brand_list_get,
               'page_template': page_template,
               'brnd_lst':brnd_lst,
               }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)


#Brands product show
def showing_product_by_brands(request, s_brand_pk, template='boomboom_user/showing_product_by_brands.html', page_template='boomboom_user/infinte_loading_showing_product_by_brands.html'):
    get_brand_uniq_slug  = Brand.objects.get(slug=s_brand_pk)
    showing_brand_list_get = Products.objects.filter(Brand=get_brand_uniq_slug)
    context = {'showing_brand_list_get': showing_brand_list_get,
               'page_template': page_template,
               'get_brand_uniq_slug':get_brand_uniq_slug,
               }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)


    



#Product-list
def product_list(request, template='boomboom_user/product_list.html', page_template='boomboom_user/next_product_list.html'):
    
    all_Shop_now_page_benner = Shop_now_page_benner.objects.all()
    
    cats_lst = Category.objects.all()
    brand_list = Brand.objects.all()
    
    sort_by_prd = "All"
    
    context = {
        'data':Products.objects.all().order_by('Product_Name'),
        'page_template': page_template,
        'sort': 'Product Name: A to Z',
        'all_Shop_now_page_benner':all_Shop_now_page_benner,
        'sort_by_prd':sort_by_prd,
        'cats_lst':cats_lst,
        'brand_list':brand_list,
    }

    if request.is_ajax():
        template = page_template
    return render(request, template, context)




def product_list_sort(request, template='boomboom_user/product_list.html', page_template='boomboom_user/next_product_list.html'):
    
    product_start_price = request.GET.get('product_start_price')
    product_end_price = request.GET.get('product_end_price')
    
    name_sortby = request.GET.get('name_sortby')
    sort_by_prd = request.GET.get('sort_by_prd')
    
    cat_id = request.GET.get('cat_name')
    subcat_id = request.GET.get('subcat_id')
    
    
    search_key = request.GET.get('search_key')
    
    if sort_by_prd=="All":
        
        all_Shop_now_page_benner = Shop_now_page_benner.objects.all()
        
        cats_lst = Category.objects.all()
        brand_list = Brand.objects.all()
        
        if product_start_price and product_end_price:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Discount_Price')
                
        else:        
            
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.all().order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.all().order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.all().order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.all().order_by('-Discount_Price')
            
        context = {
            'data':data,
            'page_template': page_template,
            'sort': name_sortby,
            'all_Shop_now_page_benner':all_Shop_now_page_benner,
            'sort_by_prd':sort_by_prd,
            'cats_lst':cats_lst,
            'brand_list':brand_list,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    
    
    elif sort_by_prd=="Category":
        get_Category = Category.objects.get(id=cat_id)
        
        subcats = Subcategory_1.objects.filter(Category=get_Category)
        
        brand_list = Brand.objects.all()
        
        
        if product_start_price and product_end_price:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(Category=get_Category).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(Category=get_Category).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(Category=get_Category).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(Category=get_Category).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Discount_Price')
            
            
        else:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(Category=get_Category).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(Category=get_Category).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(Category=get_Category).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(Category=get_Category).order_by('-Discount_Price')
            
            
    
        context = {
            'data':data,
            'page_template': page_template,
            'sort': name_sortby,
            'sort_by_prd':sort_by_prd,
            'subcats':subcats,
            'brand_list':brand_list,
            'get_Category':get_Category,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
        
        
        
    elif sort_by_prd=="subCategory":
        getsubcat = Subcategory_1.objects.get(id=subcat_id)
        
        
        cats_lst = Category.objects.all()
        
        brand_list = Brand.objects.all()
        
        
        
        
        
        if product_start_price and product_end_price:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(Subcategory_1=getsubcat).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(Subcategory_1=getsubcat).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(Subcategory_1=getsubcat).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(Subcategory_1=getsubcat).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Discount_Price')
                
                
        else:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(Subcategory_1=getsubcat).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(Subcategory_1=getsubcat).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(Subcategory_1=getsubcat).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(Subcategory_1=getsubcat).order_by('-Discount_Price')
            
            
    
        context = {
            'data':data,
            'page_template': page_template,
            'sort': name_sortby,
            'sort_by_prd':sort_by_prd,
            'cats_lst':cats_lst,
            'brand_list':brand_list,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    
    
    
    elif sort_by_prd=="searching":
        
        no_result = False
    
            
        template='boomboom_user/product_list.html' 
        page_template='boomboom_user/next_product_list.html'
        
        brand_list = Brand.objects.all()
        cats_lst = Category.objects.all()
        
        
        
        if product_start_price and product_end_price:
            if name_sortby == "Product Name: A to Z":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Discount_Price')
                
            
            elif name_sortby == "Price: High to low":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Discount_Price')
                
                
        else:
            if name_sortby == "Product Name: A to Z":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).order_by('Product_Name')
                
                
            elif name_sortby == "Product Name: Z to A":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).order_by('Discount_Price')
                
            
            elif name_sortby == "Price: High to low":
                search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).order_by('-Discount_Price')
            
        
        
        cont_search_result_all = search_result_all.count()
        if cont_search_result_all==0:
            no_result = True
        
        context = {
            'data':search_result_all,
            'page_template': page_template,
            
            
            'search_key':search_key,
            'cont_search_result_all':cont_search_result_all,
            'no_result':no_result,
            'search_result_all':search_result_all,
            'brand_list':brand_list,
            'cats_lst':cats_lst,
            'sort_by_prd':sort_by_prd,
            'sort':name_sortby,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
        
    
    elif sort_by_prd=="flash_sale":
        
        cats_lst = Category.objects.all()
        
        brand_list = Brand.objects.all()
        
        
        
        if product_start_price and product_end_price:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(flash_sell=True).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(flash_sell=True).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(flash_sell=True).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(flash_sell=True).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('-Discount_Price')
                
                
        else:
            if name_sortby == "Product Name: A to Z":
                data = Products.objects.filter(flash_sell=True).order_by('Product_Name')
                
            elif name_sortby == "Product Name: Z to A":
                data = Products.objects.filter(flash_sell=True).order_by('-Product_Name')
            
            elif name_sortby == "Price: Low to High":
                data = Products.objects.filter(flash_sell=True).order_by('Discount_Price')
            
            elif name_sortby == "Price: High to low":
                data = Products.objects.filter(flash_sell=True).order_by('-Discount_Price')
            
            
    
        context = {
            'data':data,
            'page_template': page_template,
            'sort': name_sortby,
            'sort_by_prd':sort_by_prd,
            'cats_lst':cats_lst,
            'brand_list':brand_list,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)    
    
    
    






def price_filter(request, template='boomboom_user/product_list.html', page_template='boomboom_user/next_product_list.html'):
    
    product_start_price = request.GET.get('product_start_price')
    product_end_price = request.GET.get('product_end_price')
    
    
    sort_by_prd = request.GET.get('sort_by_prd')
    
    cat_id = request.GET.get('cat_name')
    subcat_id = request.GET.get('subcat_id')
    
    search_key = request.GET.get('search_key')
    
    if sort_by_prd=="All":
        
        all_Shop_now_page_benner = Shop_now_page_benner.objects.all()
        
        cats_lst = Category.objects.all()
        brand_list = Brand.objects.all()
        
        
        
        data = Products.objects.filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
        
        
            
        context = {
            'data':data,
            'page_template': page_template,
            'product_start_price': product_start_price,
            'product_end_price': product_end_price,
            'all_Shop_now_page_benner':all_Shop_now_page_benner,
            'sort_by_prd':sort_by_prd,
            'cats_lst':cats_lst,
            'brand_list':brand_list,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    
    
    elif sort_by_prd=="Category":
        get_Category = Category.objects.get(id=cat_id)
        
        subcats = Subcategory_1.objects.filter(Category=get_Category)
        
        brand_list = Brand.objects.all()
        
        data = Products.objects.filter(Category=get_Category).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
        
          
    
        context = {
            'data':data,
            'page_template': page_template,
            'product_start_price': product_start_price,
            'product_end_price': product_end_price,
            'sort_by_prd':sort_by_prd,
            'subcats':subcats,
            'brand_list':brand_list,
            'get_Category':get_Category,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
        
        
        
    elif sort_by_prd=="subCategory":
        getsubcat = Subcategory_1.objects.get(id=subcat_id)
        
        
        cats_lst = Category.objects.all()
        
        brand_list = Brand.objects.all()
        
        data = Products.objects.filter(Subcategory_1=getsubcat).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
        
        
    
        context = {
            'data':data,
            'page_template': page_template,
            'product_start_price': product_start_price,
            'product_end_price': product_end_price,
            'sort_by_prd':sort_by_prd,
            'cats_lst':cats_lst,
            'brand_list':brand_list,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    
    
    
    elif sort_by_prd=="searching":
        
        no_result = False
    
            
        template = 'boomboom_user/product_list.html' 
        page_template ='boomboom_user/next_product_list.html'
        
        brand_list = Brand.objects.all()
        cats_lst = Category.objects.all()
        
        
        search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
        
        cont_search_result_all = search_result_all.count()
        if cont_search_result_all==0:
            no_result = True
        
        context = {
            'data':search_result_all,
            'page_template': page_template,
            'product_start_price': product_start_price,
            'product_end_price': product_end_price,
            
            'search_key':search_key,
            'cont_search_result_all':cont_search_result_all,
            'no_result':no_result,
            'search_result_all':search_result_all,
            'brand_list':brand_list,
            'cats_lst':cats_lst,
            'sort_by_prd':sort_by_prd,
            
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
        
    
    elif sort_by_prd=="flash_sale":
        
        cats_lst = Category.objects.all()
        
        brand_list = Brand.objects.all()
        
        data = Products.objects.filter(flash_sell=True).filter(MRP_Price__range=(product_start_price,product_end_price)).order_by('Product_Name')
        
    
        context = {
            'data':data,
            'page_template': page_template,
            'product_start_price': product_start_price,
            'product_end_price': product_end_price,
            'sort_by_prd':sort_by_prd,
            'cats_lst':cats_lst,
            'brand_list':brand_list,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context) 








# product_list_Z_to_A
def product_list_Z_to_A(request, template='boomboom_user/product_list.html',
                 page_template='boomboom_user/next_product_list.html'):
    context = {
        'data': Products.objects.all().order_by('-Product_Name'),
        'page_template': page_template,
        'sort': 'Product Name: Z to A',
    }

    if request.is_ajax():
        template = page_template
    return render(request, template, context)



# product_list_Price_Lowest_first
def product_list_Price_Lowest_first(request, template='boomboom_user/product_list.html',
                 page_template='boomboom_user/next_product_list.html'):
    context = {
        'data': Products.objects.all().order_by('MRP_Price'),
        'page_template': page_template,
        'sort': 'Price: Lowest first',
    }


    if request.is_ajax():
        template = page_template
    return render(request, template, context)



# product_list_Price_Highest_first
def product_list_Price_Highest_first(request, template='boomboom_user/product_list.html',
                 page_template='boomboom_user/next_product_list.html'):
    context = {
        'data': Products.objects.all().order_by('-MRP_Price'),
        'page_template': page_template,
        'sort':'Price: Highest first',
    }

    if request.is_ajax():
        template = page_template
    return render(request, template, context)







    

    
    
class product_ListView(ListView):
    context_object_name = 'data'
    paginate_by = 4
    template_name = 'boomboom_user/product_list.html'
    def get_queryset(self):
        return Products.objects.all().order_by('Product_Name')
    




def product_details(request, slug):
    get_product = Products.objects.get(slug=slug)
    
    filter_prod_by_cat = Products.objects.filter(Category=get_product.Category).exclude(slug=slug).order_by('Discount_Price')[:9]

    filter_attri_conct_with_product = None
    if get_product.TYPE_OF_PRODUCTS =='Variable Product' or get_product.TYPE_OF_PRODUCTS =='Virtual Product':
        filter_attri_conct_with_product = attribute_connect_with_product.objects.filter(connect_with_product=get_product)


    get_review_total = customer_review.objects.filter(Product=get_product)
    get_review = get_review_total.count()

    Total_sum_of_reviews_quentity = 0
    for i in get_review_total:
        Total_sum_of_reviews_quentity = Total_sum_of_reviews_quentity + i.Ratting_qty

    if Total_sum_of_reviews_quentity == 0:
        avarage_Total_sum_of_reviews_quentity = 0
    else:
        avarage_Total_sum_of_reviews_quentity_1 = Total_sum_of_reviews_quentity / get_review
        avarage_Total_sum_of_reviews_quentity = format(avarage_Total_sum_of_reviews_quentity_1, ".1f")

    last_three_review = customer_review.objects.filter(Product=get_product).order_by('-id')[:3]

    int_avarage_Total_sum_of_reviews_quentity = float(avarage_Total_sum_of_reviews_quentity)

    zero = ""
    poin_five = ""
    one = ""
    one_point_five = ""
    two = ""
    tow_point_five = ""
    three = ""
    three_point_five = ""
    four = ""
    four_point_five = ""
    five = ""

    if int_avarage_Total_sum_of_reviews_quentity == 0:
        zero = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 0 and int_avarage_Total_sum_of_reviews_quentity < 1:
        poin_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity ==1:
        one = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 1 and int_avarage_Total_sum_of_reviews_quentity < 2:
        one_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 2:
        two = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 2 and int_avarage_Total_sum_of_reviews_quentity <3:
        tow_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 3:
        three = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 3 and int_avarage_Total_sum_of_reviews_quentity <4:
        three_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 4:
        four = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 4 and int_avarage_Total_sum_of_reviews_quentity < 5:
        four_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 5:
        five = "1"

    print("int_avarage_Total_sum_of_reviews_quentity")
    print(int_avarage_Total_sum_of_reviews_quentity)


    context2 = {'get_product': get_product, 'get_review': get_review, 'last_three_review': last_three_review,
                'avarage_Total_sum_of_reviews_quentity': avarage_Total_sum_of_reviews_quentity, 'zero':zero, 'poin_five':poin_five, 'one':one, 'one_point_five':one_point_five, 'two':two, 'tow_point_five':tow_point_five, 'three':three, 'three_point_five':three_point_five, 'four':four, 'four_point_five':four_point_five, 'five':five, 'filter_attri_conct_with_product':filter_attri_conct_with_product, 'filter_prod_by_cat':filter_prod_by_cat}

    return render(request, 'boomboom_user/product_details_page.html', context2)

 
   
def campaign_product_details(request, slug):
        
    get_campaign_prodt_tbl = campaign_product_table.objects.get(slug=slug)
    get_product = Products.objects.get(slug=get_campaign_prodt_tbl.product.slug)
    
    prd_slg = get_product.slug
    
    filter_attri_conct_with_product = None
    if get_product.TYPE_OF_PRODUCTS =='Variable Product' or get_product.TYPE_OF_PRODUCTS =='Virtual Product':
        filter_attri_conct_with_product = campaign_product_attribute.objects.filter(campaign_product=get_campaign_prodt_tbl)

    get_review_total = customer_review.objects.filter(Product=get_product)
    get_review = get_review_total.count()

    Total_sum_of_reviews_quentity = 0
    for i in get_review_total:
        Total_sum_of_reviews_quentity = Total_sum_of_reviews_quentity + i.Ratting_qty

    if Total_sum_of_reviews_quentity == 0:
        avarage_Total_sum_of_reviews_quentity = 0
    else:
        avarage_Total_sum_of_reviews_quentity_1 = Total_sum_of_reviews_quentity / get_review
        avarage_Total_sum_of_reviews_quentity = format(avarage_Total_sum_of_reviews_quentity_1, ".1f")

    last_three_review = customer_review.objects.filter(Product=get_product).order_by('-id')[:3]

    int_avarage_Total_sum_of_reviews_quentity = float(avarage_Total_sum_of_reviews_quentity)

    zero = ""
    poin_five = ""
    one = ""
    one_point_five = ""
    two = ""
    tow_point_five = ""
    three = ""
    three_point_five = ""
    four = ""
    four_point_five = ""
    five = ""

    if int_avarage_Total_sum_of_reviews_quentity == 0:
        zero = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 0 and int_avarage_Total_sum_of_reviews_quentity < 1:
        poin_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity ==1:
        one = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 1 and int_avarage_Total_sum_of_reviews_quentity < 2:
        one_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 2:
        two = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 2 and int_avarage_Total_sum_of_reviews_quentity <3:
        tow_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 3:
        three = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 3 and int_avarage_Total_sum_of_reviews_quentity <4:
        three_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 4:
        four = "1"
    elif int_avarage_Total_sum_of_reviews_quentity > 4 and int_avarage_Total_sum_of_reviews_quentity < 5:
        four_point_five = "1"
    elif int_avarage_Total_sum_of_reviews_quentity == 5:
        five = "1"

    print("int_avarage_Total_sum_of_reviews_quentity")
    print(int_avarage_Total_sum_of_reviews_quentity)

    now_campgn = get_campaign_prodt_tbl.campaign.id
    
    get_cmpgn = campaign_table.objects.get(id=now_campgn)
    
    if get_cmpgn.finish_campaign:
        return redirect('product_details', prd_slg)
        
    else:
        context2 = {'get_product': get_product, 'get_review': get_review, 'last_three_review': last_three_review,
                    'avarage_Total_sum_of_reviews_quentity': avarage_Total_sum_of_reviews_quentity, 'zero':zero, 'poin_five':poin_five, 'one':one, 'one_point_five':one_point_five, 'two':two, 'tow_point_five':tow_point_five, 'three':three, 'three_point_five':three_point_five, 'four':four, 'four_point_five':four_point_five, 'five':five, 'get_campaign_prodt_tbl':get_campaign_prodt_tbl, 'filter_attri_conct_with_product':filter_attri_conct_with_product}
    
        return render(request, 'boomboom_user/campaign_product_details_page.html', context2)

   
   
   
    

#customer-dashboard
def customer_dashboard(request):
    if request.user.is_authenticated:
        customer = request.user
        print('customer.old_customer_uniqe_id')
        print(customer.old_customer_uniqe_id)
        print(customer)
        old_cus_uniq_id = customer.old_customer_uniqe_id

        filter_cus_Ordr_Table_3 = Order_Table_3.objects.filter(old_unq_number=old_cus_uniq_id).order_by('old_order_date')
        print(filter_cus_Ordr_Table_3)

        filter_all_orders = Order_Table.objects.filter(Customer=customer).order_by('-Order_Id')
        
        form_Up_Deposit_slip = Upload_Deposit_slip()
        
        context={'filter_all_orders':filter_all_orders, 'form_Up_Deposit_slip':form_Up_Deposit_slip, 'filter_cus_Ordr_Table_3':filter_cus_Ordr_Table_3}
        return render(request,'boomboom_user/customer_dashboard.html', context)
    else:
        return redirect('login_register')



def customer_order_view(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        
        if Order_Table.objects.filter(id=pk, Customer=customer):
            get_orders = Order_Table.objects.get(id=pk, Customer=customer)
            
            filter_orders_prod = Order_Table_2.objects.filter(Order_Id=get_orders)
            
            context={'get_orders':get_orders, 'filter_orders_prod':filter_orders_prod}
            return render(request, 'boomboom_user/customer_order_view.html', context)
        else:
            return redirect('customer-dashboard')
    else:
        return redirect('login_register')


def old_customer_order_view(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        old_cus_uniq_id = customer.old_customer_uniqe_id

        if Order_Table_3.objects.get(old_order_id=pk, old_unq_number=old_cus_uniq_id):
            get_Order_Table_3 = Order_Table_3.objects.get(old_order_id=pk, old_unq_number=old_cus_uniq_id)

            context = {'get_Order_Table_3': get_Order_Table_3}
            return render(request, 'boomboom_user/old_customer_order_view.html', context)
        else:
            return redirect('customer-dashboard')
    else:
        return redirect('login_register')


def customer_pay_order(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        
        if Order_Table.objects.filter(id=pk, Customer=customer):
            get_orders = Order_Table.objects.get(id=pk, Customer=customer)
            filter_orders_prod = Order_Table_2.objects.filter(Order_Id=get_orders)
            context={'get_orders':get_orders, 'filter_orders_prod':filter_orders_prod}
            return render(request, 'boomboom_user/customer_pay_order.html', context)
        else:
            return redirect('customer-dashboard')
    else:
        return redirect('login_register')
        



def bank_deposite_submit(request):
    if request.method == "POST":
        order_h_id = request.POST.get('order_h_id')
        Holder_Name= request.POST.get('Holder_Name')
        Bank_Name= request.POST.get('Bank_Name')
        Branch_Name= request.POST.get('Branch_Name')
        Account_Number= request.POST.get('Account_Number')
        Slip_Number= request.POST.get('Slip_Number')
        
        get_ordr = Order_Table.objects.get(id = order_h_id)
        
        form_Up_Deposit_slip = Upload_Deposit_slip(request.POST, request.FILES, instance=get_ordr)
        
        if form_Up_Deposit_slip.is_valid():
            other_value = form_Up_Deposit_slip.save(commit=False)
            other_value.Holder_Name = Holder_Name
            other_value.Bank_Name = Bank_Name
            other_value.Branch_Name = Branch_Name
            other_value.Account_Number = Account_Number
            other_value.Slip_Number = Slip_Number
            other_value.save()
        else:
            messages.error(request, 'Unsupported file extension. Choose Only PNG, JPG and JPEG files PLease ..')
    return redirect('customer-dashboard')
    
    
    
def cancel_order(request):
    cancel_button = request.POST.get('cancel_button')
    get_ordr = Order_Table.objects.get(id = cancel_button)
    get_ordr.Order_Status='Cancelled'
    get_ordr.save()
    return redirect('customer-dashboard')



#cart_page
def cart_page(request):
    return render(request, 'boomboom_user/cart_page.html')





#all_store_page
def stores(request, template='boomboom_user/stores.html', page_template='boomboom_user/infinte_loading_stores.html'):
    stores_e_r_t = vendor_registration_table.objects.filter(vendor_activation=True)
    vendor_total_product_count = []

    for i in stores_e_r_t:
        ppppp = Products.objects.filter(Vendors=i).count()
        vendor_total_product_count.append(ppppp)

    if request.is_ajax():
        template = page_template

    print("vendor_total_product_count")
    print("vendor_total_product_count")
    print(vendor_total_product_count)

    total_zip = zip(stores_e_r_t, vendor_total_product_count)

    vendor_first_page = True

    context = {'page_template': page_template, 'stores_e_r_t':stores_e_r_t, 'vendor_total_product_count':vendor_total_product_count, 'total_zip':total_zip, 'vendor_first_page':vendor_first_page}

    return render(request, template, context)
    
    
    
def search_store_user_page(request, template='boomboom_user/stores.html', page_template='boomboom_user/infinte_loading_stores.html'):
    name_search_store_user_page = request.POST.get('name_search_store_user_page')
    
    # stores_e_r_t_p = vendor_registration_table.objects.filter(vendor_activation=True)
    # stores_e_r_t = stores_e_r_t_p.filter(vendor_name = name_search_store_user_page)
    stores_e_r_t = vendor_registration_table.objects.filter(vendor_activation=True).filter(Q(vendor_name__icontains = name_search_store_user_page) |  Q(vendor_shop_name__icontains = name_search_store_user_page))

    count_stores_e_r_t= stores_e_r_t.count()

    search_result_none=False
    if count_stores_e_r_t == 0:
        search_result_none = True

    vendor_total_product_count = []

    for i in stores_e_r_t:
        ppppp = Products.objects.filter(Vendors=i).count()
        vendor_total_product_count.append(ppppp)

    if request.is_ajax():
        template = page_template

    search_vendor = True

    total_zip = zip(stores_e_r_t, vendor_total_product_count)

    context = {'page_template': page_template, 'stores_e_r_t': stores_e_r_t,
               'vendor_total_product_count': vendor_total_product_count, 'total_zip': total_zip, 'name_search_store_user_page':name_search_store_user_page, 'search_vendor':search_vendor, 'count_stores_e_r_t':count_stores_e_r_t, 'search_result_none':search_result_none}

    return render(request, template, context)
    
    
    
    
    
    
#single_vendor_page
def single_vendor(request, s_v_pk, template='boomboom_user/single_vendor.html', page_template='boomboom_user/infinte_loading_single_vendor.html'):

    s_v_stores_e_r_t = vendor_registration_table.objects.get(vendor_phone_no=s_v_pk)
    ppppp = Products.objects.filter(Vendors=s_v_stores_e_r_t)
    ppppp_count = Products.objects.filter(Vendors=s_v_stores_e_r_t).count()

    lst_cat = []
    for i in ppppp:
        p_cat = i.Category
        if p_cat not in lst_cat:
            lst_cat.append(p_cat)

    vendor_sort_by = "All"

    # return render(request, 'boomboom_user/single_vendor.html', {'ppppp':ppppp, 's_v_stores_e_r_t':s_v_stores_e_r_t, 'ppppp_count':ppppp_count})
    if request.is_ajax():
        template = page_template
    context = {'page_template': page_template, 'ppppp':ppppp, 's_v_stores_e_r_t':s_v_stores_e_r_t, 'ppppp_count':ppppp_count, "lst_cat":lst_cat, 'vendor_sort_by':vendor_sort_by}

    return render(request, template, context)




def vendor_price_filter(request, template='boomboom_user/single_vendor.html', page_template='boomboom_user/infinte_loading_single_vendor.html'):
    vendor_sort_by = request.GET.get('vendor_sort_by')
    product_start_price = request.GET.get('product_start_price')
    product_end_price = request.GET.get('product_end_price')
    vendor_phn_no = request.GET.get('vendor_phn_no')
    cat_id = request.GET.get('cat_id')

    no_result = False
    Category_get = None

    print(vendor_sort_by, product_start_price, product_end_price, vendor_phn_no)

    s_v_stores_e_r_t = vendor_registration_table.objects.get(vendor_phone_no=vendor_phn_no)
    ppppp2 = Products.objects.filter(Vendors=s_v_stores_e_r_t)
    ppppp_count = Products.objects.filter(Vendors=s_v_stores_e_r_t).count()

    lst_cat = []
    for i in ppppp2:
        p_cat = i.Category
        if p_cat not in lst_cat:
            lst_cat.append(p_cat)

    if vendor_sort_by == "All":

        ppppp = Products.objects.filter(Vendors=s_v_stores_e_r_t).filter(MRP_Price__range=(product_start_price,product_end_price))

        result_qty = ppppp.count()
        if result_qty == 0:
            no_result = True

    elif vendor_sort_by == "Category":

        Category_get = Category.objects.get(id=cat_id)

        ppppp = Products.objects.filter(Vendors=s_v_stores_e_r_t).filter(
            MRP_Price__range=(product_start_price, product_end_price)).filter(Category=Category_get)

        result_qty = ppppp.count()

        if result_qty == 0:
            no_result = True


    if request.is_ajax():
        template = page_template

    context = {'page_template': page_template, 'ppppp': ppppp, 's_v_stores_e_r_t': s_v_stores_e_r_t,
               'ppppp_count': ppppp_count, "lst_cat": lst_cat, 'vendor_sort_by': vendor_sort_by, 'result_qty':result_qty, 'no_result':no_result, 'cat_id':cat_id, 'Category_get':Category_get, 'product_start_price':product_start_price, 'product_end_price':product_end_price}

    return render(request, template, context)


def vendor_category(request, template='boomboom_user/single_vendor.html', page_template='boomboom_user/infinte_loading_single_vendor.html'):
    category_id = request.GET.get('category_id')
    vendor_number = request.GET.get('vendor_number')

    s_v_stores_e_r_t = vendor_registration_table.objects.get(vendor_phone_no=vendor_number)

    Category_get = Category.objects.get(id=category_id)

    ppppp = Products.objects.filter(Vendors=s_v_stores_e_r_t).filter(Category=Category_get)

    cate_result_qty = ppppp.count()

    ppppp2 = Products.objects.filter(Vendors=s_v_stores_e_r_t)
    ppppp_count = Products.objects.filter(Vendors=s_v_stores_e_r_t).count()

    lst_cat = []
    for i in ppppp2:
        p_cat = i.Category
        if p_cat not in lst_cat:
            lst_cat.append(p_cat)

    vendor_sort_by = "Category"

    # return render(request, 'boomboom_user/single_vendor.html', {'ppppp':ppppp, 's_v_stores_e_r_t':s_v_stores_e_r_t, 'ppppp_count':ppppp_count})
    if request.is_ajax():
        template = page_template
    context = {'page_template': page_template, 'ppppp': ppppp, 's_v_stores_e_r_t': s_v_stores_e_r_t,
               'ppppp_count': ppppp_count, "lst_cat": lst_cat, 'vendor_sort_by': vendor_sort_by, 'cate_result_qty':cate_result_qty, 'Category_get':Category_get}

    return render(request, template, context)




# campaign page
def campaign_page(request):
    filter_current_campaign = campaign_table.objects.filter(finish_campaign=False)
    count_filter_current_campaign = filter_current_campaign.count()
    
    context = {'filter_current_campaign':filter_current_campaign}
    
    if count_filter_current_campaign == 0:
        return render(request, 'boomboom_user/campaign_page.html')
    elif count_filter_current_campaign == 1:
        get_current_campaign = campaign_table.objects.get(finish_campaign=False)
        return redirect('campaign_landing', get_current_campaign.campaign_slug)
    elif count_filter_current_campaign > 1:
        return render(request, 'boomboom_user/campaign_list.html', context)
        



#campaign_landing_page
def campaign_landing(request, pk, template='boomboom_user/campaign_landing.html', page_template='boomboom_user/new_campaign_landing.html'):
    # filter_current_campaign = campaign_table.objects.filter(finish_campaign=False)
    # if filter_current_campaign:
        
        
    # else:
    #     get_current_campaign = None
    #     dates_end_strptime = None
    
    
    get_current_campaign = campaign_table.objects.get(campaign_slug=pk)
        
    campaign_last_time = get_current_campaign.end_time
    print(type(campaign_last_time))
    dates_end_strptime = datetime.strptime(str(campaign_last_time), '%Y-%m-%d').strftime('%b %d, %Y')
    
    filter_campgn_categries_prcntage = campaign_categories_percentage.objects.filter(campaign=get_current_campaign).filter(percentage__isnull=False)
    
    context = {'filter_campgn_categries_prcntage':filter_campgn_categries_prcntage, 'get_current_campaign':get_current_campaign, 'dates_end_strptime':dates_end_strptime, 'page_template': page_template}
    if request.is_ajax():
        template = page_template
    return render(request, template, context)




#campaign_category_landing_page
def camcat_land2(request, pk, template='boomboom_user/camcat_land.html', page_template='boomboom_user/new_camcat_land.html'):
    get_campgn_catgries_prcntag = campaign_categories_percentage.objects.get(id=pk)
    
    # filter_Table_products_campaign = Table_products_campaign.objects.filter(category_percentage=get_campgn_catgries_prcntag)
    # if filter_Table_products_campaign:
    #     filter_Table_products_campaign = Table_products_campaign.objects.get(category_percentage=get_campgn_catgries_prcntag)
    # else:
    #     filter_Table_products_campaign=None
    
    get_categries = get_campgn_catgries_prcntag.Category
    
    filtr_cgin_prod_tbl = campaign_product_table.objects.filter(category_percentage=get_campgn_catgries_prcntag)
    
    
    filter_Subcategory_1 = Subcategory_1.objects.filter(Category=get_categries)
    
    
    context = {'get_campgn_catgries_prcntag':get_campgn_catgries_prcntag, 'filter_Subcategory_1':filter_Subcategory_1, 'get_categries':get_categries, 'page_template': page_template, 'filtr_cgin_prod_tbl':filtr_cgin_prod_tbl}
    if request.is_ajax():
        template = page_template
    return render(request, template, context)



# campaign_category_landing_page
def category_campaign_product(request, pk, template='boomboom_user/category_campaign_product.html',
                 page_template='boomboom_user/category_campaign_product_new.html'):
    get_campgn_catgries_prcntag = campaign_categories_percentage.objects.get(id=pk)

    get_categries = get_campgn_catgries_prcntag.Category

    filtr_cgin_prod_tbl = campaign_product_table.objects.filter(category_percentage=get_campgn_catgries_prcntag)

    filter_Subcategory_1 = Subcategory_1.objects.filter(Category=get_categries)



    lst_brand = []
    for br in filtr_cgin_prod_tbl:
        if br.product.Brand:
            br_id = br.product.Brand.slug
            if br_id not in lst_brand:
                lst_brand.append(br_id)
        else:
            br_id = 0
            if br_id not in lst_brand:
                lst_brand.append(br_id)

    other_brands = False

    print(lst_brand)
    if 0 in lst_brand:
        print('zero ase')
        other_brands = True
        lst_brand.remove(0)

    print(lst_brand)

    brand_list_get = Brand.objects.filter(slug__in=lst_brand)[:6]

    context = {'get_campgn_catgries_prcntag': get_campgn_catgries_prcntag,
               'filter_Subcategory_1': filter_Subcategory_1,
               'get_categries': get_categries,
               'page_template': page_template,
               'filtr_cgin_prod_tbl': filtr_cgin_prod_tbl,
               'brand_list_get':brand_list_get,
               }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)



#Brand
def camcat_land(request, pk, template='boomboom_user/cam_brand_list.html', page_template='boomboom_user/cam_infinte_loading_brand_list.html'):
    get_campgn_catgries_prcntag = campaign_categories_percentage.objects.get(id=pk)
    get_categries = get_campgn_catgries_prcntag.Category
    filtr_cgin_prod_tbl = campaign_product_table.objects.filter(category_percentage=get_campgn_catgries_prcntag)

    lst_brand = []
    for br in filtr_cgin_prod_tbl:
        if br.product.Brand:
            br_id = br.product.Brand.slug
            if br_id not in lst_brand:
                lst_brand.append(br_id)
        else:
            br_id = 0
            if br_id not in lst_brand:
                lst_brand.append(br_id)

    other_brands = False

    print(lst_brand)
    if 0 in lst_brand:
        print('zero ase')
        other_brands = True
        lst_brand.remove(0)

    print(lst_brand)

    brand_list_get = Brand.objects.filter(slug__in=lst_brand)

    print(brand_list_get)


    context = {'brand_list_get': brand_list_get,
               'page_template': page_template,
               'get_categries':get_categries,
               'get_campgn_catgries_prcntag':get_campgn_catgries_prcntag,
               'other_brands':other_brands,
               }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)



#Brands product show
def show_campaign_brands_products(request, template='boomboom_user/cam_showing_product_by_brands.html', page_template='boomboom_user/cam_infinte_loading_showing_product_by_brands.html'):
    campaign_cat = request.GET.get('campaign_cat')
    brand = request.GET.get('brand')

    if brand == '0':
        get_campgn_catgries_prcntag = campaign_categories_percentage.objects.get(id=campaign_cat)


        filtr_cgin_prod_tbl = campaign_product_table.objects.filter(
            category_percentage=get_campgn_catgries_prcntag).filter(product__Brand__isnull=True)

        other_brands = True

        context = {
                   'page_template': page_template,
                   'filtr_cgin_prod_tbl': filtr_cgin_prod_tbl,
                   'other_brands':other_brands,
                   }
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    else:
        get_campgn_catgries_prcntag = campaign_categories_percentage.objects.get(id=campaign_cat)

        get_brand_uniq_slug  = Brand.objects.get(slug=brand)

        filtr_cgin_prod_tbl = campaign_product_table.objects.filter(category_percentage=get_campgn_catgries_prcntag).filter(product__Brand=get_brand_uniq_slug)

        showing_brand_list_get = Products.objects.filter(Brand=get_brand_uniq_slug)

        context = {'showing_brand_list_get': showing_brand_list_get,
                   'page_template': page_template,
                   'get_brand_uniq_slug':get_brand_uniq_slug,
                   'filtr_cgin_prod_tbl':filtr_cgin_prod_tbl,
                   }
        if request.is_ajax():
            template = page_template
        return render(request, template, context)


    
@csrf_exempt
def save_customer_review(request):
    varprod_review_hash_id = request.POST.get('varid_prod_review_hash_id')
    get_prod =  Products.objects.get(slug=varprod_review_hash_id)
    
    varcustomer_review_rat = request.POST.get('qty_customer_ratings')
    varcustomer_review_text = request.POST.get('varid_customer_review_text')
    
    varcustomer_name = request.user
    save_cus_review = customer_review(Customer=varcustomer_name, Product=get_prod, Ratting_qty=varcustomer_review_rat, Review_Text=varcustomer_review_text)
    save_cus_review.save()

    # product table has review quantity
    past_qty = get_prod.Review_Quantity
    if past_qty:
        get_prod.Review_Quantity=past_qty+1
        get_prod.save()
    else:
        get_prod.Review_Quantity = 1
        get_prod.save()
    
    get_review_total = customer_review.objects.filter(Product=get_prod)
    get_review = get_review_total.count()
    
    return HttpResponse(get_review)
    
    
    
    
    
@csrf_exempt
def update_avarage_rat_url(request):
    slug = request.POST.get('varid_prod_review_hash_id')
    get_product = Products.objects.get(slug=slug)
    
    get_review_total = customer_review.objects.filter(Product=get_product)
    get_review = get_review_total.count()

    Total_sum_of_reviews_quentity = 0
    
    for i in get_review_total:
        Total_sum_of_reviews_quentity = Total_sum_of_reviews_quentity + i.Ratting_qty  

    if Total_sum_of_reviews_quentity==0:
        avarage_Total_sum_of_reviews_quentity = 0
    else:
        avarage_Total_sum_of_reviews_quentity_1 = Total_sum_of_reviews_quentity/get_review
        avarage_Total_sum_of_reviews_quentity = format(avarage_Total_sum_of_reviews_quentity_1, ".1f")
        
    return HttpResponse(avarage_Total_sum_of_reviews_quentity)
    
    
@csrf_exempt    
def func_update_star_rat_url(request):
    slug = request.POST.get('varid_prod_review_hash_id')
    get_product = Products.objects.get(slug=slug)
    
    get_review_total = customer_review.objects.filter(Product=get_product)
    get_review = get_review_total.count()

    Total_sum_of_reviews_quentity = 0
    
    for i in get_review_total:
        Total_sum_of_reviews_quentity = Total_sum_of_reviews_quentity + i.Ratting_qty  

    if Total_sum_of_reviews_quentity==0:
        avarage_Total_sum_of_reviews_quentity = 0
    else:
        avarage_Total_sum_of_reviews_quentity_1 = Total_sum_of_reviews_quentity/get_review
        avarage_Total_sum_of_reviews_quentity = format(avarage_Total_sum_of_reviews_quentity_1, ".1f")
        

    int_avarage_Total_sum_of_reviews_quentity = float(avarage_Total_sum_of_reviews_quentity)

    zero = ""
    poin_five = ""
    one = ""
    one_point_five = ""
    two = ""
    tow_point_five = ""
    three = ""
    three_point_five = ""
    four = ""
    four_point_five = ""
    five = ""

    if int_avarage_Total_sum_of_reviews_quentity == 0:
        
        star_status = "zero"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity > 0 and int_avarage_Total_sum_of_reviews_quentity < 1:
        star_status = "poin_five"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity ==1:
        
        star_status = "one"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity > 1 and int_avarage_Total_sum_of_reviews_quentity < 2:
        
        star_status = "one_point_five"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity == 2:
        
        star_status = "two"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity > 2 and int_avarage_Total_sum_of_reviews_quentity <3:
        
        star_status = "tow_point_five"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity == 3:
        
        star_status = "three"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity > 3 and int_avarage_Total_sum_of_reviews_quentity <4:
        
        star_status = "three_point_five"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity == 4:
        
        star_status = "four"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity > 4 and int_avarage_Total_sum_of_reviews_quentity < 5:
        
        star_status = "four_point_five"
        return HttpResponse(star_status)
    elif int_avarage_Total_sum_of_reviews_quentity == 5:
        
        star_status = "five"
        return HttpResponse(star_status)
        
        

#for sending otp

# import http.client as ht
# def send_sms(request):


#     conn = ht.HTTPConnection("smsplus.sslwireless.com")

#     payload = '''{
#      "api_token": "744d2817-6c3b-4a70-a91e-e3f9ee5cf1b5",
#      "sid": "BOOMBOOMNONAPI",
#      "sms": "From boomboom ltd.. it's a congratulations massage. You got 1 lakh taka, as a bestemployee of the month ...PLEASE collecte the money from Azizul Bari Pran.....this massage from MD.SOHEL CHOWDHURY",
#      "msisdn": "8801681882854",
#      "csms_id": "123456"
#     }'''

    
#     conn.request("GET", "https://smsplus.sslwireless.com/api/v3/send-sms?api_token=&sid=&sms=&msisdn=&csms_id=", payload)

#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))
#     return render(request, 'boomboom_user/index.html')




import http.client as ht
import json

def send_sms(request):


    conn = ht.HTTPSConnection("smsplus.sslwireless.com")
    headers = {'Content-type': 'application/json'}


    payload = {
     "api_token": "744d2817-6c3b-4a70-a91e-e3f9ee5cf1b",
     "sid": "BOOMBOOMNONAPI",
     "sms": "From boomboom ltd.. it's a congratulations massage. You got 1 lakh taka, as a bestemployee of the month ...PLEASE collecte the money from Azizul Bari Pran.....this massage from MD.SOHEL CHOWDHURY",
     "msisdn": "8801822224080",
     "csms_id": "123456"
    }

    payload_json = json.dumps(payload)
    conn.request("POST", "/api/v3/send-sms", payload_json, headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return render(request, 'boomboom_user/index.html')
    

 
@csrf_exempt        
def get_all_cats(request):
    all_cats = Category.objects.all()
    get_cat_seri = serializers.serialize('json', all_cats)
    return JsonResponse(get_cat_seri, safe=False)
    
    
def category_products(request, pk, template='boomboom_user/product_list.html', page_template='boomboom_user/next_product_list.html'):
    get_Category = Category.objects.get(id=pk)
    
    subcats = Subcategory_1.objects.filter(Category=get_Category)
    
    brand_list = Brand.objects.all()
    
    sort_by_prd = "Category"
    
    
    
    context = {
        'data':Products.objects.filter(Category=get_Category).order_by('Product_Name'),
        'page_template': page_template,
        'get_Category':get_Category,
        'brand_list':brand_list,
        'sort_by_prd':sort_by_prd,
        'subcats':subcats,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)
    


def subcategory_products(request, pk, template='boomboom_user/product_list.html', page_template='boomboom_user/next_product_list.html'):
    getsubcat = Subcategory_1.objects.get(id=pk)
    
    brand_list = Brand.objects.all()
    cats_lst = Category.objects.all()
    
    sort_by_prd = "subCategory"
    
    context = {
        'data':Products.objects.filter(Subcategory_1=getsubcat).order_by('Product_Name'),
        'page_template': page_template,
        'brand_list':brand_list,
        'sort_by_prd':sort_by_prd,
        'getsubcat':getsubcat,
        'cats_lst':cats_lst,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)
    
    
    
    
def flash_details_product(request, pk, template='boomboom_user/product_list.html', page_template='boomboom_user/next_product_list.html'):
    get_Flash_Sell = Flash_Sell.objects.get(id=pk)
    
    brand_list = Brand.objects.all()
    cats_lst = Category.objects.all()
    
    sort_by_prd = "flash_sale"
    
    flash_sales_products = Products.objects.filter(flash_sell=True).order_by('Product_Name')
    
    context = {
        'data':flash_sales_products,
        'page_template': page_template,
        'get_Flash_Sell':get_Flash_Sell,
        'brand_list':brand_list,
        'cats_lst':cats_lst,
        'sort_by_prd':sort_by_prd,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)





@csrf_exempt
def search_main_box(request):
    var_main_search_box = request.POST.get('var_main_search_box')
    
    search_value_choose = request.POST.get('search_value_choose')
    
    if search_value_choose=="Categories":
        search_result = Category.objects.filter(Q(Category_Name__icontains = var_main_search_box))[0:6]
    elif search_value_choose=="Stores":
        search_result = vendor_registration_table.objects.filter(Q(vendor_shop_name__icontains = var_main_search_box) | Q(vendor_name__icontains = var_main_search_box) | Q(vendor_phone_no__icontains = var_main_search_box) | Q(vendor_email__icontains = var_main_search_box))[0:6]
    elif search_value_choose=="Brands":
        search_result = Brand.objects.filter(Q(Brand_Name__icontains = var_main_search_box))[0:6]
    else:
        
        search_result3 = Products.objects.filter(Q(Product_Name__icontains = var_main_search_box))[0:2]
        
        # active_cm = campaign_table.objects.filter(finish_campaign=False)
        
        # search_result4 = []
        
        # for i in search_result3:
        #     for j in active_cm:
        #         cam_prd = campaign_product_table.objects.filter(product=i).filter(campaign=j)
                
        #         search_result4.append(cam_prd)
    
        search_result = search_result3
        # search_result2 = Products.objects.filter(Q(Product_Name__icontains = var_main_search_box))[0:3]
        
        # search_result = search_result2+search_result5
    
        #search_result = Products.objects.filter(Q(Product_Name__icontains = var_main_search_box))[0:3]
    
    query_search_product = serializers.serialize('json', search_result)
    return JsonResponse(query_search_product, safe=False)
    
    
    
    
def submit_search_word(request):
    search_key = request.GET.get('search_key')
    
    sort_by_prd = "searching"
    
    name_type_search2 = request.GET.get('name_type_search')
    print(name_type_search2[:-1])
    print(name_type_search2[1:])
    print(name_type_search2[:-1][1:])

    name_type_search = name_type_search2[:-1][1:]
    
    no_result = False
    
    if name_type_search=="Categories":
        
        search_result = Category.objects.filter(Q(Category_Name__icontains = var_main_search_box))[0:6]
        
        
        
    elif name_type_search=="Stores":
        
        template='boomboom_user/stores.html'
        page_template='boomboom_user/infinte_loading_stores.html'
        
        brand_list = Brand.objects.all()
        cats_lst = Category.objects.all()
        
        
        stores_e_r_t = vendor_registration_table.objects.filter(Q(vendor_shop_name__icontains = search_key) | Q(vendor_name__icontains = search_key) | Q(vendor_phone_no__icontains = search_key) | Q(vendor_email__icontains = search_key))
        cont_stores_e_r_t = stores_e_r_t.count()
        if cont_stores_e_r_t==0:
            no_result = True
        
        context = {'page_template': page_template, 
                    'stores_e_r_t':stores_e_r_t, 
                    'name_type_search':name_type_search,
                    'search_key':search_key,
                    'cont_stores_e_r_t':cont_stores_e_r_t,
                    'no_result':no_result,
                    'brand_list':brand_list,
                    'cats_lst':cats_lst,
                    'sort_by_prd':sort_by_prd,
        }
        
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
        
        
        
    
    elif name_type_search=="Brands":
        
        template='boomboom_user/brand_list.html'
        page_template='boomboom_user/infinte_loading_brand_list.html'
        
        search_result = Brand.objects.filter(Q(Brand_Name__icontains = search_key))
        cnt_search_result = search_result.count()
        
        brand_list = Brand.objects.all()
        cats_lst = Category.objects.all()
        
        if cnt_search_result==0:
            no_result = True
        
        context = {'brand_list_get': search_result,
                   'page_template': page_template,
                   'name_type_search':name_type_search,
                   'search_key':search_key,
                   'cnt_search_result':cnt_search_result,
                   'no_result':no_result,
                   'brand_list':brand_list,
                   'cats_lst':cats_lst,
                   'sort_by_prd':sort_by_prd,
                   }
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
        
    elif name_type_search=="Products":
        
        template='boomboom_user/product_list.html' 
        page_template='boomboom_user/next_product_list.html'
        
        brand_list = Brand.objects.all()
        cats_lst = Category.objects.all()
        
        search_result_all = Products.objects.filter(Q(Product_Name__icontains = search_key)).order_by('Product_Name')
        cont_search_result_all = search_result_all.count()
        if cont_search_result_all==0:
            no_result = True
        
        context = {
            'data':search_result_all,
            'page_template': page_template,
            'sort': 'Product Name: A to Z',
            'name_type_search':name_type_search,
            'search_key':search_key,
            'cont_search_result_all':cont_search_result_all,
            'no_result':no_result,
            'search_result_all':search_result_all,
            'brand_list':brand_list,
            'cats_lst':cats_lst,
            'sort_by_prd':sort_by_prd,
        }
    
        if request.is_ajax():
            template = page_template
        return render(request, template, context)
    
    
    

    
    
    
def wishlist(request):
    user = request.user
    
    wishlist_prds = Products.objects.filter(product_wishlist=user)
    context = {
        'wishlist_prds':wishlist_prds,
    }
    
    return render(request, 'boomboom_user/wishlist.html', context)



def campaign_wishlist(request):
    user = request.user
    
    wishlist_cam_prds = campaign_product_table.objects.filter(wishlist = user)
    
    context = {
        'wishlist_cam_prds':wishlist_cam_prds,
    }
    
    return render(request, 'boomboom_user/wishlist_cam_prds.html', context)
    
    
    
@csrf_exempt    
def add_campaign_product_wishlist(request):
    product_id = request.POST.get('product_id')
    get_campgn_prd = campaign_product_table.objects.get(slug=product_id)
    
    user=request.user
    
    get_campgn_prd.wishlist.add(user)
    
    return HttpResponse(True)



    
@csrf_exempt    
def remove_campaign_product_wishlist(request):
    product_id = request.POST.get('product_id')
    get_campgn_prd = campaign_product_table.objects.get(slug=product_id)
    
    user=request.user
    
    get_campgn_prd.wishlist.remove(user)
    
    return HttpResponse(True)
    
    
    
    
    
    
    
@csrf_exempt    
def add_reguler_product_wishlist(request):
    product_id = request.POST.get('product_id')
    get_prd = Products.objects.get(slug=product_id)
    
    user=request.user
    
    get_prd.product_wishlist.add(user)
    
    return HttpResponse(True)



    
@csrf_exempt    
def remove_reguler_product_wishlist(request):
    product_id = request.POST.get('product_id')
    get_prd = Products.objects.get(slug=product_id)
    
    user=request.user
    
    get_prd.product_wishlist.remove(user)
    
    return HttpResponse(True)




@csrf_exempt
def check_and_send_otp(request):
    varforgot_pass_num = request.POST.get('varforgot_pass_num')
    print(varforgot_pass_num)

    check_num = User.objects.filter(username=varforgot_pass_num)
    print(check_num)
    if check_num:
        # make random order ID
        otp_num = random.randint(11111, 99999)

        otp_num_str = str(otp_num)
        print(otp_num_str)

        customer_phn_numwith88 = "88" + varforgot_pass_num

        # sms sending
        conn = ht.HTTPSConnection("smsplus.sslwireless.com")
        headers = {'Content-type': 'application/json'}

        payload = {
            "api_token": "744d2817-6c3b-4a70-a91e-e3f9ee5cf1b",
            "sid": "BOOMBOOMNONAPI",
            "sms": otp_num_str + " is Your Reset Password OTP from boomboom",
            "msisdn": customer_phn_numwith88,
            "csms_id": "123456"
        }

        payload_json = json.dumps(payload)
        conn.request("POST", "/api/v3/send-sms", payload_json, headers)

        res = conn.getresponse()
        data = res.read()

        return HttpResponse(otp_num)
    else:
        return HttpResponse(False)


@csrf_exempt
def change_password_confirm(request):
    phn_number = request.POST.get('phn_number')
    password_forgot = request.POST.get('password_forgot')
    print(phn_number, password_forgot)


    get_customer = User.objects.get(username=phn_number)
    get_customer.password = make_password(password_forgot)
    get_customer.save()
    print('get_user.password')
    print(get_customer.password)


    # logged in
    user = authenticate(request, username=get_customer.username, password=password_forgot)
    if user is not None:
        login(request, user)
    return HttpResponse(True)