from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Customer_delivery_information, Order_Table, Order_Table_2
from app_1.models import Products, campaign_table, campaign_product_table, attribute_connect_with_product
from django.http import HttpResponse
import random
from django.core.paginator import Paginator, EmptyPage
# Create your views here.
import json
from sslcommerz_lib import SSLCOMMERZ


def checkout_func(request):
    return render(request, 'boomboom_user/checkout.html')


@csrf_exempt
def save_customer_delivery_info(request):
    customer_first_name = request.POST.get('customer_first_name')
    customer_last_name = request.POST.get('customer_last_name')
    customer_Street_Address = request.POST.get('customer_Street_Address')
    customer_Town_City = request.POST.get('customer_Town_City')
    customer_District = request.POST.get('customer_District')
    customer_Post_Code = request.POST.get('customer_Post_Code')
    customer_Phone_Number = request.POST.get('customer_Phone_Number')
    customer_Email_Address =request.POST.get('customer_Email_Address')

    print(customer_first_name, customer_last_name, customer_Street_Address, customer_Town_City, customer_District, customer_Post_Code, customer_Phone_Number, customer_Email_Address)

    var_customer_info = Customer_delivery_information(Customer=request.user, First_Name=customer_first_name, Last_Name=customer_last_name, Street_Address=customer_Street_Address, Town_City=customer_Town_City, District=customer_District, Post_Code=customer_Post_Code, Phone_Number=customer_Phone_Number, Email_Address=customer_Email_Address)

    var_customer_info.save()

    print(var_customer_info.id)
    customer_info_id = var_customer_info.id

    return HttpResponse(customer_info_id)




@csrf_exempt
def get_last_oder_ID(request):
    print('hiijhihiihihhhs')
    customer_deli_info_id = request.POST.get('customer_deli_info_id')
    order_delivery_place = request.POST.get('order_delivery_place')
    order_delivery_option = request.POST.get('order_delivery_option')
    get_grand_total2 = request.POST.get('vget_Sub_total2')
    vshow_subtotalss2 = request.POST.get('vshow_subtotalss2')
    vshow_delivery_charge2 = request.POST.get('vshow_delivery_charge2')

    varvar_odr_typ_slug = request.POST.get('var_odr_typ_slug')

    if campaign_table.objects.filter(campaign_slug=varvar_odr_typ_slug):
        get_campgn = campaign_table.objects.get(campaign_slug=varvar_odr_typ_slug)
        varorder_cam_or_reguler_status = 'Campaign'
    else:
        get_campgn = None
        varorder_cam_or_reguler_status = 'Reguler'

    print(get_grand_total2, vshow_subtotalss2, vshow_delivery_charge2)
    print('ss')
    print(get_grand_total2)
    print('ssrfrf')
    print(vshow_subtotalss2)
    print('saas')
    print(vshow_delivery_charge2)

    print('checl_plaxce')

    if order_delivery_place == "0":
        order_delivery_place_t = "Pickup From BoomBoom Office"
    else:
        order_delivery_place_t = "Delivery"

    # get the customer delivery information
    get_Customer_delivery_infor = Customer_delivery_information.objects.get(id=customer_deli_info_id)

    last_one = Order_Table.objects.all().order_by('-Order_Id')[:1]
    # last_one = Order_Table.objects.last()
    if last_one:
        for i in last_one:
            print(i.Order_Id)
            last_ordr_id = i.Order_Id
            new_order_id = int(last_ordr_id) + 1
    else:
        new_order_id = 30000

    print('monna id')
    print(new_order_id)

    var_Order_Table = Order_Table(Customer=request.user, Customer_delivery_information=get_Customer_delivery_infor, Order_Id = new_order_id, SubTotal_Price=int(get_grand_total2), Delivery_Charge=int(vshow_delivery_charge2), GrandTotal_Price=int(vshow_subtotalss2), Order_Status='Pending payment', Shopping=order_delivery_place_t, Payment_method=order_delivery_option, Campaign_Status=varorder_cam_or_reguler_status, Order_Campaign=get_campgn)

    var_Order_Table.save()
    return HttpResponse(var_Order_Table.id)


@csrf_exempt
def save_all_orders_one_by_one(request):
    print('sssss')
    order_product_id = request.POST.get('order_product_id')
    order_product_qty = request.POST.get('order_product_qty')
    order_single_price = request.POST.get('order_single_price')
    order_sub_single_price = request.POST.get('order_sub_single_price')

    latest_ord_numID = request.POST.get('latest_ord_numID')
    get_ordr = Order_Table.objects.get(id=latest_ord_numID)

    var_campgn_slug = request.POST.get('campgn_slug')

    if campaign_table.objects.filter(campaign_slug=var_campgn_slug):
        get_campgn = campaign_table.objects.get(campaign_slug=var_campgn_slug)

    else:
        get_campgn = None


    # get the product
    get_the_Product = Products.objects.get(slug=order_product_id)
    vendor_get = get_the_Product.Vendors
    print(get_the_Product)

    var_Order_Table2 = Order_Table_2(Order_Id=get_ordr, Product=get_the_Product, Vendors=vendor_get, then_price=order_single_price, Quantity=int(order_product_qty), SubTotal_Price=order_sub_single_price, Campaign=get_campgn)
    var_Order_Table2.save()

    # saving product selling qty and price
    prod_sell_qty = get_the_Product.total_quantity_of_sell_product
    prod_sell_money = get_the_Product.total_money_of_sell_product

    get_the_Product.total_quantity_of_sell_product=prod_sell_qty+int(order_product_qty)
    get_the_Product.total_money_of_sell_product=prod_sell_money+int(order_sub_single_price)
    get_the_Product.save()

    # saving category selling qty and price
    prod_cat = get_the_Product.Category
    cat_sell_qty = prod_cat.total_quantity_of_sell
    cat_sell_money = prod_cat.total_money_of_sell

    prod_cat.total_money_of_sell=cat_sell_money+int(order_sub_single_price)
    prod_cat.total_quantity_of_sell=cat_sell_qty+int(order_product_qty)
    prod_cat.save()

    return HttpResponse(True)



@csrf_exempt
def save_all_campaign_orders_one_by_one(request):
    camorder_product_id = request.POST.get('order_product_id')
    odr_campaign_slug = request.POST.get('odr_campaign_slug')
    order_product_qty = request.POST.get('order_product_qty')
    order_single_price = request.POST.get('order_single_price')
    order_sub_single_price = request.POST.get('order_sub_single_price')
    latest_ord_numID = request.POST.get('latest_ord_numID')


    get_ordr = Order_Table.objects.get(id=latest_ord_numID)

    campgn_table_get = campaign_table.objects.get(campaign_slug=odr_campaign_slug)

    get_campn_prodt_tbl = campaign_product_table.objects.get(slug=camorder_product_id)

    order_product = get_campn_prodt_tbl.product.slug

    # get the product
    get_the_Product = Products.objects.get(slug=order_product)
    vendor_get = get_the_Product.Vendors
    print(get_the_Product)

    var_Order_Table2 = Order_Table_2(Order_Id=get_ordr, Product=get_the_Product, Vendors=vendor_get, then_price=order_single_price, Quantity=int(order_product_qty), SubTotal_Price=order_sub_single_price, Campaign=campgn_table_get)
    var_Order_Table2.save()


    # saving product selling qty and price
    prod_sell_qty = get_the_Product.total_quantity_of_sell_product
    prod_sell_money = get_the_Product.total_money_of_sell_product

    get_the_Product.total_quantity_of_sell_product=prod_sell_qty+int(order_product_qty)
    get_the_Product.total_money_of_sell_product=prod_sell_money+int(order_sub_single_price)
    get_the_Product.save()

    # saving category selling qty and price
    prod_cat = get_the_Product.Category
    cat_sell_qty = prod_cat.total_quantity_of_sell
    cat_sell_money = prod_cat.total_money_of_sell

    prod_cat.total_money_of_sell=cat_sell_money+int(order_sub_single_price)
    prod_cat.total_quantity_of_sell=cat_sell_qty+int(order_product_qty)
    prod_cat.save()

    return HttpResponse(True)





def order_save_with_all_info(request):
    customer_deli_info_id1 = request.POST.get('customer_deli_info_id')
    customer_deli_info_id = json.loads(customer_deli_info_id1)
    order_delivery_place1 = request.POST.get('order_delivery_place')
    order_delivery_place = json.loads(order_delivery_place1)
    order_delivery_option1 = request.POST.get('order_delivery_option')
    order_delivery_option = json.loads(order_delivery_option1)


    # get_grand_total21 = request.POST.get('vget_Sub_total2')
    # get_grand_total2 = json.loads(get_grand_total21)
    # vshow_subtotalss21 = request.POST.get('vshow_subtotalss2')
    # vshow_subtotalss2 = json.loads(vshow_subtotalss21)
    # vshow_delivery_charge21 = request.POST.get('vshow_delivery_charge2')
    # vshow_delivery_charge2 = json.loads(vshow_delivery_charge21)


    lst_cam_sts1 = request.POST.get('lst_cam_sts')
    lst_cam_sts = json.loads(lst_cam_sts1)
    product_cart1 = request.POST.get('product_cart')
    product_cart = json.loads(product_cart1)

    name_odr_note_txtara = request.POST.get('name_order_note_textarea')
    name_odr_note_txtara2 = json.loads(name_odr_note_txtara)

    lst_cam_sub_delivery_grand2 = request.POST.get('lst_cam_sub_delivery_grand')
    lst_cam_sub_delivery_grand = json.loads(lst_cam_sub_delivery_grand2)
    print(lst_cam_sub_delivery_grand)

    input_show_subtotalss = request.POST.get('input_show_subtotalss')
    input_show_subtotalss2 = json.loads(input_show_subtotalss)

    input_total_to_pay_price = request.POST.get('input_total_to_pay_price')
    input_total_to_pay_price2 = json.loads(input_total_to_pay_price)

    input_total_due_price = request.POST.get('input_total_due_price')
    input_total_due_price2 = json.loads(input_total_due_price)

    input_payment_type = request.POST.get('input_payment_type')
    input_payment_type2 = json.loads(input_payment_type)

    print('input_show_subtotalss2, input_total_to_pay_price2, input_total_due_price2, input_payment_type2')
    print(input_show_subtotalss2, input_total_to_pay_price2, input_total_due_price2, input_payment_type2)


    lst_ordr_ids = []

    for cam_name in lst_cam_sts:
        print(cam_name)

        for i in lst_cam_sub_delivery_grand:
            print(i)
            print(i[0])

            if i[0]==cam_name:
                print('ho')

                get_grand_total2=i[1]
                vshow_delivery_charge2=i[2]
                vshow_subtotalss2=i[3]

                partial_payment_price = i[4]
                due_price = i[5]

                print(get_grand_total2, vshow_delivery_charge2, vshow_subtotalss2, partial_payment_price, due_price)


        if campaign_table.objects.filter(campaign_name=cam_name):
            varorder_cam_or_reguler_status = 'Campaign'
            if campaign_table.objects.filter(campaign_name=cam_name, finish_campaign=False):
                get_campgn = campaign_table.objects.get(campaign_name=cam_name, finish_campaign=False)
            else:
                return redirect('Offer_not_available')
        else:
            get_campgn = None
            varorder_cam_or_reguler_status = 'Reguler'


        print(get_campgn, varorder_cam_or_reguler_status)


        if order_delivery_place == "0":
            order_delivery_place_t = "Pickup From BoomBoom Office"
        else:
            order_delivery_place_t = "Delivery"

        print(order_delivery_place_t)

        # get the customer delivery information
        get_Customer_delivery_infor = Customer_delivery_information.objects.get(id=customer_deli_info_id)
        print(get_Customer_delivery_infor)


        last_one = Order_Table.objects.all().order_by('-Order_Id')[:1]
        # last_one = Order_Table.objects.last()
        if last_one:
            for i in last_one:
                print(i.Order_Id)
                last_ordr_id = i.Order_Id
                new_order_id = int(last_ordr_id) + 1
        else:
            new_order_id = 30000

        print('monna id')
        print(new_order_id)

        print('checkout errors check')
        print(get_Customer_delivery_infor)
        print(new_order_id)
        print(get_grand_total2)
        print(vshow_delivery_charge2)
        print(vshow_subtotalss2)
        print(partial_payment_price)
        print(due_price)
        print(order_delivery_place_t)
        print(order_delivery_option)
        print(varorder_cam_or_reguler_status)
        print(get_campgn)

        var_Order_Table = Order_Table(Customer=request.user, Customer_delivery_information=get_Customer_delivery_infor, Order_Id=new_order_id, SubTotal_Price=get_grand_total2, Delivery_Charge=vshow_delivery_charge2, GrandTotal_Price=vshow_subtotalss2, Partial_Price=partial_payment_price , Due_price=due_price , Order_Status='Pending payment', Payment_Type=input_payment_type2, Shopping=order_delivery_place_t, Payment_method=order_delivery_option, Campaign_Status=varorder_cam_or_reguler_status, Order_Campaign=get_campgn, Order_Note=name_odr_note_txtara2)

        var_Order_Table.save()

        print(var_Order_Table.id)

        lst_ordr_ids.append(var_Order_Table.Order_Id)



        for item in product_cart:
            print(item)
            print(cam_name)


            if item[5] == cam_name:
                print(cam_name)

                order_product_id = item[4]
                order_product_qty = item[0]
                order_single_price = item[2]
                order_sub_single_price = int(order_product_qty)*int(order_single_price)


                print(order_product_id, order_product_qty, order_single_price, order_sub_single_price)

                attr_id = item[9]
                if attr_id==0:
                    get_attrbt=None
                else:
                    get_attrbt = attribute_connect_with_product.objects.get(id=attr_id)

                latest_ord_numID = var_Order_Table.id
                get_ordr = Order_Table.objects.get(id=latest_ord_numID)

                print(get_ordr)


                if campaign_table.objects.filter(campaign_name=cam_name):
                    get_campgn = campaign_table.objects.get(campaign_name=cam_name)

                    get_campn_prodt_tbl = campaign_product_table.objects.get(slug=order_product_id)
                    print('get_campn_prodt_tbl')
                    print(get_campn_prodt_tbl)
                    get_the_Product = get_campn_prodt_tbl.product
                    print(get_the_Product)
                    print('get_the_Product')
                else:
                    get_campgn = None

                    get_the_Product = Products.objects.get(slug=order_product_id)
                    print(get_the_Product)
                    print('get_the_Product')


                print(get_campgn)

                # get the product
                print(order_product_id)



                vendor_get = get_the_Product.Vendors
                if vendor_get:
                    pass
                elif vendor_get=='' or vendor_get=='None':
                    vendor_get== None


                print(vendor_get)
                print('error check koretesi')
                print('get_ordr')
                print(get_ordr)
                print('get_the_Product')
                print(get_the_Product)
                print('get_the_Product.Category')
                print(get_the_Product.Category)
                print('vendor_get')
                print(vendor_get)


                print('order_single_price')
                print(order_single_price)
                print('order_product_qty')
                print(order_product_qty)
                print('order_sub_single_price')
                print(order_sub_single_price)
                print('get_campgn')
                print(get_campgn)
                print('get_attrbt')
                print(get_attrbt)


                if get_attrbt:

                    print('get_attrbt.MRP_Price')
                    print(get_attrbt.MRP_Price)
                    print('get_attrbt.Cost_Price')
                    print(get_attrbt.Cost_Price)

                    if_cost_price_blank = get_attrbt.Cost_Price
                    if if_cost_price_blank:
                        pass
                    elif if_cost_price_blank=='' or if_cost_price_blank=='None':
                        if_cost_price_blank=None

                    var_Order_Table2 = Order_Table_2(Order_Id=get_ordr, Product=get_the_Product,
                                                     Category=get_the_Product.Category, Vendors=vendor_get,
                                                     MRP_price=get_attrbt.MRP_Price, Cost_price=if_cost_price_blank, then_price=order_single_price, Quantity=int(order_product_qty),
                                                     SubTotal_Price=order_sub_single_price, Campaign=get_campgn,
                                                     Attribute=get_attrbt)
                    var_Order_Table2.save()
                else:

                    var_cst_prc = get_the_Product.Cost_Price
                    if var_cst_prc:
                        pass
                    elif var_cst_prc == '' or var_cst_prc=='None':
                        var_cst_prc=None


                    var_Order_Table2 = Order_Table_2(Order_Id=get_ordr, Product=get_the_Product, Category=get_the_Product.Category, Vendors=vendor_get,
                                                     MRP_price=get_the_Product.MRP_Price, Cost_price=var_cst_prc, then_price=order_single_price, Quantity=int(order_product_qty),
                                                     SubTotal_Price=order_sub_single_price, Campaign=get_campgn, Attribute=get_attrbt)
                    var_Order_Table2.save()

                # saving product selling qty and price
                prod_sell_qty = get_the_Product.total_quantity_of_sell_product
                prod_sell_money = get_the_Product.total_money_of_sell_product

                if prod_sell_qty==None:
                    prod_sell_qty=0

                if prod_sell_money==None:
                    prod_sell_money=0

                get_the_Product.total_quantity_of_sell_product = prod_sell_qty + int(order_product_qty)
                get_the_Product.total_money_of_sell_product = prod_sell_money + int(order_sub_single_price)
                get_the_Product.save()

                # saving category selling qty and price
                prod_cat = get_the_Product.Category
                cat_sell_qty = prod_cat.total_quantity_of_sell
                cat_sell_money = prod_cat.total_money_of_sell

                if cat_sell_qty==None:
                    cat_sell_qty=0

                if cat_sell_money==None:
                    cat_sell_money=0

                prod_cat.total_money_of_sell = cat_sell_money + int(order_sub_single_price)
                prod_cat.total_quantity_of_sell = cat_sell_qty + int(order_product_qty)
                prod_cat.save()

                if get_campgn:
                    get_campn_prodt_tbl = campaign_product_table.objects.get(slug=order_product_id)

                    cam_total_qty_prod = get_campn_prodt_tbl.total_quantity_of_sell_campaign_product
                    cam_total_money_prod = get_campn_prodt_tbl.total_money_of_sell_campaign_product

                    if cam_total_qty_prod == None:
                        cam_total_qty_prod=0

                    if cam_total_money_prod==None:
                        cam_total_money_prod=0

                    get_campn_prodt_tbl.total_quantity_of_sell_campaign_product = cam_total_qty_prod + int(order_product_qty)
                    get_campn_prodt_tbl.total_money_of_sell_campaign_product = cam_total_money_prod + int(order_sub_single_price)
                    get_campn_prodt_tbl.save()



                    campaign_cat = get_campn_prodt_tbl.category_percentage

                    cam_cat_total_qty = campaign_cat.total_quantity_of_sell_cat_campaign
                    cam_cat_total_money = campaign_cat.total_money_of_sell_cat_campaign

                    if cam_cat_total_qty==None:
                        cam_cat_total_qty=0

                    if cam_cat_total_money==None:
                        cam_cat_total_money=0

                    campaign_cat.total_quantity_of_sell_cat_campaign = cam_cat_total_qty + int(order_product_qty)
                    campaign_cat.total_money_of_sell_cat_campaign = cam_cat_total_money + int(order_sub_single_price)
                    campaign_cat.save()
                else:
                    # saving product selling qty and price
                    prod_sell_qty2 = get_the_Product.total_quantity_of_sell_reguler_product
                    prod_sell_money2 = get_the_Product.total_money_of_sell_reguler_product

                    if prod_sell_qty2==None:
                        prod_sell_qty2=0

                    if prod_sell_money2==None:
                        prod_sell_money2=0

                    get_the_Product.total_quantity_of_sell_reguler_product = prod_sell_qty2 + int(order_product_qty)
                    get_the_Product.total_money_of_sell_reguler_product = prod_sell_money2 + int(order_sub_single_price)
                    get_the_Product.save()

                    # saving category selling qty and price
                    prod_cat = get_the_Product.Category
                    cat_sell_qty2 = prod_cat.total_quantity_of_sell_reguler
                    cat_sell_money2 = prod_cat.total_money_of_sell_reguler

                    if cat_sell_qty2==None:
                        cat_sell_qty2=0

                    if cat_sell_money2==None:
                        cat_sell_money2=0

                    prod_cat.total_money_of_sell_reguler = cat_sell_money2 + int(order_sub_single_price)
                    prod_cat.total_quantity_of_sell_reguler = cat_sell_qty2 + int(order_product_qty)
                    prod_cat.save()

            else:
                print('deferent section')



            # if cam_name==None:
            #     print('no cam')

            #     order_product_id = item[4]
            #     order_product_qty = item[0]
            #     order_single_price = item[2]
            #     order_sub_single_price = int(order_product_qty) * int(order_single_price)

            #     print(order_product_id, order_product_qty, order_single_price, order_sub_single_price)

            #     latest_ord_numID = var_Order_Table.id
            #     get_ordr = Order_Table.objects.get(id=latest_ord_numID)

            #     print(get_ordr)

            #     var_campgn_slug = cam_name
            #     get_campgn = None

            #     print(get_campgn)

            #     # get the product
            #     print(order_product_id)





            #     vendor_get = get_the_Product.Vendors
            #     print(vendor_get)

            #     var_Order_Table2 = Order_Table_2(Order_Id=get_ordr, Product=get_the_Product, Vendors=vendor_get,
            #                                      then_price=order_single_price, Quantity=int(order_product_qty),
            #                                      SubTotal_Price=order_sub_single_price, Campaign=get_campgn)
            #     var_Order_Table2.save()

            #     # saving product selling qty and price
            #     prod_sell_qty = get_the_Product.total_quantity_of_sell_product
            #     prod_sell_money = get_the_Product.total_money_of_sell_product

            #     get_the_Product.total_quantity_of_sell_product = prod_sell_qty + int(order_product_qty)
            #     get_the_Product.total_money_of_sell_product = prod_sell_money + int(order_sub_single_price)
            #     get_the_Product.save()

            #     # saving category selling qty and price
            #     prod_cat = get_the_Product.Category
            #     cat_sell_qty = prod_cat.total_quantity_of_sell
            #     cat_sell_money = prod_cat.total_money_of_sell

            #     prod_cat.total_money_of_sell = cat_sell_money + int(order_sub_single_price)
            #     prod_cat.total_quantity_of_sell = cat_sell_qty + int(order_product_qty)
            #     prod_cat.save()

            # else:
            #     print('cam')


    print(lst_ordr_ids)

    lst_ordr_ids2 = ""
    for i in lst_ordr_ids:
        if lst_ordr_ids2=="":
            lst_ordr_ids2 = str(i)
        else:
            lst_ordr_ids2 = lst_ordr_ids2+ ', ' + str(i)

    print(lst_ordr_ids2)

    get_Customer_delivery_infor = Customer_delivery_information.objects.get(id=customer_deli_info_id)


    print(order_delivery_option)

    if order_delivery_option == 'Pay Online With SSLCommerz(Credit/Debit Card/MobileBanking/NetBanking/bKash)':

        settings = {'store_id': 'bbtec614580491067c', 'store_pass': 'bbtec614580491067c@ssl', 'issandbox': True}
        sslcommez = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = input_total_to_pay_price2
        post_body['currency'] = "BDT"
        post_body['tran_id'] = lst_ordr_ids
        post_body['success_url'] = "http://127.0.0.1:8000/payment-successful"
        post_body['fail_url'] = "http://127.0.0.1:8000/payment-failed"
        post_body['cancel_url'] = "http://127.0.0.1:8000/payment-cancelled"
        post_body['emi_option'] = 0
        post_body['cus_name'] = get_Customer_delivery_infor.First_Name + get_Customer_delivery_infor.Last_Name
        post_body['cus_email'] = get_Customer_delivery_infor.Email_Address
        post_body['cus_phone'] = get_Customer_delivery_infor.Phone_Number
        post_body['cus_add1'] = get_Customer_delivery_infor.Street_Address + ', '+ get_Customer_delivery_infor.Town_City
        post_body['cus_city'] = get_Customer_delivery_infor.District
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = "Master Card"
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = sslcommez.createSession(post_body)
        print(response)
        return redirect(response['GatewayPageURL'])

    elif order_delivery_option == 'COD':
        return redirect('customer-dashboard')

    elif order_delivery_option == 'Bank Deposit':
        return redirect('customer-dashboard')




def Offer_not_available(request):
    return render(request, 'boomboom_user/Offer_not_available.html')