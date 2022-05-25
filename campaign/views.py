from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import add_campaign, edit_campaign
from django.contrib import messages
from app_1.models import campaign_table, campaign_categories_percentage, campaign_product_attribute, attribute_connect_with_product
from app_1.models import campaign_product_table
from app_1.models import Category, Products
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



def create_campaign(request):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        all_campaign_list = campaign_table.objects.filter(finish_campaign=False).order_by('-id')
        check_current_campgn = campaign_table.objects.filter(finish_campaign=False)
        context = {'all_campaign_list':all_campaign_list, 'check_current_campgn':check_current_campgn}
        return render(request, 'campaign/create_campaign.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
def campaign_details(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        get_campaign = campaign_table.objects.get(id=pk)
        campaign_form = add_campaign(instance=get_campaign)
        
        get_cam_cat_percentage = campaign_categories_percentage.objects.filter(campaign=get_campaign)
        
        
        if request.method == "POST":
            campaign_form = add_campaign(request.POST, request.FILES, instance=get_campaign)
            if campaign_form.is_valid():
                campaign_form.save()
                messages.success(request,"Successfully Edited !!")
                return redirect('create_campaign')
        
        context = {'get_campaign':get_campaign, 'get_cam_cat_percentage':get_cam_cat_percentage, 'campaign_form':campaign_form}
        return render(request, 'campaign/campaign_details.html', context)
    else:
        return redirect('deshboard_login')


    
def add_campaign_name(request):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        campaign_form = add_campaign()
        
        if request.method == "POST":
            campaign_form = add_campaign(request.POST, request.FILES)
            if campaign_form.is_valid():
                cam = campaign_form.save()
                
                messages.success(request,"Added New Campaign Name !!")
                return redirect('add_category_percentage', cam.id)
    
        context = {'campaign_form':campaign_form}
        return render(request, 'campaign/add_campaign_name.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
def add_category_percentage(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        the_campaign = campaign_table.objects.get(id=pk)
        all_Category_list = Category.objects.all()
        
        context = {'the_campaign':the_campaign,'all_Category_list':all_Category_list}
        return render(request, 'campaign/add_category_percentage.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
    
@csrf_exempt
def save_categories_percentages(request):
    cat_id = request.POST.get('cat_id')
    get_cam_id = request.POST.get('get_cam_id')
    get_percentage = request.POST.get('get_percentage')
    
    get_cat = Category.objects.get(id=cat_id)
    get_camp = campaign_table.objects.get(id=get_cam_id)
    
    table_cam_cat_percent = campaign_categories_percentage(campaign=get_camp, Category=get_cat, percentage=get_percentage)
    table_cam_cat_percent.save()
    
    filter_cat_prod = Products.objects.filter(Category=get_cat)
    
    for i in filter_cat_prod:
        i.campaign_percentage = get_percentage
        i.save()
    
    return HttpResponse(True)
    
    
    
    
    
@csrf_exempt
def save_blank_categories_percentages(request):
    cat_id = request.POST.get('cat_id')
    get_cam_id = request.POST.get('get_cam_id')
    # get_percentage = request.POST.get('get_percentage')
    
    
    get_cat = Category.objects.get(id=cat_id)
    get_camp = campaign_table.objects.get(id=get_cam_id)
    
    table_cam_cat_percent = campaign_categories_percentage(campaign=get_camp, Category=get_cat)
    table_cam_cat_percent.save()
    
    return HttpResponse(True)
    
    
    
    
@csrf_exempt
def edit_categories_percentages(request):
    cat_id = request.POST.get('cat_id')
    get_campgn_cat_prctge = campaign_categories_percentage.objects.get(id=cat_id)
    get_percentage = request.POST.get('get_percentage')
    
    if get_percentage=="None" or get_percentage=="":
        get_campgn_cat_prctge.percentage = None
    else:
        get_campgn_cat_prctge.percentage = get_percentage
        
    get_campgn_cat_prctge.save()
    
    return HttpResponse(True)    
    
    
def products_campaign(request):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        # get_cam = campaign_table.objects.get(id=pk)
        # get_cat_in_cam = campaign_categories_percentage.objects.filter(campaign=get_cam)
        all_campaign_list = campaign_table.objects.filter(finish_campaign=False).order_by('-id')
        context = {'all_campaign_list':all_campaign_list}
        return render(request, 'campaign/products_campaign.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
def cam_cat(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        get_camp = campaign_table.objects.get(id=pk)
        filter_cats_by_cam = campaign_categories_percentage.objects.filter(campaign=get_camp, percentage__isnull=False)
        context={'get_camp':get_camp, 'filter_cats_by_cam':filter_cats_by_cam}
        return render(request, 'campaign/cam_cat.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
def add_products_to_cam(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        get_cat_by_cam = campaign_categories_percentage.objects.get(id=pk)
        
        cat = get_cat_by_cam.Category
        
        filter_Products_cat = Products.objects.filter(Category=cat)
        cat_prod_count = filter_Products_cat.count()
        
        # filter_Table_prod_cam = Table_products_campaign.objects.filter(category_percentage=get_cat_by_cam)
        # if filter_Table_prod_cam:
        #     get_Table_prod_cam = Table_products_campaign.objects.get(category_percentage=get_cat_by_cam)
        # else:
        #     get_Table_prod_cam = None
            
        check_campaign_cat = campaign_product_table.objects.filter(category_percentage=get_cat_by_cam)
        
        context={'get_cat_by_cam':get_cat_by_cam, 'filter_Products_cat':filter_Products_cat, 'cat_prod_count':cat_prod_count, 'check_campaign_cat':check_campaign_cat}
        return render(request, 'campaign/add_products_to_cam.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
@csrf_exempt
def save_product_campaign(request):
    prod_uid = request.POST.get('prod_uid')
    get_prod = Products.objects.get(slug=prod_uid)
    
    product_mrp_price = get_prod.MRP_Price
    
    
    # make product add campaign
    # get_prod.add_item_campaign=True
    # get_prod.save()
    
    
    get_cat_by_cam_id = request.POST.get('get_cat_by_cam_id')
    get_cat_by_camp = campaign_categories_percentage.objects.get(id=get_cat_by_cam_id)
    
    prod_percntg = get_cat_by_camp.percentage
    
    campgn_price = product_mrp_price-product_mrp_price*prod_percntg/100
    
    
    
    campign_prod_tbl = campaign_product_table(
        category_percentage = get_cat_by_camp,
        campaign=get_cat_by_camp.campaign,
        product = get_prod,
        add_item_campaign = True,
        campaign_percentage = prod_percntg,
        campaign_price = campgn_price
        )
    campign_prod_tbl.save()
    
    
    # filter_produc_camp = Table_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    
    # if filter_produc_camp:
    #     get_produc_camp = Table_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.products.add(get_prod)
    
    # else:
    #     var_products_camp = Table_products_campaign(category_percentage=get_cat_by_camp)
    #     var_products_camp.save()
        
    #     var_products_camp.products.add(get_prod)
    
    return HttpResponse(True)
    
    
    
@csrf_exempt
def save_unselected_product_campaign(request):
    unselected_prod_uid = request.POST.get('unselected_prod_uid')
    get_prod = Products.objects.get(slug=unselected_prod_uid)
    
    product_mrp_price = get_prod.MRP_Price
    
    # get_prod.add_item_campaign=False
    # get_prod.save()
    
    get_cat_by_cam_id = request.POST.get('get_cat_by_cam_id')
    get_cat_by_camp = campaign_categories_percentage.objects.get(id=get_cat_by_cam_id)
    
    prod_percntg = get_cat_by_camp.percentage
    
    campgn_price = product_mrp_price-product_mrp_price*prod_percntg/100
    
    
    campign_prod_tbl = campaign_product_table(
        category_percentage = get_cat_by_camp,
        campaign=get_cat_by_camp.campaign,
        product = get_prod,
        add_item_campaign = False,
        campaign_percentage = prod_percntg,
        campaign_price = campgn_price
        )
    campign_prod_tbl.save()
    
    
    # filter_produc_camp = Table_Unselected_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    
    # if filter_produc_camp:
    #     get_produc_camp = Table_Unselected_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.Unselected_products.add(get_prod)
    
    # else:
    #     var_products_camp = Table_Unselected_products_campaign(category_percentage=get_cat_by_camp)
    #     var_products_camp.save()
        
    #     var_products_camp.Unselected_products.add(get_prod)
    
    return HttpResponse(True)
    


    

    

    
    

@csrf_exempt
def remove_products_campaign(request):
    prod_uid = request.POST.get('prod_uid')
    get_prod = campaign_product_table.objects.get(slug=prod_uid)
    
    get_prod.add_item_campaign=False
    get_prod.save()
    
    
    # get_cat_by_cam_id = request.POST.get('get_cat_by_cam_id')
    # get_cat_by_camp = campaign_categories_percentage.objects.get(id=get_cat_by_cam_id)
    
    
    
    # filter_produc_camp = Table_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    
    # if filter_produc_camp:
    #     get_produc_camp = Table_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.products.remove(get_prod)
        
        
        
    # filter_produc_camp = Table_Unselected_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    # if filter_produc_camp:
    #     get_produc_camp = Table_Unselected_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.Unselected_products.add(get_prod)
        
    return HttpResponse(True)
    
    
    
    
@csrf_exempt
def add_availble_products_campaign(request):
    prod_uid = request.POST.get('prod_uid')
    get_prod = campaign_product_table.objects.get(slug=prod_uid)
    
    get_prod.add_item_campaign=True
    get_prod.save()
    
    
    # get_cat_by_cam_id = request.POST.get('get_cat_by_cam_id')
    # get_cat_by_camp = campaign_categories_percentage.objects.get(id=get_cat_by_cam_id)
    
    
    
    # filter_produc_camp = Table_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    
    # if filter_produc_camp:
    #     get_produc_camp = Table_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.products.remove(get_prod)
        
        
        
    # filter_produc_camp = Table_Unselected_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    # if filter_produc_camp:
    #     get_produc_camp = Table_Unselected_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.Unselected_products.add(get_prod)
        
    return HttpResponse(True)
    
    
    
    
def edit_add_products_to_camp(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        get_cat_by_cam = campaign_categories_percentage.objects.get(id=pk)
        
        filtr_campaign_product_tbl = campaign_product_table.objects.filter(category_percentage=get_cat_by_cam)
        
        lst20 = []
        for i in filtr_campaign_product_tbl:
            lst20.append(i.product)
            
        cam_cat_prod = get_cat_by_cam.Category
        
        all_products = Products.objects.filter(Category=cam_cat_prod)
        cnt = 0
        lst30 = []
        for i in all_products:
            if i not in lst20:
                lst30.append(i)
                cnt = cnt + 1
            
        
        # filter_unselected_Table_prod_cam = Table_Unselected_products_campaign.objects.filter(category_percentage=get_cat_by_cam)
        # if filter_unselected_Table_prod_cam:
        #     get_unselected_Table_prod_cam = Table_Unselected_products_campaign.objects.get(category_percentage=get_cat_by_cam)
        # else:
        #     get_unselected_Table_prod_cam = None
        
        context={'get_cat_by_cam':get_cat_by_cam, 'lst30':lst30, 'cnt':cnt}
        return render(request, 'campaign/edit_add_products_to_camp.html', context)
    else:
        return redirect('deshboard_login')
    

    

@csrf_exempt    
def adding_more_products_campaign(request):
    prod_uid = request.POST.get('prod_uid')
    get_prod = Products.objects.get(slug=prod_uid)
    
    
    product_mrp_price = get_prod.MRP_Price
    
    get_cat_by_cam_id = request.POST.get('get_cat_by_cam_id')
    get_cat_by_camp = campaign_categories_percentage.objects.get(id=get_cat_by_cam_id)
    
    prod_percntg = get_cat_by_camp.percentage
    
    campgn_price = product_mrp_price-product_mrp_price*prod_percntg/100
    
    
    
    campign_prod_tbl = campaign_product_table(
        category_percentage = get_cat_by_camp,
        campaign=get_cat_by_camp.campaign,
        product = get_prod,
        add_item_campaign = True,
        campaign_percentage = prod_percntg,
        campaign_price = campgn_price
        )
    campign_prod_tbl.save()
    
    
    # get_prod.add_item_campaign=True
    # get_prod.save()
    
    
    
    # filter_un_produc_camp = Table_Unselected_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    
    # if filter_un_produc_camp:
    #     get_un_produc_camp = Table_Unselected_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_un_produc_camp.Unselected_products.remove(get_prod)
        
        
        
    # filter_produc_camp = Table_products_campaign.objects.filter(category_percentage=get_cat_by_camp)
    # if filter_produc_camp:
    #     get_produc_camp = Table_products_campaign.objects.get(category_percentage=get_cat_by_camp)
    #     get_produc_camp.products.add(get_prod)
        
        
    return HttpResponse(True)
    
    

@csrf_exempt
def campaign_change_status_star(request):
    campaign_product_slug = request.POST.get('campaign_product_slug')
    get_the_prod =campaign_product_table.objects.get(slug=campaign_product_slug)
    get_the_prod.make_campaign_star=True
    get_the_prod.save()
    return HttpResponse(True)


    

@csrf_exempt
def campaign_change_status_home_star(request):
    campaign_product_slug = request.POST.get('campaign_product_slug')
    get_the_prod =campaign_product_table.objects.get(slug=campaign_product_slug)
    get_the_prod.make_index_star=True
    get_the_prod.save()
    return HttpResponse(True)

    
    


@csrf_exempt
def campaign_change_undo_status_star(request):
    campaign_product_slug = request.POST.get('campaign_product_slug')
    get_the_prod =campaign_product_table.objects.get(slug=campaign_product_slug)
    get_the_prod.make_campaign_star=False
    get_the_prod.save()
    return HttpResponse(True)
    
@csrf_exempt
def campaign_change_undo_status_home_star(request):
    campaign_product_slug = request.POST.get('campaign_product_slug')
    get_the_prod =campaign_product_table.objects.get(slug=campaign_product_slug)
    get_the_prod.make_index_star=False
    get_the_prod.save()
    return HttpResponse(True)
    
    
@csrf_exempt
def save_change_percentage_prod(request):
    show_100_loops = request.POST.get('show_100_loops')
    camprod_uid = request.POST.get('camprod_uid')
    
    get_prod = campaign_product_table.objects.get(slug=camprod_uid)
    
    
    mrp_prce_prod = get_prod.product.MRP_Price
    
    
    get_prod.campaign_price = mrp_prce_prod-mrp_prce_prod*int(show_100_loops)/100
    get_prod.campaign_percentage = show_100_loops
    get_prod.save()
    
    return HttpResponse(True)
    
    
    
@csrf_exempt
def save_change_price_prod(request):
    new_cam_price = request.POST.get('new_cam_price')
    camprod_uid = request.POST.get('camprod_uid')
    
    get_prod = campaign_product_table.objects.get(slug=camprod_uid)
    get_prod.campaign_price = int(new_cam_price)
    get_prod.save()
    
    return HttpResponse(True)
    
    
    
def finish_campaign_deshbrd(request):
    get_campaign_id= request.POST.get('get_campaign_id')
    
    all_prodct = Products.objects.all()
    
    for i in all_prodct:
        i.add_item_campaign=False
        i.campaign_percentage=None
        i.save()
    
    get_closing_campaign = campaign_table.objects.get(id=get_campaign_id)
    get_closing_campaign.finish_campaign = True
    get_closing_campaign.save()
    
    return redirect('create_campaign')
    
    
    
    
def summery_campaign(request):
    staff_admin = request.session.get('deshboard_admin_username')
    if staff_admin:
        all_campaign_list = campaign_table.objects.all().order_by('-id')
        context = {'all_campaign_list':all_campaign_list}
        return render(request, 'campaign/summery_campaign.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
def campaign_product_add_attribute(request, pk):
    get_cam_prd = campaign_product_table.objects.get(slug=pk)
    get_prodct = get_cam_prd.product
    
    filter_attr_prd = attribute_connect_with_product.objects.filter(connect_with_product = get_prodct)
    
    if campaign_product_attribute.objects.filter(campaign_product=get_cam_prd):
        pass
    else:
        for i in filter_attr_prd:
            save_cam_prd_attr = campaign_product_attribute(campaign_product=get_cam_prd, attribute=i, Cost_Price=i.Cost_Price, MRP_Price=i.MRP_Price)
            save_cam_prd_attr.save()
    
    prd_att = campaign_product_attribute.objects.filter(campaign_product=get_cam_prd)
    
    context = {'get_cam_prd':get_cam_prd, 'prd_att':prd_att}
    return render(request, 'campaign/campaign_product_add_attribute.html', context)
    
    
@csrf_exempt    
def edit_campaign_product_attr(request):
    id_campaign_product_row = request.POST.get('id_campaign_product_row')
    cam_prod_attr_check_id = request.POST.get('cam_prod_attr_check_id')
    get_discount_price = request.POST.get('get_discount_price')
    
    get_prd_att = campaign_product_attribute.objects.get(id=cam_prod_attr_check_id)
    if get_discount_price == "":
        get_prd_att.Discount_Price=None
    else:
        get_prd_att.Discount_Price=int(get_discount_price)
    get_prd_att.save()
    return HttpResponse(True)
    
    
    
    
    
    
    
    
    