from django.shortcuts import render, HttpResponse, redirect
from . models import vendor_registration_table, vendor_payment_info
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from app_1.forms import s_vendor_edit_product_field
from app_1.models import Products
from checkout.models import Order_Table, Order_Table_2
from django.views.decorators.csrf import csrf_exempt
from app_1.forms import vendor_edit_product_field
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.core.files.storage import FileSystemStorage
import http.client as ht
from app_1.models import Category, Subcategory_1, Subcategory_2
# Create your views here.
import json
from app_1.models import User
import random




def vendor_dashboard_index(request):
    r = request.session.get('vendor_session_phone')
    if r:
        return render(request, 'vendor_templates/vendor_index.html')

    else:
        return redirect('vendor_login')


def vendor_registration(request):
    check_sessin = request.session.get('vendor_session_phone')
    if check_sessin:
        return redirect('vendor_dashboard_index')
    else:
        return render(request, 'vendor_templates/vendor_registration.html')


def vendor_login(request):
    check_sessin = request.session.get('vendor_session_phone')
    if check_sessin:
        return redirect('vendor_dashboard_index')
    else:
        return render(request, 'vendor_templates/vendor_deshboard_login.html')


def cheake_vendor_login_details(request):
    vendor_login_credential_Username = request.POST.get('vendor_login_phone_number')
    vendor_login_credential_Password = request.POST.get('vendor_login_Password')

    vendor_phone_p = vendor_registration_table.objects.filter(vendor_phone_no=vendor_login_credential_Username)
    if vendor_phone_p:
        vendor_pass_p = vendor_registration_table.objects.get(vendor_phone_no=vendor_login_credential_Username)
        vendor_pass_pass =vendor_pass_p.vendor_password
        vendor_pass_vendor_name =vendor_pass_p.vendor_name
        
        check_active = vendor_pass_p.vendor_activation
        
        
        if check_active:
            check_password_after_hash = check_password(vendor_login_credential_Password, vendor_pass_pass)
    
            if check_password_after_hash==True:
                request.session['vendor_session_phone'] = vendor_login_credential_Username
                request.session['vendor_session_pass'] = vendor_login_credential_Password
                request.session['vendor_session_name'] = vendor_pass_vendor_name
                e = request.session.get('vendor_session_phone')
                return redirect('vendor_dashboard_index')
            else:
                messages.error(request, 'your password is wrong!')
        else:
            messages.error(request, 'your Account is not active!')

        # print(request.session.get('vendor_session_phone'))

    else:
        messages.error(request, 'your phone number is wrong!')
    return render(request, 'vendor_templates/vendor_deshboard_login.html')


def vendor_dashboard_logout_func(request):
    request.session.clear()
    return redirect('vendor_login')
    


def save_vendor_registration(request):
    Vendor_registration_Full_Name = request.POST.get('Vendor_registration_Full_Name')
    vendor_registration_Shop_Name = request.POST.get('vendor_registration_Shop_Name')
    vendor_registration_Address = request.POST.get('vendor_registration_Address')
    vendor_registration_Shop_URL = request.POST.get('vendor_registration_Shop_URL')
    vendor_registration_Phone_No = request.POST.get('vendor_registration_Phone_No')
    vendor_otp = request.POST.get('vendor_otp')
    generated_otp_num_str = request.POST.get('generated_otp_num_str')


    print("generated_otp_num_str")
    print(generated_otp_num_str)
    print("vendor_otp")
    print(vendor_otp)

    if vendor_otp==generated_otp_num_str:
        contex = {
            'Vendor_registration_Full_Name': Vendor_registration_Full_Name,
            'vendor_registration_Shop_Name': vendor_registration_Shop_Name,
            'vendor_registration_Address': vendor_registration_Address,
            'vendor_registration_Shop_URL': vendor_registration_Shop_URL,
            'vendor_registration_Phone_No': vendor_registration_Phone_No,
            'vendor_otp': vendor_otp,
            'generated_otp_num_str': generated_otp_num_str,
        }

        return render(request, 'vendor_templates/third_stap_to_save_vendor_registration.html', contex)

    error_massage = "OTP is dosn't match"

    contex_2 = {
        'Vendor_registration_Full_Name': Vendor_registration_Full_Name,
        'vendor_registration_Shop_Name': vendor_registration_Shop_Name,
        'vendor_registration_Shop_URL': vendor_registration_Shop_URL,
        'vendor_registration_Address': vendor_registration_Address,
        'vendor_registration_Phone_No': vendor_registration_Phone_No,
        'generated_otp_num_str': generated_otp_num_str,
        'error_massage':error_massage
    }

    return render(request, 'vendor_templates/cheake_otp_for_vendor_registration.html', contex_2)
    
    
    
    

def cheake_otp_for_vendor_registration(request):
    Vendor_registration_Full_Name = request.POST.get('Vendor_registration_Full_Name')
    vendor_registration_Shop_Name = request.POST.get('vendor_registration_Shop_Name')
    vendor_registration_Shop_URL = request.POST.get('vendor_registration_Shop_URL')
    vendor_registration_Address = request.POST.get('vendor_registration_Address')
    vendor_registration_Phone_No = request.POST.get('vendor_registration_Phone_No')
    vendor_registration_Address = request.POST.get('vendor_registration_Address')

    filter_phone_no = vendor_registration_table.objects.filter(vendor_phone_no=vendor_registration_Phone_No)
    erorr_message = ""

    if filter_phone_no:
        erorr_message = "Phone number is already exist !"

    else:
        import random
        otp_num = random.randint(11111, 99999)
        generated_otp_num_str = str(otp_num)

        print(generated_otp_num_str)

        
        # sms sending
        import http.client as ht
        import json
        
        customer_phn_numwith88 = "88"+str(vendor_registration_Phone_No)
        
        # sms sending
        conn = ht.HTTPSConnection("smsplus.sslwireless.com")
        headers = {'Content-type': 'application/json'}
    
    
        payload = {
        #  "api_token": "744d2817-6c3b-4a70-a91e-e3f9ee5cf1b5",
         "api_token": "744d2817-6c3b-4a70-a91e-e3f9ee5cf1b",
         "sid": "BOOMBOOMNONAPI",
         "sms": generated_otp_num_str + " is Your Signup OTP from boomboom",
         "msisdn": customer_phn_numwith88,
         "csms_id": "123456"
        }
    
        payload_json = json.dumps(payload)
        conn.request("POST", "/api/v3/send-sms", payload_json, headers)
    
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        
 
        contex = {
            'Vendor_registration_Full_Name': Vendor_registration_Full_Name,
            'vendor_registration_Shop_Name': vendor_registration_Shop_Name,
            'vendor_registration_Shop_URL': vendor_registration_Shop_URL,
            'vendor_registration_Address': vendor_registration_Address,
            'vendor_registration_Phone_No': vendor_registration_Phone_No,
            'generated_otp_num_str': generated_otp_num_str,
        }

        return render(request, 'vendor_templates/cheake_otp_for_vendor_registration.html', contex)

    contex_2 = {
        'Vendor_registration_Full_Name': Vendor_registration_Full_Name,
        'vendor_registration_Shop_Name': vendor_registration_Shop_Name,
        'vendor_registration_Shop_URL': vendor_registration_Shop_URL,
        'vendor_registration_Address': vendor_registration_Address,
        'vendor_registration_Phone_No': vendor_registration_Phone_No,

        'erorr_message': erorr_message
    }

    return render(request, 'vendor_templates/vendor_registration.html', contex_2)




def third_stap_to_save_vendor_registration(request):
    Vendor_registration_Full_Name = request.POST.get('Vendor_registration_Full_Name')
    vendor_registration_Shop_Name = request.POST.get('vendor_registration_Shop_Name')
    vendor_registration_Address = request.POST.get('vendor_registration_Address')
    vendor_registration_Shop_URL = request.POST.get('vendor_registration_Shop_URL')
    vendor_shop_logo = request.FILES.get('vendor_shop_logo')
    vendor_shop_Banner = request.FILES.get('vendor_shop_Banner')
    vendor_registration_Phone_No = request.POST.get('vendor_registration_Phone_No')
    vendor_registration_Email = request.POST.get('vendor_registration_Email')
    vendor_registration_Password = request.POST.get('vendor_registration_Password')
    vendor_registration_Retype_Password = request.POST.get('vendor_registration_Retype_Password')
    vendor_otp = request.POST.get('vendor_otp')
    generated_otp_num_str = request.POST.get('generated_otp_num_str')

    choos_get_paymnt_way = request.POST.get('choos_get_paymnt_way')
    ssl_operator_name = request.POST.get('ssl_operator_name')
    ssl_number = request.POST.get('ssl_number')

    bank_nam = request.POST.get('bank_nam')
    bnk_account_nam = request.POST.get('bnk_account_nam')
    bnk_account_number = request.POST.get('bnk_account_number')
    bnk_brnch = request.POST.get('bnk_brnch')
    bnk_rout_num = request.POST.get('bnk_rout_num')

    print(choos_get_paymnt_way)



    erorr_message = ""

    filter_email = vendor_registration_table.objects.filter(vendor_email=vendor_registration_Email)

    if filter_email:
        erorr_message = "email is already exist !"

    elif vendor_registration_Password != vendor_registration_Retype_Password:
        erorr_message = "Password dosn't match !"

    else:
        if vendor_shop_logo:
            print("image 1")
            fss = FileSystemStorage()
            filename = fss.save(vendor_shop_logo.name, vendor_shop_logo)
            url_file = fss.url(filename)
        else:
            url_file = ''

        if vendor_shop_Banner:
            fsss = FileSystemStorage()
            filename2 = fsss.save(vendor_shop_Banner.name, vendor_shop_Banner)
            url_file2 = fsss.url(filename2)
        else:
            url_file2 = ''


        g = make_password(vendor_registration_Password)

        s = vendor_registration_table(vendor_name=Vendor_registration_Full_Name, vendor_shop_name=vendor_registration_Shop_Name, vendor_address = vendor_registration_Address, vendor_shop_url=vendor_registration_Shop_URL, vendor_phone_no= vendor_registration_Phone_No, vendor_email=vendor_registration_Email, vendor_password=g, vendor_shop_logo=url_file, vendor_shop_banner= url_file2)
        s.save()
        success_message = "You are registration is successfully"

        if choos_get_paymnt_way == 'SSLCommerz':
            s_vendr_pay_info = vendor_payment_info(
                Vendor=s,
                vendor_payment_roll=choos_get_paymnt_way,
                SSL_operator=ssl_operator_name,
                SSL_Mobile_Number=ssl_number
            )
            s_vendr_pay_info.save()

        elif choos_get_paymnt_way == 'Bank Deposite':
            s_vendr_pay_info = vendor_payment_info(
                Vendor=s,
                vendor_payment_roll=choos_get_paymnt_way,
                Bank_Name=bank_nam,
                Account_Name=bnk_account_nam,
                Account_Number=bnk_account_number,
                Branch=bnk_brnch,
                Routing_Number=bnk_rout_num
            )
            s_vendr_pay_info.save()

        return render(request, 'vendor_templates/vendor_registration.html', {'success_message': success_message})

    con_dict ={

        'erorr_message':erorr_message,
        'Vendor_registration_Full_Name': Vendor_registration_Full_Name,
        'vendor_registration_Shop_Name': vendor_registration_Shop_Name,
        'vendor_registration_Address': vendor_registration_Address,
        'vendor_registration_Shop_URL': vendor_registration_Shop_URL,
        'vendor_registration_Phone_No': vendor_registration_Phone_No,

        'vendor_registration_Email': vendor_registration_Email,

        'vendor_otp': vendor_otp,
        'generated_otp_num_str': generated_otp_num_str,

    }

    return render(request, 'vendor_templates/third_stap_to_save_vendor_registration.html', con_dict)

 
    

def vendor_Store_details(request):
    r = request.session.get('vendor_session_phone')
    if r:
        vendor_shope_info = vendor_registration_table.objects.get(vendor_phone_no = r)


        return render(request, 'vendor_templates/vendor_Store_details.html', {'vendor_shope_info':vendor_shope_info})
        # return HttpResponse("stor details")

    else:
        return redirect('vendor_login')

def vendor_info_edit(request):
    r = request.session.get('vendor_session_phone')
    if r:
        vendor_shope_info1 = vendor_registration_table.objects.get(vendor_phone_no=r)
        return render(request, 'vendor_templates/vendor_info_edit.html', {'vendor_shope_info1':vendor_shope_info1})
    else:
        return redirect('vendor_login')

def vendor_info_password_edit(request):
    r = request.session.get('vendor_session_phone')
    if r:
        vendor_shope_info1 = vendor_registration_table.objects.get(vendor_phone_no=r)
        return render(request, 'vendor_templates/vendor_info_edit_password.html', {'vendor_shope_info1': vendor_shope_info1})
    else:
        return redirect('vendor_login')



def save_vendor_info_edit(request):
    itt = request.session.get('vendor_session_phone')
    if request.method == "POST":

        if itt:
            e_n = request.POST.get('edited_Vendor_registration_Full_Name')
            e_n_s_n = request.POST.get('edited_vendor_registration_Shop_Name')
            e_n_r_s = request.POST.get('edited_vendor_registration_Shop_URL')
            e_n_r_p = request.POST.get('edited_vendor_registration_Phone_No')
            e_n_r_e = request.POST.get('edited_vendor_registration_Email')
            e_logo = request.FILES.get('edited_vendor_logo')
            e_venner = request.FILES.get('edited_vendor_banner')


            if e_logo:
                print("image 1")
                fss = FileSystemStorage()
                filename = fss.save(e_logo.name, e_logo)
                url_file = fss.url(filename)
            else:
                url_file = ''

            if e_venner:
                fsss = FileSystemStorage()
                filename2 = fsss.save(e_venner.name, e_venner)
                url_file2 = fsss.url(filename2)
            else:
                url_file2 = ''

            t = vendor_registration_table.objects.get(vendor_phone_no = itt)
            t.vendor_name = e_n
            t.vendor_shop_name = e_n_s_n
            t.vendor_shop_url = e_n_r_s
            t.vendor_phone_no = e_n_r_p
            t.vendor_email = e_n_r_e
            t.vendor_shop_logo = url_file
            t.vendor_shop_banner = url_file2
            t.save()
            request.session['vendor_session_phone'] = e_n_r_p
            request.session['vendor_session_name'] = e_n
        return redirect('vendor_Store_details')

    return redirect('vendor_Store_details')

def save_vendor_info_password_edit(request):
    itt = request.session.get('vendor_session_phone')
    erorr_message = ""
    if request.method == "POST":
        if itt:
            edited_pass_of_vendor = request.POST.get('edited_new_vendor_registration_Password')
            edited_Retype_pass_of_vendor = request.POST.get('edited_new_vendor_registration_Retype_Password')

            if edited_pass_of_vendor == edited_Retype_pass_of_vendor:
                t = vendor_registration_table.objects.get(vendor_phone_no=itt)
                t.vendor_password = make_password(edited_pass_of_vendor)
                t.save()

                request.session['vendor_session_pass'] = edited_pass_of_vendor
                return redirect('vendor_Store_details')


            else:

                erorr_message = "Password dosn't match !"
                return render(request, 'vendor_templates/vendor_info_edit_password.html', {'erorr_message': erorr_message})
        return redirect('vendor_Store_details')
    return redirect('vendor_Store_details')


def vendor_dashbord_add_new_products(request):
    f = s_vendor_edit_product_field()
    get_all_categories = Category.objects.all()

    return render(request, 'vendor_templates/vendor_dashbord_add_new_products.html', {'f':f, 'get_all_categories':get_all_categories})

def save_vendor_dashbord_add_new_products(request):
    if request.method == "POST":
        itt = request.session.get('vendor_session_phone')
        if itt:
            yyy = vendor_registration_table.objects.get(vendor_phone_no = itt)

            vendor_Product_name = request.POST.get('vendor_Product_name')
            vendor_SKU = request.POST.get('vendor_SKU')
            vendor_MRP_Price = request.POST.get('vendor_MRP_Price')
            vendor_Discount_Price = request.POST.get('vendor_Discount_Price')
            
            vendor_product_quentity = request.POST.get('vendor_product_quentity')
            vendor_Meta_Title = request.POST.get('vendor_Meta_Title')
            vendor_Meta_Keyword = request.POST.get('vendor_Meta_Keyword')
            vendor_tags_name = request.POST.get('vendor_tags_name')
            vendor_tags_slug = request.POST.get('vendor_tags_slug')
            vendor_Prod_Image = request.FILES.get('vendor_Prod_Image')
            vendor_Product_Image_2 = request.FILES.get('vendor_Product_Image_2')
            vendor_Product_Image_3 = request.FILES.get('vendor_Product_Image_3')
            vendor_Product_Image_4 = request.FILES.get('vendor_Product_Image_4')

            Category_list = request.POST.get('Category_list')
            Subategory_list = request.POST.get('Subategory_list')
            Subategory_list2 = request.POST.get('Subategory_list2')

            if vendor_Prod_Image:
                fs = FileSystemStorage()
                filename = fs.save(vendor_Prod_Image.name, vendor_Prod_Image)
                url_file = fs.url(filename)
            else:
                url_file = ''

            if vendor_Product_Image_2:
                fs = FileSystemStorage()
                filename = fs.save(vendor_Product_Image_2.name, vendor_Product_Image_2)
                url_file2 = fs.url(filename)
            else:
                url_file2 = ''

            if vendor_Product_Image_3:
                fs = FileSystemStorage()
                filename = fs.save(vendor_Product_Image_3.name, vendor_Product_Image_3)
                url_file3 = fs.url(filename)
            else:
                url_file3 = ''

            if vendor_Product_Image_4:
                fs = FileSystemStorage()
                filename = fs.save(vendor_Product_Image_4.name, vendor_Product_Image_4)
                url_file4 = fs.url(filename)
            else:
                url_file4 = ''


            print('Category_list, Subategory_list, Subategory_list2')
            print(Category_list, Subategory_list, Subategory_list2)

            if Category_list == 'None':
                get_row_cat = ""
                get_row_subcat1 = ""
                get_row_subcat2 = ""
            else:
                get_row_cat = Category.objects.get(id=Category_list)
                if Subategory_list == 'None':
                    get_row_subcat1=""
                    get_row_subcat2=""
                else:
                    get_row_subcat1 = Subcategory_1.objects.get(id=Subategory_list)
                    if Subategory_list2 == 'None':
                        get_row_subcat2 = ""
                    else:
                        get_row_subcat2 = Subcategory_2.objects.get(id=Subategory_list2)





            get_data_vendor_forms = s_vendor_edit_product_field(request.POST)
            if get_data_vendor_forms.is_valid():
                
               vendor_other = get_data_vendor_forms.save(commit=False)
               vendor_other.Product_Name = vendor_Product_name
               vendor_other.SKU = vendor_SKU


               if Category_list != 'None':
                   vendor_other.Category = get_row_cat
                   if Subategory_list != 'None':
                       vendor_other.Subcategory_1 = get_row_subcat1
                       if Subategory_list2 != 'None':
                           vendor_other.Subcategory_2 = get_row_subcat2



               vendor_other.MRP_Price = vendor_MRP_Price
               vendor_other.Cost_Price = 0
               vendor_other.Discount_Price = vendor_Discount_Price
               vendor_other.Product_stock_Quantity = vendor_product_quentity
               vendor_other.Vendors = yyy
               
               vendor_other.Meta_Title = vendor_Meta_Title
               vendor_other.Meta_Keyword = vendor_Meta_Keyword
               vendor_other.Product_Image = url_file
               vendor_other.Product_Image2 = url_file2
               vendor_other.Product_Image3 = url_file3
               vendor_other.Product_Image4 = url_file4
               vendor_other.make_star = 'False'
               vendor_other.save()
               return redirect('vendor_dashbord_add_new_products')


            return redirect('vendor_dashbord_add_new_products')
        return redirect('vendor_dashbord_add_new_products')

    return redirect('vendor_dashbord_add_new_products')
    

def vendor_All_Products_show(request):

    itt = request.session.get('vendor_session_phone')
    if itt:
        yyytttt = vendor_registration_table.objects.get(vendor_phone_no = itt)
        gggg  = Products.objects.filter(Vendors=yyytttt)
        
        count_prod = gggg.count()
        
        all_Category = Category.objects.all()

        return render(request, 'vendor_templates/vendor_All_Products_show.html', {'gggg':gggg, 'count_prod':count_prod, 'all_Category':all_Category})

    return redirect('vendor_login')
    
    
def filter_action_vendor(request):
    itt = request.session.get('vendor_session_phone')
    if itt:
        yyy = vendor_registration_table.objects.get(vendor_phone_no = itt)
        
        
        productorder_length_stock_status = request.GET.get('productorder_length_stock_status')
        productorder_length_Category = request.GET.get('productorder_length_Category')

        get_category = Category.objects.get(id=productorder_length_Category)


        all_product_show = Products.objects.filter(Category=get_category).filter(Stock_status=productorder_length_stock_status).filter(Vendors=yyy)
        all_product_qunt = all_product_show.count()
        
        count_prod = all_product_qunt

        all_Category = Category.objects.all()


        context = {'gggg':all_product_show, 'all_Category':all_Category, 'all_product_qunt':all_product_qunt, 'count_prod':count_prod}
        return render(request, 'vendor_templates/vendor_All_Products_show.html', context)
    else:
        return redirect('vendor_login')
    


@csrf_exempt
def move_to_trash_selected_checkbox_vendors(request):
    prod_uid = request.POST.get('prod_uid')
    print(prod_uid)
    get_prd = Products.objects.get(slug=prod_uid)
    print('get_prd')
    print(get_prd)
    get_prd.delete()
    return HttpResponse(True)

    

def vendor_personal_orders(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)

    get_orders_Order_Table_2  = Order_Table_2.objects.filter(Vendors = uuuu)

    Orders = True
    context = {'get_orders_Order_Table_2':get_orders_Order_Table_2, 'Orders':Orders}
    return render(request, 'vendor_templates/single_vendor_orders_show.html', context)
    
    
    

    
    
    
    
    
    
    
    
    
    


def vendor_edited_product_page(request, pk):
    full_edited_row = Products.objects.get(slug=pk)

    product_form = vendor_edit_product_field(instance=full_edited_row)

    u = {"full_edited_row":full_edited_row,
         "product_form":product_form

         }
    return render(request, 'vendor_templates/vendor_edit_product_page.html', u)



def vendor_edit_product_save(request):
    if request.method == "POST":

        p_get_slug = request.POST.get('p_get_slug')

        product_full_row = Products.objects.get(slug=p_get_slug)

        product_form = vendor_edit_product_field(request.POST, instance=product_full_row)
        if product_form.is_valid():
            product_form.save()


        print("i am here")
        # make_feature_product = request.POST.get('make_feature_product')
        # print('make_feature_product')
        # print(make_feature_product)
        save_edited_Product_name = request.POST.get('save_edited_Product_name')
        save_edited_SKU = request.POST.get('save_edited_SKU')
        save_edited_MRP_Price = request.POST.get('save_edited_MRP_Price')
        save_edited_Cost_Price = request.POST.get('save_edited_Cost_Price')
        save_edited_Discount_Price = request.POST.get('save_edited_Discount_Price')
        save_edited_product_quentity = request.POST.get('save_edited_product_quentity')
        
        save_edited_Meta_Title = request.POST.get('save_edited_Meta_Title')
        save_edited_Meta_Keyword = request.POST.get('save_edited_Meta_Keyword')



        save_edited_Prod_Image = request.FILES.get('save_edited_Prod_Image')
        save_edited_Product_Image_2 = request.FILES.get('save_edited_Product_Image_2')
        save_edited_Product_Image_3 = request.FILES.get('save_edited_Product_Image_3')
        save_edited_Product_Image_4 = request.FILES.get('save_edited_Product_Image_4')
        print("printing image")
        print(save_edited_Prod_Image, save_edited_Product_Image_2, save_edited_Product_Image_3, save_edited_Product_Image_4)

        if save_edited_Prod_Image:
            fs = FileSystemStorage()
            filename = fs.save(save_edited_Prod_Image.name, save_edited_Prod_Image)
            save_edited_Prod_Image = fs.url(filename)
            print("printing save_edited_Prod_Image")
            print(save_edited_Prod_Image)

        if save_edited_Prod_Image is None:
            save_edited_Prod_Image = product_full_row.Product_Image



        if save_edited_Product_Image_2:
            fs2 = FileSystemStorage()
            filename2 = fs2.save(save_edited_Product_Image_2.name, save_edited_Product_Image_2)
            save_edited_Product_Image_2 = fs2.url(filename2)
            print("printing save_edited_Product_Image_2")
            print(save_edited_Product_Image_2)

        if save_edited_Product_Image_2 is None:
            save_edited_Product_Image_2 = product_full_row.Product_Image2

        if save_edited_Product_Image_3:
            fs3 = FileSystemStorage()
            filename3 = fs3.save(save_edited_Product_Image_3.name, save_edited_Product_Image_3)
            save_edited_Product_Image_3 = fs3.url(filename3)

        if save_edited_Product_Image_3 is None:
            save_edited_Product_Image_3 = product_full_row.Product_Image3

        if save_edited_Product_Image_4:
            fs4 = FileSystemStorage()
            filename4 = fs4.save(save_edited_Product_Image_4.name, save_edited_Product_Image_4)
            save_edited_Product_Image_4 = fs4.url(filename4)

        if save_edited_Product_Image_4 is None:
            save_edited_Product_Image_4 = product_full_row.Product_Image4



        product_full_row.Product_Name = save_edited_Product_name
        product_full_row.SKU = save_edited_SKU
        product_full_row.Cost_Price = save_edited_Cost_Price
        product_full_row.MRP_Price = save_edited_MRP_Price
        product_full_row.Discount_Price = save_edited_Discount_Price
        
        product_full_row.Meta_Title = save_edited_Meta_Title
        product_full_row.Meta_Keyword = save_edited_Meta_Keyword
        product_full_row.Product_Image = save_edited_Prod_Image
        product_full_row.Product_Image2 = save_edited_Product_Image_2
        product_full_row.Product_Image3 = save_edited_Product_Image_3
        product_full_row.Product_Image4 = save_edited_Product_Image_4
        product_full_row.Product_stock_Quantity = save_edited_product_quentity
        product_full_row.save()


        r = product_full_row.slug
        messages.success(request, 'Save successfully')
    return redirect('vendor_edited_product_page', r)






@csrf_exempt
def get_vendor_pending_payments_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_count_Pending_payment = Order_Table.objects.filter(Order_Status="Pending payment").filter(Vendors=uuuu).count()
    return HttpResponse(get_count_Pending_payment)


@csrf_exempt
def get_vendor_processing_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_ct_processing_payment = Order_Table.objects.filter(Order_Status="Processing").filter(Vendors=uuuu).count()
    return HttpResponse(get_ct_processing_payment)



@csrf_exempt
def get_vendor_complete_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_cont_complete_payment = Order_Table.objects.filter(Order_Status="Completed").filter(Vendors=uuuu).count()
    return HttpResponse(get_cont_complete_payment)


@csrf_exempt
def get_vendor_cencel_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_cr_cencel_payment = Order_Table.objects.filter(Order_Status="Cancelled").filter(Vendors=uuuu).count()
    return HttpResponse(get_cr_cencel_payment)


@csrf_exempt
def get_vendor_refunded_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_count_r_refunded__payment = Order_Table.objects.filter(Order_Status="Refunded").filter(Vendors=uuuu).count()
    return HttpResponse(get_count_r_refunded__payment)


@csrf_exempt
def get_vendor_picked_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_count_picked_qt_payment = Order_Table.objects.filter(Order_Status="Picked").filter(Vendors=uuuu).count()
    return HttpResponse(get_count_picked_qt_payment)


@csrf_exempt
def get_vendor_hold_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_count_hold_q_payment = Order_Table.objects.filter(Order_Status="On hold").filter(Vendors=uuuu).count()
    return HttpResponse(get_count_hold_q_payment)


@csrf_exempt
def get_vendor_deposite_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_count_deposite_pyment = Order_Table.objects.exclude(Deposit_slip='').filter(Vendors=uuuu).count()
    return HttpResponse(get_count_deposite_pyment)


@csrf_exempt
def get_vendor_all_qty(request):
    itt = request.session.get('vendor_session_phone')
    uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    get_count_allpayment = Order_Table.objects.filter(Vendors=uuuu).count()
    return HttpResponse(get_count_allpayment)





def vendor_dashboard_order_filter(request):
    itt = request.session.get('vendor_session_phone')
    if itt:
        pending =False
        process =False
        Completed =False
        Cancelled =False
        Refunded =False
        Picked =False
        hold =False
        deposite = False
        Orders =False
    
        order_Pending_payment_filtere = request.GET.get('order_Pending_payment_filtere')
        order_Processing_filter = request.GET.get('order_Processing_filter')
        order_Completed_filter = request.GET.get('order_Completed_filter')
        order_Cancelled_filter = request.GET.get('order_Cancelled_filter')
        order_Refunded_filter = request.GET.get('order_Refunded_filter')
        order_Picked_filter = request.GET.get('order_Picked_filter')
        order_On_hold_filter = request.GET.get('order_On_hold_filter')
        order_Deposited_filter = request.GET.get('order_Deposited_filter')
        order_All_Orders_filter = request.GET.get('order_All_Orders_filter')
    
        #for start and end date
    
        order_Start_Date_filter = request.GET.get('order_Start_Date_filter')
        order_End_Date_filter = request.GET.get('order_End_Date_filter')
        order_status = request.GET.get('order_status')
        print(order_status)
    
        itt = request.session.get('vendor_session_phone')
        uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
    
        if order_Pending_payment_filtere:
            get_orders = Order_Table.objects.filter(Order_Status = order_Pending_payment_filtere).filter(Vendors=uuuu).order_by('-id')
            pending=True
            context = {'get_orders': get_orders, 'pending':pending}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
            
        if order_Processing_filter:
            get_orders = Order_Table.objects.filter(Order_Status = order_Processing_filter).filter(Vendors=uuuu).order_by('-id')
            process=True
            context = {'get_orders': get_orders, 'process':process}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    
        if order_Completed_filter:
            get_orders = Order_Table.objects.filter(Order_Status = order_Completed_filter).filter(Vendors=uuuu).order_by('-id')
            Completed=True
            context = {'get_orders': get_orders, 'Completed':Completed}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    
        if order_Cancelled_filter:
            get_orders = Order_Table.objects.filter(Order_Status = order_Cancelled_filter).filter(Vendors=uuuu).order_by('-id')
            Cancelled = True
            context = {'get_orders': get_orders, 'Cancelled':Cancelled}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    
        if order_Refunded_filter:
            get_orders = Order_Table.objects.filter(Order_Status = order_Refunded_filter).filter(Vendors=uuuu).order_by('-id')
            Refunded=True
            context = {'get_orders': get_orders, 'Refunded':Refunded}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    
        if order_Picked_filter:
            get_orders = Order_Table.objects.filter(Order_Status = order_Picked_filter).filter(Vendors=uuuu).order_by('-id')
            Picked=True
            context = {'get_orders': get_orders, 'Picked':Picked}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    
        if order_On_hold_filter:
            get_orders = Order_Table.objects.filter(Order_Status = order_On_hold_filter).filter(Vendors=uuuu).order_by('-id')
            hold=True
            context = {'get_orders': get_orders, 'hold':hold}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
            
            
        if order_Deposited_filter:
            get_orders = Order_Table.objects.exclude(Deposit_slip='').filter(Vendors=uuuu).order_by('-id')
            deposite=True
            context = {'get_orders': get_orders, 'deposite':deposite}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
            
    
        if order_All_Orders_filter:
            get_orders = Order_Table.objects.filter(Vendors=uuuu).order_by('-id')
            Orders=True
            context = {'get_orders': get_orders, 'Orders':Orders}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    
        if order_Start_Date_filter and order_End_Date_filter:
            print("i am in order_Start_Date_filter ............................")
            print(order_Start_Date_filter)
            print(order_End_Date_filter)
            
            if order_status=="Pending payment":
                pending=True
    
            elif order_status=="Processing":
                process =True
    
            elif order_status=="Completed":
                Completed =True
    
            elif order_status=="Cancelled":
                Cancelled =True
    
            elif order_status=="Refunded":
                Refunded =True
    
            elif order_status=="Picked":
                Picked =True
    
            elif order_status=="On hold":
                hold =True
                
            elif order_status == 'deposite':
                deposite = True
    
            elif order_status=="All Orders":
                Orders =True
    
    
            if order_status=='All Orders':
                get_orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Vendors=uuuu).order_by('-id')
                
            elif order_status == 'deposite':
                get_orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).exclude(Deposit_slip='').filter(Vendors=uuuu).order_by('-id')
    
            else:
                get_orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Status=order_status).filter(Vendors=uuuu).order_by('-id')
                
            all_ordr_qty = get_orders.count()
                
    
            context = {'get_orders': get_orders, 'order_Start_Date_filter':order_Start_Date_filter, 'order_End_Date_filter':order_End_Date_filter, 'pending':pending, 'process':process, 'Completed':Completed, 'Cancelled':Cancelled, 'Refunded':Refunded, 'Picked':Picked, 'hold':hold, 'deposite':deposite, 'Orders':Orders, 'all_ordr_qty':all_ordr_qty}
            return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    else:
        return redirect('vendor_login')

    



def vendor_search_order_id(request):
    itt = request.session.get('vendor_session_phone')
    if itt:
        uuuu = vendor_registration_table.objects.get(vendor_phone_no = itt)
        
        order_status = request.GET.get('order_status')
        
        search_input = request.GET.get('search_input')
        search_status = request.GET.get('search_status')
        
        all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Vendors=uuuu).filter(Order_Status=order_status)
        
        
        
        
        
        if search_status=="0":
            if order_status == "All Orders":
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Vendors=uuuu).order_by('-id')
            else:
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Vendors=uuuu).filter(Order_Status=order_status).order_by('-id')
        elif search_status=="1":
            if order_status == "All Orders":
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Vendors=uuuu)
            else:
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Vendors=uuuu).filter(Order_Status=order_status)
            
        search_qty = all_Orders2.count()
        
        p = Paginator(all_Orders2, 10)
        
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        
        list1 = []
        for i in range(1, number_of_pages_1):
            list1.append(i)
    
        page_num = request.GET.get('page', 1)
        
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        
        get_orders = page  
        
        page_num=int(page_num)
        
        
        pending =False
        process =False
        Completed =False
        Cancelled =False
        Refunded =False
        Picked =False
        hold =False
        deposite = False
        Orders =False
        
        if order_status=="Pending payment":
            pending=True

        elif order_status=="Processing":
            process =True

        elif order_status=="Completed":
            Completed =True

        elif order_status=="Cancelled":
            Cancelled =True

        elif order_status=="Refunded":
            Refunded =True

        elif order_status=="Picked":
            Picked =True

        elif order_status=="On hold":
            hold =True
            
        elif order_status == 'deposite':
            deposite = True

        elif order_status=="All Orders":
            Orders =True
        
        context = {'get_orders':get_orders, 'list1':list1, 'page_num':page_num, 'search_input':search_input, 'search_status':search_status, 'search_qty':search_qty, 'pending':pending, 'process':process, 'Completed':Completed, 'Cancelled':Cancelled, 'Refunded':Refunded, 'Picked':Picked, 'hold':hold, 'deposite':deposite, 'Orders':Orders}
        return render(request, "vendor_templates/single_vendor_orders_show.html", context)
    else:
        return redirect('vendor_login')
        
        




@csrf_exempt
def vendor_check_and_send_otp(request):
    varforgot_pass_num = request.POST.get('varforgot_pass_num')
    print(varforgot_pass_num)

    check_num = vendor_registration_table.objects.filter(vendor_phone_no=varforgot_pass_num)
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
def vendor_change_password_confirm(request):
    phn_number = request.POST.get('phn_number')
    password_forgot = request.POST.get('password_forgot')

    get_vendor = vendor_registration_table.objects.get(vendor_phone_no=phn_number)
    get_vendor.vendor_password = make_password(password_forgot)
    get_vendor.save()

    request.session['vendor_session_phone'] = get_vendor.vendor_phone_no
    request.session['vendor_session_pass'] = get_vendor.vendor_password
    request.session['vendor_session_name'] = get_vendor.vendor_name

    return HttpResponse(True)
