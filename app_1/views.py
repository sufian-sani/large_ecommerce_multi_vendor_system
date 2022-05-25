from django.shortcuts import render,HttpResponse, redirect
# Create your views here.
from PIL import Image


from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')





from .forms import add_category, add_Subcategory_1, add_product_alements, edit_product_field, add_Subcategory_2, add_brand, edit_order_detail, edit_Customer_delivery_info, form_Flash_Sell_add
from django.contrib import messages
from .models import Category, Subcategory_1, Brand, Products, Staff_Access, Subcategory_2, attribute_connect_with_product
from vendor_dashboard_app.models import vendor_registration_table
from django.core.files.storage import FileSystemStorage
from checkout.models import Order_Table, Order_Table_2, Customer_delivery_information
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from vendor_dashboard_app. models import vendor_registration_table
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from app_1.models import User
from checkout.models import order_table_logs
import math
from app_1.models import Attribute, Attribute_value, campaign_table, campaign_product_table, campaign_categories_percentage, Flash_Sell
import json




def deshboard_login(request):
    if request.method == "POST":
        deshboard_user_name = request.POST.get('deshboard_user_name')
        deshboard_password = request.POST.get('deshboard_password')
        print(deshboard_user_name, deshboard_password)

        check_username = Staff_Access.objects.filter(Username=deshboard_user_name)

        if check_username:
            get_row_username = Staff_Access.objects.get(Username=deshboard_user_name)
            password_get_row = get_row_username.Password

            staff_role = get_row_username.Staff_Role
            print(staff_role)

            if staff_role == 'Admin':
                if deshboard_password == password_get_row:
                    request.session['deshboard_admin_username'] = deshboard_user_name
                    request.session['deshboard_admin_password'] = deshboard_password

                    return redirect('deshboard_index')
                else:
                    messages.error(request, 'Invalid Password !!')
                    return redirect('deshboard_login')

            elif staff_role == 'Shop Manager':
                if deshboard_password == password_get_row:
                    request.session['deshboard_shop_manager_username'] = deshboard_user_name
                    request.session['deshboard_shop_manager_password'] = deshboard_password

                    return redirect('deshboard_index')
                else:
                    messages.error(request, 'Invalid Password !!')
                    return redirect('deshboard_login')

            elif staff_role == 'Customer Support':
                if deshboard_password == password_get_row:
                    request.session['deshboard_customer_support_username'] = deshboard_user_name
                    request.session['deshboard_customer_support_password'] = deshboard_password

                    return redirect('deshboard_index')
                else:
                    messages.error(request, 'Invalid Password !!')
                    return redirect('deshboard_login')

            elif staff_role == 'Upload Team':
                if deshboard_password == password_get_row:
                    request.session['deshboard_upload_team_username'] = deshboard_user_name
                    request.session['deshboard_upload_team_password'] = deshboard_password

                    return redirect('deshboard_index')
                else:
                    messages.error(request, 'Invalid Password !!')
                    return redirect('deshboard_login')
        else:
            messages.error(request, 'Invalid Username !!')
            return redirect('deshboard_login')


    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        return redirect('deshboard_index')
    else:
        return render(request, 'staff_login.html')


def dashboard_logout_func(request):
    request.session.clear()
    return redirect('deshboard_login')
    
    
    
    
    

def dashboard_order_filter(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        pending =False
        process =False
        Completed =False
        Cancelled =False
        Refunded =False
        Picked =False
        hold =False
        deposite = False
        Orders =False
        
        page_entries = True
    
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
        
        order_entries = request.GET.get('order_entries')
    
    
        if order_Pending_payment_filtere:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Pending_payment_filtere).filter(Campaign_Status="Reguler")
            pending=True
            
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
            all_Orders = page  
            page_num=int(page_num)
            context = {'all_Orders': all_Orders, 'pending':pending, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
            
            
        if order_Processing_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Processing_filter).filter(Campaign_Status="Reguler")
            process=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'process':process, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
    
        if order_Completed_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Completed_filter).filter(Campaign_Status="Reguler")
            Completed=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Completed':Completed, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
    
        if order_Cancelled_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Cancelled_filter).filter(Campaign_Status="Reguler")
            Cancelled = True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Cancelled':Cancelled, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
    
        if order_Refunded_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Refunded_filter).filter(Campaign_Status="Reguler")
            Refunded=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Refunded':Refunded, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
    
        if order_Picked_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Picked_filter).filter(Campaign_Status="Reguler")
            Picked=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Picked':Picked, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
    
        if order_On_hold_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_On_hold_filter).filter(Campaign_Status="Reguler")
            hold=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'hold':hold, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
            
            
        if order_Deposited_filter:
            all_Orders = Order_Table.objects.exclude(Deposit_slip='').filter(Campaign_Status="Reguler")
            deposite=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'deposite':deposite, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
            
    
        if order_All_Orders_filter:
            all_Orders = Order_Table.objects.filter(Campaign_Status="Reguler").order_by('-id')
            Orders=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Orders':Orders, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashbord_order.html", context)
    
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
                all_Orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Campaign_Status="Reguler")
                
            elif order_status == 'deposite':
                all_Orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).exclude(Deposit_slip='').filter(Campaign_Status="Reguler")
    
            else:
                all_Orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Status=order_status).filter(Campaign_Status="Reguler")
            
            all_ordr_qty = all_Orders.count()
                
                
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            date_page_entries = True
    
            context = {'all_Orders': all_Orders, 'order_Start_Date_filter':order_Start_Date_filter, 'order_End_Date_filter':order_End_Date_filter, 'pending':pending, 'process':process, 'Completed':Completed, 'Cancelled':Cancelled, 'Refunded':Refunded, 'Picked':Picked, 'hold':hold, 'deposite':deposite, 'Orders':Orders, 'all_ordr_qty':all_ordr_qty, 'page_num':page_num, 'list1':list, 'date_page_entries':date_page_entries}
            return render(request, "dashbord_order.html", context)
        return HttpResponse("it's workin")
    else:
        return redirect('deshboard_login')
    
    
    
    
    

def dashboard_order_filter_campaign(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        pending =False
        process =False
        Completed =False
        Cancelled =False
        Refunded =False
        Picked =False
        hold =False
        deposite = False
        Orders =False
        
        page_entries = True
    
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
        
        order_entries = request.GET.get('order_entries')
    
    
        if order_Pending_payment_filtere:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Pending_payment_filtere).filter(Campaign_Status="Campaign")
            pending=True
            
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
            all_Orders = page  
            page_num=int(page_num)
            context = {'all_Orders': all_Orders, 'pending':pending, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
            
            
        if order_Processing_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Processing_filter).filter(Campaign_Status="Campaign")
            process=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'process':process, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
    
        if order_Completed_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Completed_filter).filter(Campaign_Status="Campaign")
            Completed=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Completed':Completed, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
    
        if order_Cancelled_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Cancelled_filter).filter(Campaign_Status="Campaign")
            Cancelled = True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Cancelled':Cancelled, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
    
        if order_Refunded_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Refunded_filter).filter(Campaign_Status="Campaign")
            Refunded=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Refunded':Refunded, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
    
        if order_Picked_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_Picked_filter).filter(Campaign_Status="Campaign")
            Picked=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Picked':Picked, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
    
        if order_On_hold_filter:
            all_Orders = Order_Table.objects.filter(Order_Status = order_On_hold_filter).filter(Campaign_Status="Campaign")
            hold=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'hold':hold, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
            
            
        if order_Deposited_filter:
            all_Orders = Order_Table.objects.exclude(Deposit_slip='').filter(Campaign_Status="Campaign")
            deposite=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'deposite':deposite, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
            
    
        if order_All_Orders_filter:
            all_Orders = Order_Table.objects.filter(Campaign_Status="Campaign").order_by('-id')
            Orders=True
            
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            context = {'all_Orders': all_Orders, 'Orders':Orders, 'page_num':page_num, 'list1':list, 'page_entries':page_entries}
            return render(request, "dashboard_campaign_order.html", context)
    
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
                all_Orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Campaign_Status="Campaign")
                
            elif order_status == 'deposite':
                all_Orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).exclude(Deposit_slip='').filter(Campaign_Status="Campaign")
    
            else:
                all_Orders = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Status=order_status).filter(Campaign_Status="Campaign")
            
            all_ordr_qty = all_Orders.count()
                
                
            # pagination
            if order_entries:
                p = Paginator(all_Orders, order_entries)
            else:
                p = Paginator(all_Orders, 20)
        
            #show list of pages
            number_of_pages_1 = p.num_pages+1
            
            list = []
            for i in range(1, number_of_pages_1):
                list.append(i)
        
            page_num = request.GET.get('page', 1)
            
            try:
                page = p.page(page_num)
            except EmptyPage:
                page = p.page(1)
                
                
            
            all_Orders = page  
            
            page_num=int(page_num)
            
            date_page_entries = True
    
            context = {'all_Orders': all_Orders, 'order_Start_Date_filter':order_Start_Date_filter, 'order_End_Date_filter':order_End_Date_filter, 'pending':pending, 'process':process, 'Completed':Completed, 'Cancelled':Cancelled, 'Refunded':Refunded, 'Picked':Picked, 'hold':hold, 'deposite':deposite, 'Orders':Orders, 'all_ordr_qty':all_ordr_qty, 'page_num':page_num, 'list1':list, 'date_page_entries':date_page_entries}
            return render(request, "dashboard_campaign_order.html", context)
        return HttpResponse("it's workin")
    else:
        return redirect('deshboard_login')
    
    


def deshboard_index(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    print(staff_admin)

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        return render(request, "deshboard_index.html")
    else:
        return redirect('deshboard_login')


def dashbord_order(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    print(staff_admin)
    
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        
        order_entries = request.GET.get('order_entries')
        
        all_Orders1 = Order_Table.objects.filter(Campaign_Status="Reguler").order_by('-Order_Id')
        Orders = True
        
        # pagination
        if order_entries:
            p = Paginator(all_Orders1, order_entries)
        else:
            p = Paginator(all_Orders1, 20)
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        
        list = []
        for i in range(1, number_of_pages_1):
            list.append(i)
    
        page_num = request.GET.get('page', 1)
        
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
            
        
        all_Orders = page  
        
        page_num=int(page_num)
        
        context = {'all_Orders': all_Orders, 'Orders':Orders, 'list':list, 'page_num':page_num, 'order_entries':order_entries}
        return render(request, "dashbord_order.html", context)
    else:
        return redirect('deshboard_login')


def dashboard_campaign_order(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    print(staff_admin)
    
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        
        order_entries = request.GET.get('order_entries')
        
        all_Orders1 = Order_Table.objects.filter(Campaign_Status="Campaign").order_by('-Order_Id')
        Orders = True
        
        # pagination
        if order_entries:
            p = Paginator(all_Orders1, order_entries)
        else:
            p = Paginator(all_Orders1, 20)
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        
        list = []
        for i in range(1, number_of_pages_1):
            list.append(i)
    
        page_num = request.GET.get('page', 1)
        
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
            
        
        all_Orders = page  
        
        page_num=int(page_num)
        
        context = {'all_Orders': all_Orders, 'Orders':Orders, 'list':list, 'page_num':page_num, 'order_entries':order_entries}
        return render(request, "dashboard_campaign_order.html", context)
    else:
        return redirect('deshboard_login')





    
def search_order_id(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        search_input = request.GET.get('search_input')
        search_status = request.GET.get('search_status')
        
        order_status = request.GET.get('order_status')
        
        order_entries = request.GET.get('order_entries')
        
        all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Order_Status=order_status).filter(Campaign_Status="Reguler")
        
        if search_status=="0":
            if order_status == "All Orders":
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Campaign_Status="Reguler").order_by('-id')
            else:
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Order_Status=order_status).filter(Campaign_Status="Reguler").order_by('-id')
        elif search_status=="1":
            if order_status == "All Orders":
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Campaign_Status="Reguler")
            else:
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Order_Status=order_status).filter(Campaign_Status="Reguler")
            
        search_qty = all_Orders2.count()
        
        if order_entries:
            p = Paginator(all_Orders2, order_entries)
        else:
            p = Paginator(all_Orders2, 20)
        
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
        
        all_Orders = page  
        
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
            
        search_box_entries_qty = True
        
        context = {'all_Orders':all_Orders, 'list1':list1, 'page_num':page_num, 'search_input':search_input, 'search_status':search_status, 'search_qty':search_qty, 'pending':pending, 'process':process, 'Completed':Completed, 'Cancelled':Cancelled, 'Refunded':Refunded, 'Picked':Picked, 'hold':hold, 'deposite':deposite, 'Orders':Orders, 'search_box_entries_qty':search_box_entries_qty}
        return render(request, "dashbord_order.html", context)
    else:
        return redirect('deshboard_login')
        
        
        
def search_order_id_campaign(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        search_input = request.GET.get('search_input')
        search_status = request.GET.get('search_status')
        
        order_status = request.GET.get('order_status')
        
        order_entries = request.GET.get('order_entries')
        
        all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Order_Status=order_status).filter(Campaign_Status="Campaign")
        
        if search_status=="0":
            if order_status == "All Orders":
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Campaign_Status="Campaign").order_by('-id')
            else:
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Order_Status=order_status).filter(Campaign_Status="Campaign").order_by('-id')
        elif search_status=="1":
            if order_status == "All Orders":
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Campaign_Status="Campaign")
            else:
                all_Orders2 = Order_Table.objects.filter(Order_Id__icontains = search_input).filter(Order_Status=order_status).filter(Campaign_Status="Campaign")
            
        search_qty = all_Orders2.count()
        
        if order_entries:
            p = Paginator(all_Orders2, order_entries)
        else:
            p = Paginator(all_Orders2, 20)
        
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
        
        all_Orders = page  
        
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
            
        search_box_entries_qty = True
        
        context = {'all_Orders':all_Orders, 'list1':list1, 'page_num':page_num, 'search_input':search_input, 'search_status':search_status, 'search_qty':search_qty, 'pending':pending, 'process':process, 'Completed':Completed, 'Cancelled':Cancelled, 'Refunded':Refunded, 'Picked':Picked, 'hold':hold, 'deposite':deposite, 'Orders':Orders, 'search_box_entries_qty':search_box_entries_qty}
        return render(request, "dashboard_campaign_order.html", context)
    else:
        return redirect('deshboard_login')
        
        


def dashbord_all_product(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    print(staff_admin)
    if staff_admin or staff_shop_manager or staff_upload_team:
        all_product_show = Products.objects.all()
        all_product_qunt = Products.objects.all().count()

        all_Category = Category.objects.all()
        print(all_Category)
        
        order_entries = request.GET.get('order_entries')
        
        # pagination
        if order_entries:
            p = Paginator(all_product_show, order_entries)
        else:
            p = Paginator(all_product_show, 20)
        
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_prod = []
        for i in range(1, number_of_pages_1):
            list_prod.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        all_product_show = page
            
        page_num = int(page_num)

        context = {'all_product_show': all_product_show, 'all_Category':all_Category, 'all_product_qunt':all_product_qunt, 'page_num':page_num, 'all_product_show':all_product_show, 'list_prod':list_prod, 'order_entries':order_entries}
        return render(request, "All_Products.html", context)
    else:
        return redirect('deshboard_login')


def dashbord_add_new_products(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        form_product = add_product_alements()
        if request.method == 'POST':

            Product_name = request.POST.get('Product_name')
            SKU = request.POST.get('SKU')
            TYPE_OF_PRODUCTS = request.POST.get('TYPE_OF_PRODUCTS')
            MRP_Price = request.POST.get('MRP_Price')

            Cost_Price = request.POST.get('Cost_Price')
            if Cost_Price == '':
                Cost_Price = None
            Discount_Price = request.POST.get('Discount_Price')
            if Discount_Price == '':
                Discount_Price = None

            product_quentity = request.POST.get('product_quentity')
            Meta_Title = request.POST.get('Meta_Title')
            Meta_Keyword = request.POST.get('Meta_Keyword')

            Category_list = request.POST.get('Category_list')

            suncat1 = request.POST.get('suncat1')
            suncat1 = json.loads(suncat1)
            suncat2 = request.POST.get('suncat2')
            suncat2 = json.loads(suncat2)
            print('suncat1, suncat2')
            print(suncat1, suncat2)




            get_rowcat = Category.objects.get(id=Category_list)
            
            
            # if Category_list == 'None' or Category_list == '':
            #     get_rowcat = ""
            #     get_rowsub1 = ""
            #     get_rowsub2 = ""
            # else:
            #     get_rowcat = Category.objects.get(id=Category_list)
            #     if Subategory_list == 'None':
            #         get_rowsub1=""
            #         get_rowsub2=""
            #     else:
            #         get_rowsub1 = Subcategory_1.objects.get(id=Subategory_list)
            #         if Subategory_list2 == 'None':
            #             get_rowsub2 = ""
            #         else:
            #             get_rowsub2 = Subcategory_2.objects.get(id=Subategory_list2)

            # print('get_rowsub1, get_rowsub2')
            # print(get_rowsub1, get_rowsub2)

            make_feature_product = request.POST.get('make_feature_product')
            print(make_feature_product)

            if make_feature_product=='on':
                make_feature_product='True'
            else:
                make_feature_product = 'False'


            print(Product_name, SKU, MRP_Price, Discount_Price, Meta_Title, Meta_Keyword)

            # try:
            print('ok')
            # Prod_Image = request.FILES['Product_Image']

            Prod_Image = request.FILES.get('Prod_Image')
            Product_Image_2 = request.FILES.get('Product_Image_2')
            Product_Image_3 = request.FILES.get('Product_Image_3')
            Product_Image_4 = request.FILES.get('Product_Image_4')

            print(Prod_Image, Product_Image_2, Product_Image_3, Product_Image_4)

            if Prod_Image:
                fs = FileSystemStorage()
                filename = fs.save(Prod_Image.name, Prod_Image)
                url_file = fs.url(filename)

                image = Image.open(Prod_Image)
                image = image.convert('RGB')
                image.save(f'{MEDIA_ROOT}/{filename}.webp', 'webp')

                url_file = fs.url(f'{filename}.webp')

            else:
                url_file = ''

            if Product_Image_2:
                fs = FileSystemStorage()
                filename2 = fs.save(Product_Image_2.name, Product_Image_2)
                url_file2 = fs.url(filename2)

                image = Image.open(Product_Image_2)
                image = image.convert('RGB')
                image.save(f'{MEDIA_ROOT}/{filename2}.webp', 'webp')
                url_file2 = fs.url(f'{filename2}.webp')

            else:
                url_file2 = ''

            if Product_Image_3:
                fs = FileSystemStorage()
                filename3 = fs.save(Product_Image_3.name, Product_Image_3)
                url_file3 = fs.url(filename3)

                image = Image.open(Product_Image_3)
                image = image.convert('RGB')
                image.save(f'{MEDIA_ROOT}/{filename3}.webp', 'webp')
                url_file3 = fs.url(f'{filename3}.webp')

            else:
                url_file3 = ''

            if Product_Image_4:
                fs = FileSystemStorage()
                filename4 = fs.save(Product_Image_4.name, Product_Image_4)
                url_file4 = fs.url(filename4)

                image = Image.open(Product_Image_4)
                image = image.convert('RGB')
                image.save(f'{MEDIA_ROOT}/{filename4}.webp', 'webp')
                url_file4 = fs.url(f'{filename4}.webp')

            else:
                url_file4 = ''

            print('online check')

            form_product = add_product_alements(request.POST)
            if form_product.is_valid():
                other_value = form_product.save(commit=False)
                other_value.Product_Name = Product_name
                other_value.SKU = SKU
                other_value.Category = get_rowcat


                # if Category_list != 'None':
                #     other_value.Category = get_rowcat
                #     if Subategory_list != 'None':
                #        other_value.Subcategory_1 = get_rowsub1
                #        if Subategory_list2 != 'None':
                #            other_value.Subcategory_2 = get_rowsub2


                other_value.TYPE_OF_PRODUCTS = TYPE_OF_PRODUCTS
                other_value.MRP_Price = MRP_Price
                other_value.Cost_Price = Cost_Price
                other_value.Discount_Price = Discount_Price
                other_value.Product_stock_Quantity = product_quentity
                other_value.Meta_Title = Meta_Title
                other_value.Meta_Keyword = Meta_Keyword
                other_value.Product_Image = url_file
                other_value.Product_Image2 = url_file2
                other_value.Product_Image3 = url_file3
                other_value.Product_Image4 = url_file4
                other_value.make_star = make_feature_product

                other_value.save()

                print(other_value.slug)


                for subc1 in suncat1:
                    other_value.Subcategory_1.add(subc1)

                for subc2 in suncat2:
                    other_value.Subcategory_2.add(subc2)

                messages.success(request, f'Successfully Added The Product - {Product_name}')

            # except:
            #     print('execpt')
            #     form_product = add_product_alements(request.POST)
            #     if form_product.is_valid():
            #         other_value = form_product.save(commit=False)
            #         other_value.Product_Name = Product_name
            #         other_value.SKU = SKU
            #
            #         if Category_list != 'None':
            #             other_value.Category = get_rowcat
            #
            #         if Subategory_list is not None:
            #             other_value.Subcategory_1 = get_rowsub1
            #
            #         if Subategory_list2 is not None:
            #             other_value.Subcategory_2 = get_rowsub2
            #
            #         other_value.MRP_Price = MRP_Price
            #         other_value.Cost_Price = Cost_Price
            #         other_value.Discount_Price = Discount_Price
            #         other_value.Product_stock_Quantity = product_quentity
            #
            #         other_value.Meta_Title = Meta_Title
            #         other_value.Meta_Keyword = Meta_Keyword
            #         other_value.make_star = make_feature_product
            #         other_value.save()
            #         messages.success(request, f'Successfully Added The Product - {Product_name}')

            if other_value.TYPE_OF_PRODUCTS == 'Variable Product' or other_value.TYPE_OF_PRODUCTS == 'Virtual Product':
                return redirect('add_attributes', other_value.slug)
            else:
                return redirect('dashbord_add_new_products')

        get_all_categories = Category.objects.all()
        context = {'form_product': form_product, 'get_all_categories':get_all_categories}
        return render(request, "dashbord_add_new_products.html", context)
    else:
        return redirect('deshboard_login')










def delete_edited_add_attribute_form_add_product(request, i_connect_with_product_slug):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        print("i_connect_with_product_slug")
        print(i_connect_with_product_slug)


        get_the_Product_i_connect_with_product_slug = attribute_connect_with_product.objects.get(id=i_connect_with_product_slug)

        k = get_the_Product_i_connect_with_product_slug.connect_with_product.slug
        get_the_Product_i_connect_with_product_slug.delete()

        return redirect('add_attributes', k)

    else:
        return redirect('deshboard_login')





def EDIT_edited_add_attribute_form_add_product(request, i_connect_with_product_slug):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')


    if staff_admin or staff_shop_manager or staff_upload_team:
        variable_qty = request.POST.get('variable_qty')
        stock_status_name = request.POST.get('stock_status_name')

        get_attribute_from_this_perticuler_product = attribute_connect_with_product.objects.get(
            id=i_connect_with_product_slug)

        get_the_Product_name = get_attribute_from_this_perticuler_product.connect_with_product


        Size_attribute__all = Attribute.objects.get(Attribute_name='Size')
        Size_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Size_attribute__all)

        Color_attribute__all = Attribute.objects.get(Attribute_name='Color')
        Color_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Color_attribute__all)

        Flavor_attribute__all = Attribute.objects.get(Attribute_name='Flavor')
        Flavor_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Flavor_attribute__all)

        Variation_attribute__all = Attribute.objects.get(Attribute_name='Variation')
        Variation_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Variation_attribute__all)

        Weight_attribute__all = Attribute.objects.get(Attribute_name='Weight')
        Weight_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Weight_attribute__all)

        Volume_attribute__all = Attribute.objects.get(Attribute_name='Volume')
        Volume_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Volume_attribute__all)

        Quantity_attribute__all = Attribute.objects.get(Attribute_name='Quantity')
        Quantity_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Quantity_attribute__all)

        Values_attribute__all = Attribute.objects.get(Attribute_name='Values')
        Values_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Values_attribute__all)

        Material_Type_attribute__all = Attribute.objects.get(Attribute_name='Material Type')
        Material_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Material_Type_attribute__all)

        Product_Type_attribute__all = Attribute.objects.get(Attribute_name='Product Type')
        Product_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Product_Type_attribute__all)

        Verification_attribute__all = Attribute.objects.get(Attribute_name='Verification')
        Verification_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Verification_attribute__all)

        Quality_attribute__all = Attribute.objects.get(Attribute_name='Quality')
        Quality_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Quality_attribute__all)

        Marketing_Claims_attribute__all = Attribute.objects.get(Attribute_name='Marketing Claims')
        Marketing_Claims_attribute_value_all = Attribute_value.objects.filter(
            Attribute_name=Marketing_Claims_attribute__all)

        Design_attribute__all = Attribute.objects.get(Attribute_name='Design')
        Design_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Design_attribute__all)

        Smell_attribute__all = Attribute.objects.get(Attribute_name='Smell')
        Smell_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Smell_attribute__all)

        Reliability_attribute__all = Attribute.objects.get(Attribute_name='Reliability')
        Reliability_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Reliability_attribute__all)

        Content_attribute__all = Attribute.objects.get(Attribute_name='Content')
        Content_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Content_attribute__all)

        Safety_attribute__all = Attribute.objects.get(Attribute_name='Safety')
        Safety_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Safety_attribute__all)

        Package_attribute__all = Attribute.objects.get(Attribute_name='Package')
        Package_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Package_attribute__all)

        Model_attribute__all = Attribute.objects.get(Attribute_name='Model')
        Model_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Model_attribute__all)

        Taste_attribute__all = Attribute.objects.get(Attribute_name='Taste')
        Taste_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Taste_attribute__all)

        Feel_attribute__all = Attribute.objects.get(Attribute_name='Feel')
        Feel_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Feel_attribute__all)

        Defferent_Type_attribute__all = Attribute.objects.get(Attribute_name='Defferent Type')
        Defferent_Type_attribute_value_all = Attribute_value.objects.filter(
            Attribute_name=Defferent_Type_attribute__all)



        context = {
            'get_the_Product_name': get_the_Product_name,
            'get_attribute_from_this_perticuler_product': get_attribute_from_this_perticuler_product,
            'Size_attribute_value_all': Size_attribute_value_all,
            'Color_attribute_value_all': Color_attribute_value_all,
            'Flavor_attribute_value_all': Flavor_attribute_value_all,
            'Variation_attribute_value_all': Variation_attribute_value_all,
            'Weight_attribute_value_all': Weight_attribute_value_all,
            'Volume_attribute_value_all': Volume_attribute_value_all,
            'Quantity_attribute_value_all': Quantity_attribute_value_all,
            'Values_attribute_value_all': Values_attribute_value_all,
            'Material_Type_attribute_value_all': Material_Type_attribute_value_all,
            'Product_Type_attribute_value_all': Product_Type_attribute_value_all,
            'Verification_attribute_value_all': Verification_attribute_value_all,
            'Quality_attribute_value_all': Quality_attribute_value_all,
            'Marketing_Claims_attribute_value_all': Marketing_Claims_attribute_value_all,
            'Design_attribute_value_all': Design_attribute_value_all,
            'Smell_attribute_value_all': Smell_attribute_value_all,
            'Reliability_attribute_value_all': Reliability_attribute_value_all,
            'Content_attribute_value_all': Content_attribute_value_all,
            'Safety_attribute_value_all': Safety_attribute_value_all,
            'Package_attribute_value_all': Package_attribute_value_all,
            'Model_attribute_value_all': Model_attribute_value_all,
            'Taste_attribute_value_all': Taste_attribute_value_all,
            'Feel_attribute_value_all': Feel_attribute_value_all,
            'Defferent_Type_attribute_value_all': Defferent_Type_attribute_value_all}

        return render(request, 'EDIT_edited_add_attribute_form_add_product.html', context)
    else:
        return redirect('deshboard_login')





def save_EDIT_edited_add_attribute_form_add_product(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        variable_qty = request.POST.get('variable_qty')
        if variable_qty == '' or variable_qty == 'None':
            variable_qty = None

        stock_status_name = request.POST.get('stock_status_name')

        going_to_save_get_the_Product_name_Product_Name = request.POST.get('going_to_save_get_the_Product_name_Product_Name')

        get_attribute_from_this_perticuler_product_id = request.POST.get('get_attribute_from_this_perticuler_product_id')


        going_to_save_name_Size_attribute_value_all = request.POST.get('going_to_save_name_Size_attribute_value_all')
        going_to_save_name_Color_attribute_value_all = request.POST.get('going_to_save_name_Color_attribute_value_all')
        going_to_save_name_Flavor_attribute_value_all = request.POST.get('going_to_save_name_Flavor_attribute_value_all')
        going_to_save_name_Variation_attribute_value_all = request.POST.get('going_to_save_name_Variation_attribute_value_all')
        going_to_save_name_Weight_attribute_value_all = request.POST.get('going_to_save_name_Weight_attribute_value_all')
        going_to_save_name_Volume_attribute_value_all = request.POST.get('going_to_save_name_Volume_attribute_value_all')
        going_to_save_name_Quantity_attribute_value_all = request.POST.get('going_to_save_name_Quantity_attribute_value_all')
        going_to_save_name_Values_attribute_value_all = request.POST.get('going_to_save_name_Values_attribute_value_all')
        going_to_save_name_Material_Type_attribute_value_all = request.POST.get('going_to_save_name_Material_Type_attribute_value_all')
        going_to_save_name_Product_Type_attribute_value_all = request.POST.get('going_to_save_name_Product_Type_attribute_value_all')
        going_to_save_name_Verification_attribute_value_all = request.POST.get('going_to_save_name_Verification_attribute_value_all')
        going_to_save_name_Quality_attribute_value_all = request.POST.get('going_to_save_name_Quality_attribute_value_all')
        going_to_save_name_Marketing_Claims_attribute_value_all = request.POST.get('going_to_save_name_Marketing_Claims_attribute_value_all')
        going_to_save_name_Design_attribute_value_all = request.POST.get('going_to_save_name_Design_attribute_value_all')
        going_to_save_name_Smell_attribute_value_all = request.POST.get('going_to_save_name_Smell_attribute_value_all')
        going_to_save_name_Reliability_attribute_value_all = request.POST.get('going_to_save_name_Reliability_attribute_value_all')
        going_to_save_name_Content_attribute_value_all = request.POST.get('going_to_save_name_Content_attribute_value_all')
        going_to_save_name_Safety_attribute_value_all = request.POST.get('going_to_save_name_Safety_attribute_value_all')
        going_to_save_name_Package_attribute_value_all = request.POST.get('going_to_save_name_Package_attribute_value_all')
        going_to_save_name_Model_attribute_value_all = request.POST.get('going_to_save_name_Model_attribute_value_all')
        going_to_save_name_Taste_attribute_value_all = request.POST.get('going_to_save_name_Taste_attribute_value_all')
        going_to_save_name_Feel_attribute_value_all = request.POST.get('going_to_save_name_Feel_attribute_value_all')
        going_to_save_name_Defferent_Type_attribute_value_all = request.POST.get('going_to_save_name_Defferent_Type_attribute_value_all')

        going_to_save_attribute_image_get = request.FILES.get('going_to_save_attribute_image_get')

        if going_to_save_attribute_image_get:
            fs = FileSystemStorage()
            filename = fs.save(going_to_save_attribute_image_get.name, going_to_save_attribute_image_get)
            url_file = fs.url(filename)
        else:
            url_file = ''

        going_to_save_variable_MRP_Price = request.POST.get('going_to_save_variable_MRP_Price')

        going_to_save_variable_Cost_Price = request.POST.get('going_to_save_variable_Cost_Price')
        if going_to_save_variable_Cost_Price == '' or going_to_save_variable_Cost_Price=='None':
            going_to_save_variable_Cost_Price=None

        going_to_save_variable_Discount_Price = request.POST.get('going_to_save_variable_Discount_Price')
        if going_to_save_variable_Discount_Price == '' or going_to_save_variable_Discount_Price=='None':
            going_to_save_variable_Discount_Price=None

        gest_astrribute_product = attribute_connect_with_product.objects.get(id= get_attribute_from_this_perticuler_product_id)

        gest_astrribute_product.Size = going_to_save_name_Size_attribute_value_all
        gest_astrribute_product.Color = going_to_save_name_Color_attribute_value_all
        gest_astrribute_product.Flavor = going_to_save_name_Flavor_attribute_value_all
        gest_astrribute_product.Variation = going_to_save_name_Variation_attribute_value_all
        gest_astrribute_product.Weight = going_to_save_name_Weight_attribute_value_all
        gest_astrribute_product.Volume = going_to_save_name_Volume_attribute_value_all
        gest_astrribute_product.Values = going_to_save_name_Values_attribute_value_all
        gest_astrribute_product.Quantity = going_to_save_name_Quantity_attribute_value_all
        gest_astrribute_product.Material_Type = going_to_save_name_Material_Type_attribute_value_all
        gest_astrribute_product.Product_Type = going_to_save_name_Product_Type_attribute_value_all
        gest_astrribute_product.Verification = going_to_save_name_Verification_attribute_value_all
        gest_astrribute_product.Quality = going_to_save_name_Quality_attribute_value_all
        gest_astrribute_product.Marketing_Claims = going_to_save_name_Marketing_Claims_attribute_value_all
        gest_astrribute_product.Design = going_to_save_name_Design_attribute_value_all

        gest_astrribute_product.Smell = going_to_save_name_Smell_attribute_value_all
        gest_astrribute_product.Reliability = going_to_save_name_Reliability_attribute_value_all
        gest_astrribute_product.Content = going_to_save_name_Content_attribute_value_all
        gest_astrribute_product.Safety = going_to_save_name_Safety_attribute_value_all
        gest_astrribute_product.Package = going_to_save_name_Package_attribute_value_all
        gest_astrribute_product.Model = going_to_save_name_Model_attribute_value_all

        gest_astrribute_product.Taste = going_to_save_name_Taste_attribute_value_all
        gest_astrribute_product.Feel = going_to_save_name_Feel_attribute_value_all
        gest_astrribute_product.Defferent_Type = going_to_save_name_Defferent_Type_attribute_value_all

        if going_to_save_attribute_image_get != None:
            gest_astrribute_product.attribute_image_of_product = url_file

        gest_astrribute_product.Cost_Price = going_to_save_variable_Cost_Price
        gest_astrribute_product.MRP_Price = going_to_save_variable_MRP_Price
        gest_astrribute_product.Discount_Price = going_to_save_variable_Discount_Price

        gest_astrribute_product.Attribute_Quantity = variable_qty
        gest_astrribute_product.Stock_status = stock_status_name

        gest_astrribute_product.save()


        return redirect('add_attributes', going_to_save_get_the_Product_name_Product_Name)
    else:
        return redirect('deshboard_login')























def add_attributes(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        get_the_Product_name = Products.objects.get(slug=pk)

        Size_attribute__all = Attribute.objects.get(Attribute_name='Size')
        Size_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Size_attribute__all)

        Color_attribute__all = Attribute.objects.get(Attribute_name='Color')
        Color_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Color_attribute__all)

        Flavor_attribute__all = Attribute.objects.get(Attribute_name='Flavor')
        Flavor_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Flavor_attribute__all)

        Variation_attribute__all = Attribute.objects.get(Attribute_name='Variation')
        Variation_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Variation_attribute__all)

        Weight_attribute__all = Attribute.objects.get(Attribute_name='Weight')
        Weight_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Weight_attribute__all)

        Volume_attribute__all = Attribute.objects.get(Attribute_name='Volume')
        Volume_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Volume_attribute__all)

        Quantity_attribute__all = Attribute.objects.get(Attribute_name='Quantity')
        Quantity_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Quantity_attribute__all)

        Values_attribute__all = Attribute.objects.get(Attribute_name='Values')
        Values_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Values_attribute__all)

        Material_Type_attribute__all = Attribute.objects.get(Attribute_name='Material Type')
        Material_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Material_Type_attribute__all)

        Product_Type_attribute__all = Attribute.objects.get(Attribute_name='Product Type')
        Product_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Product_Type_attribute__all)

        Verification_attribute__all = Attribute.objects.get(Attribute_name='Verification')
        Verification_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Verification_attribute__all)

        Quality_attribute__all = Attribute.objects.get(Attribute_name='Quality')
        Quality_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Quality_attribute__all)

        Marketing_Claims_attribute__all = Attribute.objects.get(Attribute_name='Marketing Claims')
        Marketing_Claims_attribute_value_all = Attribute_value.objects.filter(
            Attribute_name=Marketing_Claims_attribute__all)

        Design_attribute__all = Attribute.objects.get(Attribute_name='Design')
        Design_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Design_attribute__all)

        Smell_attribute__all = Attribute.objects.get(Attribute_name='Smell')
        Smell_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Smell_attribute__all)

        Reliability_attribute__all = Attribute.objects.get(Attribute_name='Reliability')
        Reliability_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Reliability_attribute__all)

        Content_attribute__all = Attribute.objects.get(Attribute_name='Content')
        Content_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Content_attribute__all)

        Safety_attribute__all = Attribute.objects.get(Attribute_name='Safety')
        Safety_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Safety_attribute__all)

        Package_attribute__all = Attribute.objects.get(Attribute_name='Package')
        Package_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Package_attribute__all)

        Model_attribute__all = Attribute.objects.get(Attribute_name='Model')
        Model_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Model_attribute__all)

        Taste_attribute__all = Attribute.objects.get(Attribute_name='Taste')
        Taste_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Taste_attribute__all)

        Feel_attribute__all = Attribute.objects.get(Attribute_name='Feel')
        Feel_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Feel_attribute__all)

        Defferent_Type_attribute__all = Attribute.objects.get(Attribute_name='Defferent Type')
        Defferent_Type_attribute_value_all = Attribute_value.objects.filter(
            Attribute_name=Defferent_Type_attribute__all)

        get_attribute_from_this_perticuler_product = attribute_connect_with_product.objects.filter(
            connect_with_product=get_the_Product_name)

        context = {
            'get_the_Product_name': get_the_Product_name,
            'get_attribute_from_this_perticuler_product':get_attribute_from_this_perticuler_product,
            'Size_attribute_value_all': Size_attribute_value_all,
            'Color_attribute_value_all': Color_attribute_value_all,
            'Flavor_attribute_value_all': Flavor_attribute_value_all,
            'Variation_attribute_value_all': Variation_attribute_value_all,
            'Weight_attribute_value_all': Weight_attribute_value_all,
            'Volume_attribute_value_all': Volume_attribute_value_all,
            'Quantity_attribute_value_all': Quantity_attribute_value_all,
            'Values_attribute_value_all': Values_attribute_value_all,
            'Material_Type_attribute_value_all': Material_Type_attribute_value_all,
            'Product_Type_attribute_value_all': Product_Type_attribute_value_all,
            'Verification_attribute_value_all': Verification_attribute_value_all,
            'Quality_attribute_value_all': Quality_attribute_value_all,
            'Marketing_Claims_attribute_value_all': Marketing_Claims_attribute_value_all,
            'Design_attribute_value_all': Design_attribute_value_all,
            'Smell_attribute_value_all': Smell_attribute_value_all,
            'Reliability_attribute_value_all': Reliability_attribute_value_all,
            'Content_attribute_value_all': Content_attribute_value_all,
            'Safety_attribute_value_all': Safety_attribute_value_all,
            'Package_attribute_value_all': Package_attribute_value_all,
            'Model_attribute_value_all': Model_attribute_value_all,
            'Taste_attribute_value_all': Taste_attribute_value_all,
            'Feel_attribute_value_all': Feel_attribute_value_all,
            'Defferent_Type_attribute_value_all': Defferent_Type_attribute_value_all}

        return render(request, 'add_attribute_form_add_product.html', context)
    else:
        return redirect('deshboard_login')








def dashbord_add_new_products_attribute(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')


    if staff_admin or staff_shop_manager or staff_upload_team:
        variable_qty = request.POST.get('variable_qty')
        print(variable_qty)


        if variable_qty == '':
            variable_qty=None
        else:
            pass


        stock_status_name = request.POST.get('stock_status_name')

        get_the_Product_name_Product_Name = request.POST.get('get_the_Product_name_Product_Name')
        print("get_the_Product_name_Product_Name")
        print("get_the_Product_name_Product_Name")
        print("get_the_Product_name_Product_Name")
        print(get_the_Product_name_Product_Name)
        get_attribute_image_get = request.FILES.get('attribute_image_get')
        print("get_attribute_image_get")
        print("get_attribute_image_get")
        print(get_attribute_image_get)

        get_the_Product_name = Products.objects.get(slug=get_the_Product_name_Product_Name)
        get_attribute_from_this_perticuler_product = attribute_connect_with_product.objects.filter(
            connect_with_product=get_the_Product_name)

        print("get_the_Product_name")
        print("get_the_Product_name")
        print(get_the_Product_name)

        if get_attribute_image_get:
            fs = FileSystemStorage()
            filename = fs.save(get_attribute_image_get.name, get_attribute_image_get)
            url_file4 = fs.url(filename)
        else:
            url_file4 = ''



        name_Size_attribute_value_all = request.POST.get('name_Size_attribute_value_all')
        if not name_Size_attribute_value_all:
            name_Size_attribute_value_all=""
        name_Color_attribute_value_all = request.POST.get('name_Color_attribute_value_all')
        if not name_Color_attribute_value_all:
            name_Color_attribute_value_all=""
        name_Flavor_attribute_value_all = request.POST.get('name_Flavor_attribute_value_all')
        if not name_Flavor_attribute_value_all:
            name_Flavor_attribute_value_all=""
        name_Variation_attribute_value_all = request.POST.get('name_Variation_attribute_value_all')
        if not name_Variation_attribute_value_all:
            name_Variation_attribute_value_all=""
        name_Weight_attribute_value_all = request.POST.get('name_Weight_attribute_value_all')
        if not name_Weight_attribute_value_all:
            name_Weight_attribute_value_all=""
        name_Volume_attribute_value_all = request.POST.get('name_Volume_attribute_value_all')
        if not name_Volume_attribute_value_all:
            name_Volume_attribute_value_all=""
        name_Quantity_attribute_value_all = request.POST.get('name_Quantity_attribute_value_all')
        if not name_Quantity_attribute_value_all:
            name_Quantity_attribute_value_all=""
        name_Values_attribute_value_all = request.POST.get('name_Values_attribute_value_all')
        if not name_Values_attribute_value_all:
            name_Values_attribute_value_all=""
        name_Material_Type_attribute_value_all = request.POST.get('name_Material_Type_attribute_value_all')
        if not name_Material_Type_attribute_value_all:
            name_Material_Type_attribute_value_all=""
        name_Product_Type_attribute_value_all = request.POST.get('name_Product_Type_attribute_value_all')
        if not name_Product_Type_attribute_value_all:
            name_Product_Type_attribute_value_all=""
        name_Verification_attribute_value_all = request.POST.get('name_Verification_attribute_value_all')
        if not name_Verification_attribute_value_all:
            name_Verification_attribute_value_all=""
        name_Quality_attribute_value_all = request.POST.get('name_Quality_attribute_value_all')
        if not name_Quality_attribute_value_all:
            name_Quality_attribute_value_all=""
        name_Marketing_Claims_attribute_value_all = request.POST.get('name_Marketing_Claims_attribute_value_all')
        if not name_Marketing_Claims_attribute_value_all:
            name_Marketing_Claims_attribute_value_all=""
        name_Design_attribute_value_all = request.POST.get('name_Design_attribute_value_all')
        if not name_Design_attribute_value_all:
            name_Design_attribute_value_all=""
        name_Smell_attribute_value_all = request.POST.get('name_Smell_attribute_value_all')
        if not name_Smell_attribute_value_all:
            name_Smell_attribute_value_all=""
        name_Reliability_attribute_value_all = request.POST.get('name_Reliability_attribute_value_all')
        if not name_Reliability_attribute_value_all:
            name_Reliability_attribute_value_all=""
        name_Content_attribute_value_all = request.POST.get('name_Content_attribute_value_all')
        if not name_Content_attribute_value_all:
            name_Content_attribute_value_all=""
        name_Safety_attribute_value_all = request.POST.get('name_Safety_attribute_value_all')
        if not name_Safety_attribute_value_all:
            name_Safety_attribute_value_all=""
        name_Package_attribute_value_all = request.POST.get('name_Package_attribute_value_all')
        if not name_Package_attribute_value_all:
            name_Package_attribute_value_all=""
        name_Model_attribute_value_all = request.POST.get('name_Model_attribute_value_all')
        if not name_Model_attribute_value_all:
            name_Model_attribute_value_all=""
        name_Taste_attribute_value_all = request.POST.get('name_Taste_attribute_value_all')
        if not name_Taste_attribute_value_all:
            name_Taste_attribute_value_all=""
        name_Feel_attribute_value_all = request.POST.get('name_Feel_attribute_value_all')
        if not name_Feel_attribute_value_all:
            name_Feel_attribute_value_all=""
        name_Defferent_Type_attribute_value_all = request.POST.get('name_Defferent_Type_attribute_value_all')
        if not name_Defferent_Type_attribute_value_all:
            name_Defferent_Type_attribute_value_all=""


        variable_MRP_Price = request.POST.get('variable_MRP_Price')
        variable_Cost_Price = request.POST.get('variable_Cost_Price')
        if variable_Cost_Price=='':
            variable_Cost_Price=None

        variable_Discount_Price = request.POST.get('variable_Discount_Price')
        if variable_Discount_Price == '':
            variable_Discount_Price = None


        print("variable_MRP_Price")
        print("variable_MRP_Price")
        print("variable_MRP_Price")
        print("variable_MRP_Price")
        print(variable_MRP_Price)
        print(variable_Cost_Price)
        print(variable_Discount_Price)

        save_attribute_connect_with_product = attribute_connect_with_product(connect_with_product = get_the_Product_name, Size=name_Size_attribute_value_all, Color=name_Color_attribute_value_all, Flavor=name_Flavor_attribute_value_all, Variation=name_Variation_attribute_value_all, Weight=name_Weight_attribute_value_all, Volume= name_Volume_attribute_value_all, Quantity=name_Quantity_attribute_value_all, Values=name_Values_attribute_value_all, Material_Type=name_Material_Type_attribute_value_all, Product_Type=name_Product_Type_attribute_value_all, Verification=name_Verification_attribute_value_all, Quality=name_Quality_attribute_value_all, Marketing_Claims = name_Marketing_Claims_attribute_value_all, Design = name_Design_attribute_value_all, Smell = name_Smell_attribute_value_all, Reliability = name_Reliability_attribute_value_all, Content=name_Content_attribute_value_all, Safety=name_Safety_attribute_value_all, Package=name_Package_attribute_value_all, Model=name_Model_attribute_value_all, Taste= name_Taste_attribute_value_all, Feel=name_Feel_attribute_value_all, Defferent_Type=name_Defferent_Type_attribute_value_all, Cost_Price = variable_Cost_Price, MRP_Price = variable_MRP_Price, Discount_Price = variable_Discount_Price, attribute_image_of_product = url_file4, Attribute_Quantity = variable_qty, Stock_status = stock_status_name)

        save_attribute_connect_with_product.save()

        return redirect('add_attributes', get_the_Product_name.slug)
    else:
        return redirect('deshboard_login')





#changed new


def edit_product_page_add_attribute(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        Add_attribute_full_edited_row_slug = request.POST.get('Add_attribute_full_edited_row_slug')
        print("Add_attribute_full_edited_row_slug")
        print(Add_attribute_full_edited_row_slug)
        print(Add_attribute_full_edited_row_slug)

        Size_attribute__all = Attribute.objects.get(Attribute_name='Size')
        Size_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Size_attribute__all)

        Color_attribute__all = Attribute.objects.get(Attribute_name='Color')
        Color_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Color_attribute__all)

        Flavor_attribute__all = Attribute.objects.get(Attribute_name='Flavor')
        Flavor_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Flavor_attribute__all)

        Variation_attribute__all = Attribute.objects.get(Attribute_name='Variation')
        Variation_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Variation_attribute__all)

        Weight_attribute__all = Attribute.objects.get(Attribute_name='Weight')
        Weight_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Weight_attribute__all)

        Volume_attribute__all = Attribute.objects.get(Attribute_name='Volume')
        Volume_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Volume_attribute__all)

        Quantity_attribute__all = Attribute.objects.get(Attribute_name='Quantity')
        Quantity_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Quantity_attribute__all)

        Values_attribute__all = Attribute.objects.get(Attribute_name='Values')
        Values_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Values_attribute__all)

        Material_Type_attribute__all = Attribute.objects.get(Attribute_name='Material Type')
        Material_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Material_Type_attribute__all)

        Product_Type_attribute__all = Attribute.objects.get(Attribute_name='Product Type')
        Product_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Product_Type_attribute__all)

        Verification_attribute__all = Attribute.objects.get(Attribute_name='Verification')
        Verification_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Verification_attribute__all)

        Quality_attribute__all = Attribute.objects.get(Attribute_name='Quality')
        Quality_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Quality_attribute__all)

        Marketing_Claims_attribute__all = Attribute.objects.get(Attribute_name='Marketing Claims')
        Marketing_Claims_attribute_value_all = Attribute_value.objects.filter(
            Attribute_name=Marketing_Claims_attribute__all)

        Design_attribute__all = Attribute.objects.get(Attribute_name='Design')
        Design_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Design_attribute__all)

        Smell_attribute__all = Attribute.objects.get(Attribute_name='Smell')
        Smell_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Smell_attribute__all)

        Reliability_attribute__all = Attribute.objects.get(Attribute_name='Reliability')
        Reliability_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Reliability_attribute__all)

        Content_attribute__all = Attribute.objects.get(Attribute_name='Content')
        Content_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Content_attribute__all)

        Safety_attribute__all = Attribute.objects.get(Attribute_name='Safety')
        Safety_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Safety_attribute__all)

        Package_attribute__all = Attribute.objects.get(Attribute_name='Package')
        Package_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Package_attribute__all)

        Model_attribute__all = Attribute.objects.get(Attribute_name='Model')
        Model_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Model_attribute__all)

        Taste_attribute__all = Attribute.objects.get(Attribute_name='Taste')
        Taste_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Taste_attribute__all)

        Feel_attribute__all = Attribute.objects.get(Attribute_name='Feel')
        Feel_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Feel_attribute__all)

        Defferent_Type_attribute__all = Attribute.objects.get(Attribute_name='Defferent Type')
        Defferent_Type_attribute_value_all = Attribute_value.objects.filter(Attribute_name=Defferent_Type_attribute__all)

        get_the_Product_name = Products.objects.get(slug=Add_attribute_full_edited_row_slug)

        get_attribute_from_this_perticuler_product = attribute_connect_with_product.objects.filter(connect_with_product = get_the_Product_name)

        print("get_the_Product_name")
        print(get_the_Product_name)

        context = {
            'get_the_Product_name': get_the_Product_name,
            'get_attribute_from_this_perticuler_product':get_attribute_from_this_perticuler_product,
            'Size_attribute_value_all': Size_attribute_value_all,
            'Color_attribute_value_all': Color_attribute_value_all,
            'Flavor_attribute_value_all': Flavor_attribute_value_all,
            'Variation_attribute_value_all': Variation_attribute_value_all,
            'Weight_attribute_value_all': Weight_attribute_value_all,
            'Volume_attribute_value_all': Volume_attribute_value_all,
            'Quantity_attribute_value_all': Quantity_attribute_value_all,
            'Values_attribute_value_all': Values_attribute_value_all,
            'Material_Type_attribute_value_all': Material_Type_attribute_value_all,
            'Product_Type_attribute_value_all': Product_Type_attribute_value_all,
            'Verification_attribute_value_all': Verification_attribute_value_all,
            'Quality_attribute_value_all': Quality_attribute_value_all,
            'Marketing_Claims_attribute_value_all': Marketing_Claims_attribute_value_all,
            'Design_attribute_value_all': Design_attribute_value_all,
            'Smell_attribute_value_all': Smell_attribute_value_all,
            'Reliability_attribute_value_all': Reliability_attribute_value_all,
            'Content_attribute_value_all': Content_attribute_value_all,
            'Safety_attribute_value_all': Safety_attribute_value_all,
            'Package_attribute_value_all': Package_attribute_value_all,
            'Model_attribute_value_all': Model_attribute_value_all,
            'Taste_attribute_value_all': Taste_attribute_value_all,
            'Feel_attribute_value_all': Feel_attribute_value_all,
            'Defferent_Type_attribute_value_all': Defferent_Type_attribute_value_all}

        return render(request, 'edited_add_attribute_form_add_product.html', context)
    else:
        return redirect('deshboard_login')















def dashbord_Add_Brand(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    print(staff_admin)
    if staff_admin or staff_shop_manager or staff_upload_team:
        brand_form = add_brand()
        if request.method == "POST":
            brand_form = add_brand(request.POST, request.FILES)
            if brand_form.is_valid:
                brand_form.save()
                return redirect('dashbord_Add_Brand')
            
        All_Brand = Brand.objects.all()
        CONTEXT = {'All_Brand': All_Brand, 'brand_form':brand_form}
        return render(request, "dashbord_Add_Brand.html", CONTEXT)
    else:
        return redirect('deshboard_login')



def dashbord_Categories(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    print(staff_admin)
    if staff_admin or staff_shop_manager or staff_upload_team:
        form_categories = add_category()
        form_subcategories = add_Subcategory_1()
        form_subcategories_2 = add_Subcategory_2()

        if request.method == 'POST':
            form_categories = add_category(request.POST, request.FILES)
            if form_categories.is_valid():
                form_categories.save()
                messages.success(request, "Successfully Added The Category")
                return redirect('dashbord_Categories')

            form_subcategories = add_Subcategory_1(request.POST)
            if form_subcategories.is_valid():
                form_subcategories.save()
                messages.success(request, "Successfully Added The Subcategory 1")
                return redirect('dashbord_Categories')


            form_subcategories_2 = add_Subcategory_2(request.POST)
            if form_subcategories_2.is_valid():
                form_subcategories_2.save()
                messages.success(request, "Successfully Added The Subcategory 2")
                return redirect('dashbord_Categories')

        # show categories
        get_all_categories = Category.objects.all()
        get_all_subcategories_1 = Subcategory_1.objects.all()
        get_all_subcategories_2 = Subcategory_2.objects.all()

        CONTEXT = {'form_categories': form_categories, 'get_all_categories': get_all_categories,
                   'form_subcategories': form_subcategories, 'form_subcategories_2':form_subcategories_2, 'get_all_subcategories_1': get_all_subcategories_1, 'get_all_subcategories_2':get_all_subcategories_2}
        return render(request, "dashbord_Categories.html", CONTEXT)
    else:
        return redirect('deshboard_login')



def save_brand(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == 'POST':
            try:
                brand_logo = request.FILES['brand_logo']
                brand_name = request.POST.get('brand_name')
                Brand_description = request.POST.get('Brand_description')

                fs = FileSystemStorage()
                filename = fs.save(brand_logo.name, brand_logo)
                uploaded_file_url = fs.url(filename)
                print(filename)
                print(uploaded_file_url)

                making_brand = Brand(Brand_Name=brand_name, Description=Brand_description, Brand_logo=uploaded_file_url)
                making_brand.save()

                messages.success(request, 'Successfully Added Brand !!')

                return redirect('dashbord_Add_Brand')

            except:

                brand_name = request.POST.get('brand_name')
                Brand_description = request.POST.get('Brand_description')

                making_brand = Brand(Brand_Name=brand_name, Description=Brand_description)
                making_brand.save()
                messages.success(request, 'Successfully Added Brand !!')
                return redirect('dashbord_Add_Brand')
    else:
        return redirect('deshboard_login')



@csrf_exempt
def change_status_star(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        product_id = request.POST.get('product_id')
        get_the_prod =Products.objects.get(slug=product_id)
        get_the_prod.make_star=True
        get_the_prod.save()
        return HttpResponse(True)
    else:
        return redirect('deshboard_login')


@csrf_exempt
def change_undo_status_star(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')


    if staff_admin or staff_shop_manager or staff_upload_team:
        product_id = request.POST.get('product_id')
        get_the_prod =Products.objects.get(slug=product_id)
        get_the_prod.make_star=False
        get_the_prod.save()
        return HttpResponse(True)
    else:
        return redirect('deshboard_login')


@csrf_exempt
def delete_the_prod_row(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        product_id = request.POST.get('prod_slug')
        get_the_prod =Products.objects.get(slug=product_id)
        get_the_prod.delete()

        return HttpResponse(True)
    else:
        return redirect('deshboard_login')



def edited_product_page(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        full_edited_row = Products.objects.get(slug=pk)

        prod_main_cat = full_edited_row.Category

        subcat1_lst = Subcategory_1.objects.filter(Category=prod_main_cat)
        print(subcat1_lst)


        lst_scat2 = []
        for scat1 in subcat1_lst:
            print(scat1)
            subcat2_lst = Subcategory_2.objects.filter(Subcategory_1=scat1)

            for subcat2_lst_2 in subcat2_lst:
                print(subcat2_lst)
                lst_scat2.append(subcat2_lst_2)


        i = full_edited_row.TYPE_OF_PRODUCTS
        have_Add_attribute = ""
        if i == 'Variable Product' or i == 'Virtual Product':
            have_Add_attribute = "yes"

        Simple_Product = ""
        Variable_Product = ""
        Virtual_Product_p = ""

        if i == 'Simple Product':
            Simple_Product = "yes"
        if i == 'Variable Product':
            Variable_Product = "yes"
        if i == 'Virtual Product':
            Virtual_Product_p = "yes"

        product_form = edit_product_field(instance=full_edited_row)

        all_main_cats = Category.objects.all()

        u = {"full_edited_row": full_edited_row,
             "product_form": product_form,
             "have_Add_attribute": have_Add_attribute,
             'Simple_Product': Simple_Product,
             'Variable_Product': Variable_Product,
             'Virtual_Product_p': Virtual_Product_p,
             'all_main_cats': all_main_cats,
             'prod_main_cat': prod_main_cat,
             'subcat1_lst': subcat1_lst,
             'lst_scat2': lst_scat2,

             }
        return render(request, 'edit_product_page.html', u)
    else:
        return redirect('deshboard_login')
        



def edit_product_save(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == "POST":

            p_get_slug = request.POST.get('p_get_slug')

            product_full_row = Products.objects.get(slug=p_get_slug)

            product_form = edit_product_field(request.POST, instance=product_full_row)
            if product_form.is_valid():
                product_form.save()

            print("i am here")
            # make_feature_product = request.POST.get('make_feature_product')
            # print('make_feature_product')
            # print(make_feature_product)
            save_edited_Product_name = request.POST.get('save_edited_Product_name')
            TYPE_OF_PRODUCTS_in_edited_dashboard = request.POST.get('TYPE_OF_PRODUCTS_in_edited_dashboard')
            save_edited_SKU = request.POST.get('save_edited_SKU')
            save_edited_MRP_Price = request.POST.get('save_edited_MRP_Price')


            Category_list = request.POST.get('Category_list')

            get_prim_cat = Category.objects.get(id=Category_list)

            suncat1 = request.POST.get('suncat1')
            suncat1 = json.loads(suncat1)
            suncat2 = request.POST.get('suncat2')
            suncat2 = json.loads(suncat2)

            print('suncat1, suncat2')
            print(suncat1, suncat2)

            save_edited_Cost_Price = request.POST.get('save_edited_Cost_Price')
            if save_edited_Cost_Price=='' or save_edited_Cost_Price=='None':
                save_edited_Cost_Price = None
            save_edited_Discount_Price = request.POST.get('save_edited_Discount_Price')
            if save_edited_Discount_Price == '' or save_edited_Discount_Price=='None':
                save_edited_Discount_Price = None

            save_edited_product_quentity = request.POST.get('save_edited_product_quentity')

            save_edited_Meta_Title = request.POST.get('save_edited_Meta_Title')
            save_edited_Meta_Keyword = request.POST.get('save_edited_Meta_Keyword')

            save_edited_Prod_Image = request.FILES.get('save_edited_Prod_Image')
            save_edited_Product_Image_2 = request.FILES.get('save_edited_Product_Image_2')
            save_edited_Product_Image_3 = request.FILES.get('save_edited_Product_Image_3')
            save_edited_Product_Image_4 = request.FILES.get('save_edited_Product_Image_4')
            print("printing image")
            print(save_edited_Prod_Image, save_edited_Product_Image_2, save_edited_Product_Image_3,
                  save_edited_Product_Image_4)

            if save_edited_Prod_Image:
                fs = FileSystemStorage()
                filename = fs.save(save_edited_Prod_Image.name, save_edited_Prod_Image)
                url_file = fs.url(filename)
                print("printing save_edited_Prod_Image")
                print(save_edited_Prod_Image)

                image = Image.open(save_edited_Prod_Image)
                image = image.convert('RGB')
                image.save(f'C:/Users/Abu Sufian/Django Practice/job_universe_IT/Ecommerce_update_5/ecomhat/media/{filename}.webp', 'webp')
                url_file = fs.url(f'{filename}.webp')

            if save_edited_Prod_Image is None:
                url_file = product_full_row.Product_Image

            if save_edited_Product_Image_2:
                fs2 = FileSystemStorage()
                filename2 = fs2.save(save_edited_Product_Image_2.name, save_edited_Product_Image_2)
                url_file_2 = fs2.url(filename2)
                print("printing save_edited_Product_Image_2")
                print(save_edited_Product_Image_2)

                image = Image.open(save_edited_Product_Image_2)
                image = image.convert('RGB')
                image.save(f'C:/Users/Abu Sufian/Django Practice/job_universe_IT/Ecommerce_update_5/ecomhat/media/{filename2}.webp', 'webp')
                url_file_2 = fs2.url(f'{filename2}.webp')

            if save_edited_Product_Image_2 is None:
                url_file_2 = product_full_row.Product_Image2

            if save_edited_Product_Image_3:
                fs3 = FileSystemStorage()
                filename3 = fs3.save(save_edited_Product_Image_3.name, save_edited_Product_Image_3)
                url_file_3 = fs3.url(filename3)

                image = Image.open(save_edited_Product_Image_3)
                image = image.convert('RGB')
                image.save(f'C:/Users/Abu Sufian/Django Practice/job_universe_IT/Ecommerce_update_5/ecomhat/media/{filename3}.webp', 'webp')
                url_file_3 = fs3.url(f'{filename3}.webp')

            if save_edited_Product_Image_3 is None:
                url_file_3 = product_full_row.Product_Image3

            if save_edited_Product_Image_4:
                fs4 = FileSystemStorage()
                filename4 = fs4.save(save_edited_Product_Image_4.name, save_edited_Product_Image_4)
                url_file_4 = fs4.url(filename4)

                image = Image.open(save_edited_Product_Image_4)
                image = image.convert('RGB')
                image.save(f'C:/Users/Abu Sufian/Django Practice/job_universe_IT/Ecommerce_update_5/ecomhat/media/{filename4}.webp', 'webp')
                url_file_4 = fs4.url(f'{filename4}.webp')

            if save_edited_Product_Image_4 is None:
                url_file_4 = product_full_row.Product_Image4

            product_full_row.Product_Name = save_edited_Product_name

            product_full_row.TYPE_OF_PRODUCTS = TYPE_OF_PRODUCTS_in_edited_dashboard

            product_full_row.SKU = save_edited_SKU
            product_full_row.Cost_Price = save_edited_Cost_Price
            product_full_row.MRP_Price = save_edited_MRP_Price
            product_full_row.Discount_Price = save_edited_Discount_Price

            product_full_row.Category = get_prim_cat



            product_full_row.Meta_Title = save_edited_Meta_Title
            product_full_row.Meta_Keyword = save_edited_Meta_Keyword
            product_full_row.Product_Image = url_file
            product_full_row.Product_Image2 = url_file_2
            product_full_row.Product_Image3 = url_file_3
            product_full_row.Product_Image4 = url_file_4
            product_full_row.Product_stock_Quantity = save_edited_product_quentity
            product_full_row.save()


            product_full_row.Subcategory_1.clear()
            for subc1 in suncat1:
                product_full_row.Subcategory_1.add(subc1)


            product_full_row.Subcategory_2.clear()
            for subc2 in suncat2:
                product_full_row.Subcategory_2.add(subc2)

        return redirect('edited_product_page', product_full_row.slug)
    else:
        return redirect('deshboard_login')
    
    
    

def filter_action(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == "POST":
            productorder_length_stock_status = request.POST.get('productorder_length_stock_status')
            productorder_length_Category = request.POST.get('productorder_length_Category')
    
            get_category = Category.objects.get(id=productorder_length_Category)
    
            # get_filter_product = Products.objects.filter(Category=get_category)
            # fatch_filter_action = Products.objects.filter(Stock_status=productorder_length_stock_status)
    
            all_product_show = Products.objects.filter(Category=get_category).filter(Stock_status=productorder_length_stock_status)
    
            all_product_qunt = Products.objects.filter(Category=get_category).filter(Stock_status=productorder_length_stock_status).count()
    
            all_Category = Category.objects.all()
    
    
            context = {'all_product_show':all_product_show, 'all_Category':all_Category, 'all_product_qunt':all_product_qunt}
            return render(request, 'All_Products.html', context)
        return redirect('dashbord_all_product')
    else:
        return redirect('deshboard_login')


@csrf_exempt
def get_sub_cat(request):
    cat_value = request.POST.get('cat_value')
    print(cat_value)
    get_cat_main = Category.objects.get(id=cat_value)
    print('get_cat_main')
    print(get_cat_main)
    all_sub_cat2 = Subcategory_1.objects.filter(Category=get_cat_main)
    print(all_sub_cat2)
    get_subcat_seri = serializers.serialize('json', all_sub_cat2)
    return JsonResponse(get_subcat_seri, safe=False)



@csrf_exempt
def get_sub_cat2(request):
    subcat_value = request.POST.get('subcat_value')
    print(subcat_value)
    get_subcat_main = Subcategory_1.objects.get(id=subcat_value)
    print('get_subcat_main')
    print(get_subcat_main)
    all_sub_category_2 = Subcategory_2.objects.filter(Subcategory_1=get_subcat_main)
    print(all_sub_category_2)
    get_subcat_seri2 = serializers.serialize('json', all_sub_category_2)
    return JsonResponse(get_subcat_seri2, safe=False)


@csrf_exempt
def move_to_trash_selected_checkbox(request):
    prod_uid = request.POST.get('prod_uid')
    print(prod_uid)
    get_prd = Products.objects.get(slug=prod_uid)
    print('get_prd')
    print(get_prd)
    get_prd.delete()
    return HttpResponse(True)


@csrf_exempt
def order_table_change_status(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin:
        rol= staff_admin
    elif staff_shop_manager:
        rol = staff_shop_manager
    elif staff_customer_support:
        rol = staff_customer_support

    print('jj')
    order_id = request.POST.get('order_id')
    bulk_action_id = request.POST.get('bulk_action_id')
    print(order_id, bulk_action_id)
    get_order = Order_Table.objects.get(id=order_id)
    print('get_order')
    print(get_order)

    past_status = get_order.Order_Status

    get_order.Order_Status=bulk_action_id
    get_order.save()

    now_stsus = get_order.Order_Status
    Staff_r = Staff_Access.objects.get(Username=rol)


    log_text = f'Order Status is Changed from - {past_status} to {now_stsus}'
    new_log = order_table_logs(staff_role=Staff_r, order_table_1=get_order, logs_status=log_text)
    new_log.save()

    return HttpResponse(True)
    




def activated_vendors(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        filter_active_vendors = vendor_registration_table.objects.filter(vendor_activation=True)
        
        vendor_entries_num=request.GET.get('vendor_entries_num')
        
        # pagination
        if vendor_entries_num:
            p = Paginator(filter_active_vendors, vendor_entries_num)
        else:
            p = Paginator(filter_active_vendors, 15)
        # print(p.num_pages)
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_vendor = []
        for i in range(1, number_of_pages_1):
            list_vendor.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        page_num = int(page_num)
        
        context={'vendor_list':page, 'list_vendor':list_vendor, 'page_num':page_num, 'vendor_entries_num':vendor_entries_num}
        return render(request, 'activated_vendors.html', context)
    else:
        return redirect('deshboard_login')




@csrf_exempt
def vendor_deactivate(request):
    vendor_id = request.POST.get('vendor_id')
    get_vendor = vendor_registration_table.objects.get(id=vendor_id)
    get_vendor.vendor_activation=False
    get_vendor.save()
    return HttpResponse(True)


def filter_vendor_date(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        vendor_Start_Date_filter = request.GET.get('vendor_Start_Date_filter')
        vendor_End_Date_filter = request.GET.get('vendor_End_Date_filter')
        
        vendor_entries_num = request.GET.get('vendor_entries_num')
        
        vendor_date_search = vendor_registration_table.objects.filter(Q(join_date__range=[vendor_Start_Date_filter, vendor_End_Date_filter])).filter(vendor_activation=True)
        filter_date_vendor_qty = vendor_date_search.count()
        
        
        # pagination
        if vendor_entries_num:
            p = Paginator(vendor_date_search, vendor_entries_num)
        else:
            p = Paginator(vendor_date_search, 15)
        # print(p.num_pages)
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_vendor_date = []
        for i in range(1, number_of_pages_1):
            list_vendor_date.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        page_num2 = int(page_num)
        
        entries_filter_vendor_date = True
        
        
        context={'vendor_Start_Date_filter':vendor_Start_Date_filter, 'vendor_End_Date_filter':vendor_End_Date_filter, 'vendor_list':page, 'filter_date_vendor_qty':filter_date_vendor_qty, 'page_num2':page_num2, 'list_vendor_date':list_vendor_date, 'entries_filter_vendor_date':entries_filter_vendor_date, 'vendor_entries_num':vendor_entries_num}
        return render(request, 'activated_vendors.html', context)
    else:
        return redirect('deshboard_login')



def search_vendor_other(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        search_status = request.GET.get('search_status')
        search_input_vendor = request.GET.get('search_input_vendor')
        
        vendor_entries_num = request.GET.get('vendor_entries_num')
        
        if search_status=='0':
            vendor_other_search = vendor_registration_table.objects.filter(Q(vendor_name__icontains=search_input_vendor) | Q(vendor_shop_name__icontains=search_input_vendor) | Q(vendor_phone_no__icontains=search_input_vendor) | Q(vendor_email__icontains=search_input_vendor)).filter(vendor_activation=True).order_by('-id')
        else:
            vendor_other_search = vendor_registration_table.objects.filter(Q(vendor_name__icontains=search_input_vendor) | Q(vendor_shop_name__icontains=search_input_vendor) | Q(vendor_phone_no__icontains=search_input_vendor) | Q(vendor_email__icontains=search_input_vendor)).filter(vendor_activation=True)
        
        
        other_search_qty = vendor_other_search.count()
        
        
        
        # pagination
        if vendor_entries_num:
            p = Paginator(vendor_other_search, vendor_entries_num)
        else:
            p = Paginator(vendor_other_search, 15)
        # print(p.num_pages)
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_vendor_other = []
        for i in range(1, number_of_pages_1):
            list_vendor_other.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        page_num3 = int(page_num)
        
        entries_filter_vendor_other= True
        
        context={'search_status':search_status, 'search_input_vendor':search_input_vendor, 'vendor_list':page, 'other_search_qty':other_search_qty, 'list_vendor_other':list_vendor_other, 'page_num3':page_num3, 'entries_filter_vendor_other':entries_filter_vendor_other, 'vendor_entries_num':vendor_entries_num}
        return render(request, 'activated_vendors.html', context)
    else:
        return redirect('deshboard_login')
    
    
    


def pending_vendors(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        filter_pending_vendors = vendor_registration_table.objects.filter(vendor_activation=False)
        vendor_entries_num=request.GET.get('vendor_entries_num')
        
        # pagination
        if vendor_entries_num:
            p = Paginator(filter_pending_vendors, vendor_entries_num)
        else:
            p = Paginator(filter_pending_vendors, 15)
        # print(p.num_pages)
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_vendor = []
        for i in range(1, number_of_pages_1):
            list_vendor.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        page_num = int(page_num)
        
        context={'vendor_list':page, 'list_vendor':list_vendor, 'page_num':page_num, 'vendor_entries_num':vendor_entries_num}
        return render(request, 'pending_vendors.html', context)
    else:
        return redirect('deshboard_login')
    





@csrf_exempt
def vendor_activate(request):
    vendor_id = request.POST.get('vendor_id')
    get_vendor = vendor_registration_table.objects.get(id=vendor_id)
    get_vendor.vendor_activation=True
    get_vendor.save()
    return HttpResponse(True)




def filter_vendor_date_deactive(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        vendor_Start_Date_filter = request.GET.get('vendor_Start_Date_filter')
        vendor_End_Date_filter = request.GET.get('vendor_End_Date_filter')
        
        vendor_entries_num = request.GET.get('vendor_entries_num')
        
        vendor_date_search = vendor_registration_table.objects.filter(Q(join_date__range=[vendor_Start_Date_filter, vendor_End_Date_filter])).filter(vendor_activation=False)
        filter_date_vendor_qty = vendor_date_search.count()
        
        
        # pagination
        if vendor_entries_num:
            p = Paginator(vendor_date_search, vendor_entries_num)
        else:
            p = Paginator(vendor_date_search, 15)
        # print(p.num_pages)
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_vendor_date = []
        for i in range(1, number_of_pages_1):
            list_vendor_date.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        page_num2 = int(page_num)
        
        entries_filter_vendor_date = True
        
        
        context={'vendor_Start_Date_filter':vendor_Start_Date_filter, 'vendor_End_Date_filter':vendor_End_Date_filter, 'vendor_list':page, 'filter_date_vendor_qty':filter_date_vendor_qty, 'page_num2':page_num2, 'list_vendor_date':list_vendor_date, 'entries_filter_vendor_date':entries_filter_vendor_date, 'vendor_entries_num':vendor_entries_num}
        return render(request, 'pending_vendors.html', context)
    else:
        return redirect('deshboard_login')




def search_vendor_other_deactive(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        search_status = request.GET.get('search_status')
        search_input_vendor = request.GET.get('search_input_vendor')
        
        vendor_entries_num = request.GET.get('vendor_entries_num')
        
        if search_status=='0':
            vendor_other_search = vendor_registration_table.objects.filter(Q(vendor_name__icontains=search_input_vendor) | Q(vendor_shop_name__icontains=search_input_vendor) | Q(vendor_phone_no__icontains=search_input_vendor) | Q(vendor_email__icontains=search_input_vendor)).filter(vendor_activation=False).order_by('-id')
        else:
            vendor_other_search = vendor_registration_table.objects.filter(Q(vendor_name__icontains=search_input_vendor) | Q(vendor_shop_name__icontains=search_input_vendor) | Q(vendor_phone_no__icontains=search_input_vendor) | Q(vendor_email__icontains=search_input_vendor)).filter(vendor_activation=False)
        
        
        other_search_qty = vendor_other_search.count()
        
        
        
        # pagination
        if vendor_entries_num:
            p = Paginator(vendor_other_search, vendor_entries_num)
        else:
            p = Paginator(vendor_other_search, 15)
        # print(p.num_pages)
        
    
        #show list of pages
        number_of_pages_1 = p.num_pages+1
        list_vendor_other = []
        for i in range(1, number_of_pages_1):
            list_vendor_other.append(i)
    
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
            
        page_num3 = int(page_num)
        
        entries_filter_vendor_other= True
        
        context={'search_status':search_status, 'search_input_vendor':search_input_vendor, 'vendor_list':page, 'other_search_qty':other_search_qty, 'list_vendor_other':list_vendor_other, 'page_num3':page_num3, 'entries_filter_vendor_other':entries_filter_vendor_other, 'vendor_entries_num':vendor_entries_num}
        return render(request, 'pending_vendors.html', context)
    else:
        return redirect('deshboard_login')
    
    


def add_vendors_by_upload(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method=='POST':
            Vendor_registration_Full_Name = request.POST.get('Vendor_registration_Full_Name')
            vendor_registration_address = request.POST.get('vendor_registration_address')
            vendor_registration_Shop_Name = request.POST.get('vendor_registration_Shop_Name')
            vendor_registration_Shop_URL = request.POST.get('vendor_registration_Shop_URL')
            vendor_shop_logo = request.FILES.get('vendor_shop_logo')
            vendor_shop_Banner = request.FILES.get('vendor_shop_Banner')
            vendor_registration_Phone_No = request.POST.get('vendor_registration_Phone_No')
            vendor_registration_Email = request.POST.get('vendor_registration_Email')
            vendor_registration_Password = request.POST.get('vendor_registration_Password')
            vendor_registration_Retype_Password = request.POST.get('vendor_registration_Retype_Password')
            vendor_cheack_upload = request.POST.get('vendor_cheack_upload')
            print("vendor_cheack_upload")
            print(vendor_cheack_upload)
    
            erorr_message = ""
    
            filter_email = vendor_registration_table.objects.filter(vendor_email=vendor_registration_Email)
            filter_phone_no = vendor_registration_table.objects.filter(vendor_phone_no=vendor_registration_Phone_No)
    
            if filter_email:
                erorr_message = "email is already exist !"
    
            elif filter_phone_no:
                erorr_message = "Phone number is already exist !"
    
            elif vendor_registration_Password != vendor_registration_Retype_Password:
                erorr_message = "Password dosn't match !"
    
            dic_value_register = {
                'erorr_message': erorr_message,
                'Vendor_registration_Full_Name': Vendor_registration_Full_Name,
                'vendor_registration_Shop_Name': vendor_registration_Shop_Name,
                'vendor_registration_Shop_URL': vendor_registration_Shop_URL,
                'vendor_registration_Phone_No': vendor_registration_Phone_No,
                'vendor_registration_Email': vendor_registration_Email,
                'vendor_registration_address': vendor_registration_address,

            }
            #
            if erorr_message:
                return render(request, 'add_vendors_by_upload.html', dic_value_register)
            else:
                print("main image 1")
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
    
                if vendor_cheack_upload == "on":
                    activations_c_value = True
                else:
                    activations_c_value = False
    
                s = vendor_registration_table(vendor_name=Vendor_registration_Full_Name,
                                              vendor_address=vendor_registration_address,
                                              vendor_shop_name=vendor_registration_Shop_Name,
                                              vendor_shop_url=vendor_registration_Shop_URL,
                                              vendor_phone_no=vendor_registration_Phone_No,
                                              vendor_email=vendor_registration_Email,
                                              vendor_password=g,
                                              vendor_shop_logo=url_file,
                                              vendor_shop_banner=url_file2,
                                              vendor_activation = activations_c_value
    
                                              )
                s.save()
                success_message = "Account is successfully created"
    
                return render(request, 'add_vendors_by_upload.html', {'success_message': success_message})
    
    
        return render(request, 'add_vendors_by_upload.html')
    else:
        return redirect('deshboard_login')
    
    
    
    
def upload_vendor_Store_details(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        row_value_of_vendor = vendor_registration_table.objects.get(vendor_phone_no=pk)
        return render(request, 'upload_vendor_Store_details.html', {'row_value_of_vendor':row_value_of_vendor})
    else:
        return redirect('deshboard_login')
        
        

def upload_vendor_info_edit(request, pk2):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        row_value_of_vendor_edit = vendor_registration_table.objects.get(vendor_phone_no=pk2)
        return render(request, 'upload_vendor_info_edit.html', {'row_value_of_vendor_edit':row_value_of_vendor_edit})
    else:
        return redirect('deshboard_login')
    
    
    
def upload_save_vendor_info_edit(request, pk3):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        save_e_n = request.POST.get('save_edited_Vendor_registration_Full_Name')
        save_e_n_s_n = request.POST.get('save_edited_vendor_registration_Shop_Name')
        save_e_n_r_s = request.POST.get('save_edited_vendor_registration_Shop_URL')
        save_edited_vendor_registration_Addresse = request.POST.get('save_edited_vendor_registration_Address')
        save_e_n_r_p = request.POST.get('save_edited_vendor_registration_Phone_No')
        save_e_n_r_e = request.POST.get('save_edited_vendor_registration_Email')
        save_e_logo = request.FILES.get('save_edited_vendor_logo')
        save_e_venner = request.FILES.get('save_edited_vendor_banner')
        
        fertrd_vendr = request.POST.get('fertrd_vendr')
    
        if save_e_logo:
            print("image 1")
            fss = FileSystemStorage()
            filename = fss.save(save_e_logo.name, save_e_logo)
            url_file = fss.url(filename)
        else:
            url_file = ''
    
        if save_e_venner:
            fsss = FileSystemStorage()
            filename2 = fsss.save(save_e_venner.name, save_e_venner)
            url_file2 = fsss.url(filename2)
        else:
            url_file2 = ''
    
        save_row_value_of_vendor_edit = vendor_registration_table.objects.get(vendor_phone_no=pk3)
        save_row_value_of_vendor_edit.vendor_name = save_e_n
        save_row_value_of_vendor_edit.vendor_shop_name = save_e_n_s_n
        save_row_value_of_vendor_edit.vendor_shop_url = save_e_n_r_s

        save_row_value_of_vendor_edit.vendor_address = save_edited_vendor_registration_Addresse

        save_row_value_of_vendor_edit.vendor_phone_no = save_e_n_r_p
        save_row_value_of_vendor_edit.vendor_email = save_e_n_r_e
        
        if fertrd_vendr:
            save_row_value_of_vendor_edit.featured_vendor = True
        else:
            save_row_value_of_vendor_edit.featured_vendor = False
    
        if save_e_logo:
            save_row_value_of_vendor_edit.vendor_shop_logo = url_file
    
        if save_e_venner:
            save_row_value_of_vendor_edit.vendor_shop_banner = url_file2
    
        save_row_value_of_vendor_edit.save()
    
        pk = save_e_n_r_p
    
        return redirect('upload_vendor_Store_details', pk)
    else:
        return redirect('deshboard_login')




def upload_vendor_info_password_edit(request, pk4):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        return render(request, 'save_vendor_info_edit_password.html', {'pk4':pk4})
    else:
        return redirect('deshboard_login')





def upload_save_vendor_info_password_edit(request, pk4):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        erorr_message = ""
        save_e_u_n_passs = request.POST.get('upload_save_edited_new_vendor_registration_Password')
        save_e_n_u_retype_passs = request.POST.get('upload_save_edited_new_vendor_registration_Retype_Password')
    
        if save_e_u_n_passs == save_e_n_u_retype_passs:
            save_row_pass_value_of_vendor_edit = vendor_registration_table.objects.get(vendor_phone_no=pk4)
            save_e_u_n_passs_g = make_password(save_e_u_n_passs)
            save_row_pass_value_of_vendor_edit.vendor_password = save_e_u_n_passs_g
            save_row_pass_value_of_vendor_edit.save()
    
        else:
            erorr_message="your password dosn't match"
            return render(request, 'save_vendor_info_edit_password.html', {'pk4': pk4, 'erorr_message':erorr_message})
        pk = pk4
        return redirect('upload_vendor_Store_details', pk)
    else:
        return redirect('deshboard_login')
        
        
        
        
        
        
#for delete brands       
def dashboard_brand_deleted(request, dashboard_brand_deleted_pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        get_dashboard_brand_for_deleted = Brand.objects.get(slug=dashboard_brand_deleted_pk)
        get_dashboard_brand_for_deleted.delete()
        return redirect('dashbord_Add_Brand')
    else:
        return redirect('deshboard_login')



#Brand edited function
def dashboard_brand_edit(request, dashboard_brand_edit_pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        get_dashboard_brand_edit = Brand.objects.get(slug = dashboard_brand_edit_pk)

        brand_edit = add_brand(instance=get_dashboard_brand_edit)

        if request.method == "POST":
            brand_edit = add_brand(request.POST, request.FILES, instance=get_dashboard_brand_edit)
            if brand_edit.is_valid():
                brand_edit.save()
                return redirect('dashboard_brand_edit', dashboard_brand_edit_pk)

        print("get_dashboard_brand_edit")
        print(get_dashboard_brand_edit)
        print(get_dashboard_brand_edit.Brand_Name)

        context = {'get_dashboard_brand_edit':get_dashboard_brand_edit, 'brand_edit':brand_edit}

        return render(request, 'dashboard_brand_edit.html', context)
    else:
        return redirect('deshboard_login')
    
    
def dashboard_customer_order_edit(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support:
        get_ordr_tbl = Order_Table.objects.get(id=pk)
        filter_ordr_tbl_2 = Order_Table_2.objects.filter(Order_Id=get_ordr_tbl)

        invoice_var = pk

        filter_logs = order_table_logs.objects.filter(order_table_1=get_ordr_tbl).order_by('-id')

        context = {'get_ordr_tbl':get_ordr_tbl, 'filter_ordr_tbl_2':filter_ordr_tbl_2, 'filter_logs':filter_logs, 'invoice_var':invoice_var}
        return render(request, 'dashboard_customer_order_edit.html', context)
    else:
        return redirect('deshboard_login')


def submit_edited_order(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support:
        ordr_tble_id_get = request.POST.get('ordr_tble_id_get')


        # billing adrees
        ordr_first_name = request.POST.get('ordr_first_name')
        ordr_last_name = request.POST.get('ordr_last_name')
        ordr_street_address = request.POST.get('ordr_street_address')
        ordr_town_city = request.POST.get('ordr_town_city')
        ordr_distric = request.POST.get('ordr_distric')
        ordr_customer_zip = request.POST.get('ordr_customer_zip')

        ordr_customer_email = request.POST.get('ordr_customer_email')
        ordr_customer_phone = request.POST.get('ordr_customer_phone')


        # order other option
        status_order = request.POST.get('status_order')
        delivery_optin = request.POST.get('delivery_optin')
        ordr_shipping_note = request.POST.get('ordr_shipping_note')


        charge_odr = request.POST.get('charge_odr')

        change_type_deli_crg = int(charge_odr)


        overright_orderID_name = request.POST.get('overright_orderID_name')

        get_ordr_tbl = Order_Table.objects.get(id=ordr_tble_id_get)

        var_odr_status = get_ordr_tbl.Order_Status
        var_odr_shipping = get_ordr_tbl.Shopping

        var_odr_shipping_note = get_ordr_tbl.shipping_note

        if var_odr_shipping_note:
            print('ok')
        else:
            var_odr_shipping_note = ""

        var_odr_delivry_chrg = get_ordr_tbl.Delivery_Charge


        if staff_admin:
            staff_role = request.session.get('deshboard_admin_username')
        elif staff_shop_manager:
            staff_role = staff_shop_manager
        elif staff_customer_support:
            staff_role = staff_customer_support

        get_staff_row = Staff_Access.objects.get(Username=staff_role)

        # save other options
        if var_odr_status != status_order:
            get_ordr_tbl.Order_Status = status_order
            get_ordr_tbl.save()

            log_text = f'Order Status is Changed from - {var_odr_status} to {status_order}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if var_odr_shipping != delivery_optin:
            get_ordr_tbl.Shopping = delivery_optin
            get_ordr_tbl.save()
            log_text = f'Order Delivery Option Changed from {var_odr_shipping} to {delivery_optin}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if var_odr_shipping_note != ordr_shipping_note:
            get_ordr_tbl.shipping_note = ordr_shipping_note
            get_ordr_tbl.save()

            log_text = f'Shipping Note is Edited from ({var_odr_shipping_note}) to ({ordr_shipping_note})'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if var_odr_delivry_chrg != change_type_deli_crg:
            get_ordr_tbl.Delivery_Charge = change_type_deli_crg
            get_ordr_tbl.save()

            log_text = f'Delivery Charge Changed From {var_odr_delivry_chrg} to {charge_odr}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        customer_detail_id = get_ordr_tbl.Customer_delivery_information.id

        get_customr_row = Customer_delivery_information.objects.get(id=customer_detail_id)


        past_f_name = get_customr_row.First_Name
        past_l_name = get_customr_row.Last_Name
        past_street_address = get_customr_row.Street_Address
        past_town_city = get_customr_row.Town_City
        past_district = get_customr_row.District
        past_zip = get_customr_row.Post_Code
        past_email = get_customr_row.Email_Address
        past_phone = get_customr_row.Phone_Number

        if past_f_name != ordr_first_name:
            get_customr_row.First_Name=ordr_first_name
            get_customr_row.save()

            log_text = f'First Name is Changed From {past_f_name} to {ordr_first_name}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_l_name != ordr_last_name:
            get_customr_row.Last_Name=ordr_last_name
            get_customr_row.save()

            log_text = f'Last Name is Changed From {past_l_name} to {ordr_last_name}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_street_address != ordr_street_address:
            get_customr_row.Street_Address=ordr_street_address
            get_customr_row.save()

            log_text = f'Street Address is Changed From {past_street_address} to {ordr_street_address}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_town_city != ordr_town_city:
            get_customr_row.Town_City=ordr_town_city
            get_customr_row.save()

            log_text = f'Town City is Changed From {past_town_city} to {ordr_town_city}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_district != ordr_distric:
            get_customr_row.District=ordr_distric
            get_customr_row.save()

            log_text = f'Distric is Changed From {past_district} to {ordr_distric}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_zip != ordr_customer_zip:
            get_customr_row.Post_Code=ordr_customer_zip
            get_customr_row.save()

            log_text = f'Zip Code is Changed From {past_zip} to {ordr_customer_zip}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_email != ordr_customer_email:
            get_customr_row.Email_Address=ordr_customer_email
            get_customr_row.save()

            log_text = f'Email is Changed From {past_email} to {ordr_customer_email}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()

        if past_phone != ordr_customer_phone:
            get_customr_row.Phone_Number=ordr_customer_phone
            get_customr_row.save()

            log_text = f'Phone Number is Changed From {past_phone} to {ordr_customer_phone}'
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl, logs_status=log_text)
            new_log.save()



        # if overright_orderID_name == '1':
        #     messages.success(request, "You Are Overighting The New Order ID !")
        # else:
        #     messages.success(request, f"Updated SuccessFully {overright_orderID_name} !")

        return redirect('dashboard_customer_order_edit', get_ordr_tbl.id)
    else:
        return redirect('deshboard_login')


def delete_item_from_order(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support:
        if staff_admin:
            stf_role = staff_admin
        elif staff_shop_manager:
            stf_role = staff_shop_manager
        elif staff_customer_support:
            stf_role = staff_customer_support

        get_staff_row = Staff_Access.objects.get(Username=stf_role)

        newget_ordr_tbl2 = Order_Table_2.objects.get(id=pk)
        main_ordr_id = newget_ordr_tbl2.Order_Id.id

        mainordr_ordr_id = newget_ordr_tbl2.Order_Id.Order_Id

        ordr2_prod = newget_ordr_tbl2.Product.Product_Name



        get_ordr_tbl2 = Order_Table_2.objects.get(id=pk)
        get_ordr_tbl2.delete()



        log_text = f'Item {ordr2_prod} is Delete From Order ID {mainordr_ordr_id}'
        delete_new_log = order_table_logs(staff_role=get_staff_row, order_table_1=newget_ordr_tbl2.Order_Id, logs_status=log_text)
        delete_new_log.save()

        return redirect('dashboard_customer_order_edit', main_ordr_id)
    else:
        return redirect('deshboard_login')
    


@csrf_exempt    
def update_ordr_prdtble2(request):
    prod_order_uid = request.POST.get('prod_order_uid')
    
    vid_order_status = request.POST.get('vid_order_status')
    vid_prod_qty = request.POST.get('vid_prod_qty')
    vid_order_newID = request.POST.get('vid_order_newID')

    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin:
        stff_role=staff_admin
    elif staff_shop_manager:
        stff_role = staff_shop_manager
    elif staff_customer_support:
        stff_role = staff_customer_support
    
    get_staff_row = Staff_Access.objects.get(Username=stff_role)
    
    get_ordr_tbl2 = Order_Table_2.objects.get(id=prod_order_uid)
    past_qty_ordr = get_ordr_tbl2.Quantity
    ordr_prod = get_ordr_tbl2.Product
    order_ID_usr = get_ordr_tbl2.Order_Id
    
    then_price_ordr = get_ordr_tbl2.then_price
    
    
    if past_qty_ordr != vid_prod_qty:
        get_ordr_tbl2.Quantity=vid_prod_qty
        get_ordr_tbl2.SubTotal_Price = then_price_ordr*int(vid_prod_qty)
        get_ordr_tbl2.save()
        
        log_text = f'Order ID - {order_ID_usr} Changed Quantity from {past_qty_ordr} to {vid_prod_qty} Of Product - {ordr_prod} '
        
        new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl2.Order_Id, logs_status=log_text)
        new_log.save()
    
    
    filter_ordr_tbl2 = Order_Table_2.objects.filter(New_Order_Id=vid_order_newID)
    
    
    order_id_db = get_ordr_tbl2.Order_Id.Order_Id
    
    if vid_order_newID==order_id_db:
        messages.success(request, "Updated SuccessFully !")
        return HttpResponse(False)
        
    else:
        if filter_ordr_tbl2:
            messages.success(request, "You Are Overighting The New Order ID !")
            return HttpResponse(True)
            
        else:
            get_ordr_tbl2.New_Order_Id=vid_order_newID
            get_ordr_tbl2.New_Order_Status=vid_order_status
            get_ordr_tbl2.save()
            
            log_text = f'Order ID - {order_ID_usr}: Added New Order ID To {vid_order_newID} and Order Status {vid_order_status} Of Product - {ordr_prod}'
        
            new_log = order_table_logs(staff_role=get_staff_row, order_table_1=get_ordr_tbl2.Order_Id, logs_status=log_text)
            new_log.save()
            
            messages.success(request, "Added New Order ID SuccessFully !")
            return HttpResponse(False)
            
            
            

# all analitics code here

# code for Overview

def Analytics_Overview(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        if request.method=="POST":
            name_analitics_overview = request.POST.get('name_analitics_overview')
            name_analitics_overview_cam_name = request.POST.get('name_analitics_overview_cam_name')

            if name_analitics_overview=="All":
                get_row_grand_total_count = Order_Table.objects.all()
                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)

                get_ordr2_all = Order_Table_2.objects.all()

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)

                highst_qty_prd = Products.objects.all().order_by('-total_quantity_of_sell_product')[:10]
                highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell')[:10]

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'highst_qty_prd':highst_qty_prd,
                    'highst_qty_cat':highst_qty_cat,
                    'name_analitics_overview':name_analitics_overview,
                }
                return render(request, 'Analytics_Overview.html', contex)


            elif name_analitics_overview=="Reguler":
                get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign__isnull=True)
                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)

                get_ordr2_all = Order_Table_2.objects.filter(Campaign__isnull=True)

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)

                highst_qty_prd = Products.objects.all().order_by('-total_quantity_of_sell_reguler_product')[:10]
                highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell_reguler')[:10]

                reguler=True

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'highst_qty_prd':highst_qty_prd,
                    'highst_qty_cat':highst_qty_cat,
                    'name_analitics_overview':name_analitics_overview,
                    'reguler':reguler,
                }
                return render(request, 'Analytics_Overview.html', contex)





            elif name_analitics_overview=="Campaign":


                all_campaign_list = campaign_table.objects.all().order_by('-id')

                if name_analitics_overview_cam_name:
                    last_campaign_list = campaign_table.objects.get(id=name_analitics_overview_cam_name)
                else:
                    last_campaign_list = campaign_table.objects.last()

                get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign=last_campaign_list)
                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)

                get_ordr2_all = Order_Table_2.objects.filter(Campaign=last_campaign_list)

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)

                cam_highst_qty_prd = campaign_product_table.objects.filter(campaign=last_campaign_list).order_by('-total_quantity_of_sell_campaign_product')[:10]
                cam_highst_qty_cat = campaign_categories_percentage.objects.filter(campaign=last_campaign_list).order_by('-total_quantity_of_sell_cat_campaign')[:10]

                campaign=True

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'cam_highst_qty_prd':cam_highst_qty_prd,
                    'cam_highst_qty_cat':cam_highst_qty_cat,
                    'name_analitics_overview':name_analitics_overview,
                    'campaign':campaign,
                    'all_campaign_list':all_campaign_list,
                    'last_campaign_list':last_campaign_list,

                }
                return render(request, 'Analytics_Overview.html', contex)

        else:
            get_row_grand_total_count = Order_Table.objects.all()

            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()
            print("total_order_count")
            print(total_order_count)

            get_ordr2_all = Order_Table_2.objects.all()

            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()
            print("item_product")
            print(item_product)

            highst_qty_prd = Products.objects.all().order_by('-total_quantity_of_sell_product')[:10]
            highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell')[:10]

            contex={
                'net_sell_count_addition':net_sell_count_addition,
                'grand_total_count_addition':grand_total_count_addition,
                'item_product':item_product,
                'total_order_count':total_order_count,
                'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                'highst_qty_prd':highst_qty_prd,
                'highst_qty_cat':highst_qty_cat,
            }
            return render(request, 'Analytics_Overview.html', contex)
    else:
        return redirect('deshboard_login')








# code for Products

def Analytics_Products(request, template='Analytics_Products.html', page_template='Analytics_Products_new.html'):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        if request.method == "POST":
            name_analitics_prod = request.POST.get('name_analitics_prod')
            name_analitics_overview_cam_name = request.POST.get('name_analitics_overview_cam_name')

            if name_analitics_prod=="All":
                get_row_grand_total_count = Order_Table.objects.all()
                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)

                get_ordr2_all = Order_Table_2.objects.all()

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)

                highst_qty_prd = Products.objects.all().order_by('-total_quantity_of_sell_product')
                highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell')[:10]

                total_prod = highst_qty_prd.count()

                context={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'highst_qty_prd':highst_qty_prd,
                    'highst_qty_cat':highst_qty_cat,
                    'total_prod':total_prod,
                    'page_template':page_template,
                }
                if request.is_ajax():
                    template = page_template
                return render(request, template, context)




            elif name_analitics_prod=="Reguler":
                get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign__isnull=True)
                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)

                get_ordr2_all = Order_Table_2.objects.filter(Campaign__isnull=True)

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)

                highst_qty_prd = Products.objects.all().order_by('-total_quantity_of_sell_reguler_product')
                highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell_reguler')[:10]

                total_prod = highst_qty_prd.count()

                reguler=True

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'highst_qty_prd':highst_qty_prd,
                    'highst_qty_cat':highst_qty_cat,
                    'name_analitics_prod':name_analitics_prod,
                    'reguler':reguler,
                    'total_prod':total_prod,
                    'page_template':page_template,
                }

                if request.is_ajax():
                    template = page_template
                return render(request, template, contex)




            elif name_analitics_prod=="Campaign":
                all_campaign_list = campaign_table.objects.all().order_by('-id')

                if name_analitics_overview_cam_name:
                    last_campaign_list = campaign_table.objects.get(id=name_analitics_overview_cam_name)
                else:
                    last_campaign_list = campaign_table.objects.last()

                get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign=last_campaign_list)
                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)

                get_ordr2_all = Order_Table_2.objects.filter(Campaign=last_campaign_list)

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)

                highst_qty_prd = campaign_product_table.objects.filter(campaign=last_campaign_list).order_by('-total_quantity_of_sell_campaign_product')
                cam_highst_qty_cat = campaign_categories_percentage.objects.filter(campaign=last_campaign_list).order_by('-total_quantity_of_sell_cat_campaign')[:10]

                total_prod = highst_qty_prd.count()

                campaign=True

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'highst_qty_prd':highst_qty_prd,
                    'cam_highst_qty_cat':cam_highst_qty_cat,
                    'name_analitics_prod':name_analitics_prod,
                    'campaign':campaign,
                    'all_campaign_list':all_campaign_list,
                    'last_campaign_list':last_campaign_list,
                    'total_prod':total_prod,
                    'page_template':page_template,
                }

                if request.is_ajax():
                    template = page_template
                return render(request, template, contex)
        else:
            get_row_grand_total_count = Order_Table.objects.all()

            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()
            print("total_order_count")
            print(total_order_count)

            get_ordr2_all = Order_Table_2.objects.all()

            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()
            print("item_product")
            print(item_product)

            highst_qty_prd = Products.objects.all().order_by('-total_quantity_of_sell_product')
            highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell')[:10]

            total_prod = highst_qty_prd.count()

            context={
                'net_sell_count_addition':net_sell_count_addition,
                'grand_total_count_addition':grand_total_count_addition,
                'item_product':item_product,
                'total_order_count':total_order_count,
                'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                'highst_qty_prd':highst_qty_prd,
                'highst_qty_cat':highst_qty_cat,
                'total_prod':total_prod,
                'page_template':page_template,
            }

            if request.is_ajax():
                template = page_template
            return render(request, template, context)
    else:
        return redirect('deshboard_login')
        





# code for Categories
def Analytics_Categories(request, template='Analytics_Categories.html', page_template='Analytics_Categories_new.html'):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        if request.method == "POST":
            name_analitics_cat = request.POST.get('name_analitics_cat')
            name_analitics_overview_cam_name = request.POST.get('name_analitics_overview_cam_name')


            cat_Start_Date_filter = request.POST.get('cat_Start_Date_filter')
            cat_End_Date_filter = request.POST.get('cat_End_Date_filter')

            date_filter=False

            if name_analitics_cat=="All":
                if cat_Start_Date_filter and cat_End_Date_filter:
                    get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter]))
                else:
                    get_row_grand_total_count = Order_Table.objects.all()

                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)


                if cat_Start_Date_filter and cat_End_Date_filter:
                    get_ordr2_all = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter]))
                else:
                    get_ordr2_all = Order_Table_2.objects.all()


                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)


                list_1_filrt_dt=None
                a=None


                if cat_Start_Date_filter and cat_End_Date_filter:
                    a = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter]))

                    cat_list = []
                    cat_lc = 0



                    for i in a:
                        if i.Product.Category in cat_list:
                            pass
                        else:
                            cat_list.append(i.Product.Category)
                            cat_lc = cat_lc+1



                    list_1_filrt_dt = []
                    for jj in cat_list:
                        bbbb = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Category=jj)

                        total_qtycat=0
                        total_mneycat=0
                        for yyuyyy in bbbb:
                            total_qtycat = total_qtycat + yyuyyy.Quantity
                            total_mneycat = total_mneycat + yyuyyy.SubTotal_Price


                        prod_calcul_date=0
                        lstprod_calcul_date=[]

                        for i in bbbb:
                            if i.Product in lstprod_calcul_date:
                                pass
                            else:
                                lstprod_calcul_date.append(i.Product)
                                prod_calcul_date = prod_calcul_date + 1


                        odr_calcul_date=0
                        lstodr_calcul_date=[]

                        for i in bbbb:
                            if i.Order_Id.Order_Id in lstodr_calcul_date:
                                pass
                            else:
                                lstodr_calcul_date.append(i.Order_Id.Order_Id)
                                odr_calcul_date = odr_calcul_date + 1


                        list_1_filrt_dt.append([jj, total_qtycat, total_mneycat, prod_calcul_date, odr_calcul_date])

                    highst_qty_cat = list_1_filrt_dt

                    total_cat = cat_lc

                    date_filter=True
                else:
                    highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell')

                    total_cat = highst_qty_cat.count()

                context={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                    'highst_qty_cat':highst_qty_cat,
                    'total_cat':total_cat,
                    'name_analitics_cat':name_analitics_cat,
                    'page_template': page_template,
                    'cat_Start_Date_filter':cat_Start_Date_filter,
                    'cat_End_Date_filter':cat_End_Date_filter,
                    'list_1_filrt_dt':list_1_filrt_dt,
                    'date_filter':date_filter,
                }


                if request.is_ajax():
                    template = page_template

                return render(request, template, context)


            elif name_analitics_cat=="Reguler":

                if cat_Start_Date_filter and cat_End_Date_filter:
                    get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Order_Campaign__isnull=True)
                else:
                    get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign__isnull=True)


                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)


                if cat_Start_Date_filter and cat_End_Date_filter:
                    get_ordr2_all = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Campaign__isnull=True)
                else:
                    get_ordr2_all = Order_Table_2.objects.filter(Campaign__isnull=True)

                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)





                list_1_filrt_dt=None
                a=None


                if cat_Start_Date_filter and cat_End_Date_filter:
                    a = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Campaign__isnull=True)

                    cat_list = []
                    cat_lc = 0



                    for i in a:
                        if i.Product.Category in cat_list:
                            pass
                        else:
                            cat_list.append(i.Product.Category)
                            cat_lc = cat_lc+1



                    list_1_filrt_dt = []
                    for jj in cat_list:
                        bbbb = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Category=jj).filter(Campaign__isnull=True)

                        total_qtycat=0
                        total_mneycat=0
                        for yyuyyy in bbbb:
                            total_qtycat = total_qtycat + yyuyyy.Quantity
                            total_mneycat = total_mneycat + yyuyyy.SubTotal_Price


                        prod_calcul_date=0
                        lstprod_calcul_date=[]

                        for i in bbbb:
                            if i.Product in lstprod_calcul_date:
                                pass
                            else:
                                lstprod_calcul_date.append(i.Product)
                                prod_calcul_date = prod_calcul_date + 1


                        odr_calcul_date=0
                        lstodr_calcul_date=[]

                        for i in bbbb:
                            if i.Order_Id.Order_Id in lstodr_calcul_date:
                                pass
                            else:
                                lstodr_calcul_date.append(i.Order_Id.Order_Id)
                                odr_calcul_date = odr_calcul_date + 1


                        list_1_filrt_dt.append([jj, total_qtycat, total_mneycat, prod_calcul_date, odr_calcul_date])

                    highst_qty_cat = list_1_filrt_dt

                    total_cat = cat_lc

                    date_filter=True
                else:

                    highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell_reguler')
                    total_cat = highst_qty_cat.count()


                reguler=True

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,

                    'highst_qty_cat':highst_qty_cat,
                    'name_analitics_cat':name_analitics_cat,
                    'reguler':reguler,
                    'total_cat':total_cat,
                    'page_template': page_template,
                    'cat_Start_Date_filter':cat_Start_Date_filter,
                    'cat_End_Date_filter':cat_End_Date_filter,
                    'list_1_filrt_dt':list_1_filrt_dt,
                    'date_filter':date_filter,
                }

                if request.is_ajax():
                    template = page_template

                return render(request, template, contex)



            elif name_analitics_cat=="Campaign":

                all_campaign_list = campaign_table.objects.all().order_by('-id')

                if name_analitics_overview_cam_name:
                    last_campaign_list = campaign_table.objects.get(id=name_analitics_overview_cam_name)
                else:
                    last_campaign_list = campaign_table.objects.last()



                if cat_Start_Date_filter and cat_End_Date_filter:
                    get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                else:
                    get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign=last_campaign_list)



                grand_total_count_addition = 0
                net_sell_count_addition = 0

                for i in get_row_grand_total_count:
                    grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

                for i in get_row_grand_total_count:
                    net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

                total_order_count = get_row_grand_total_count.count()
                print("total_order_count")
                print(total_order_count)


                if cat_Start_Date_filter and cat_End_Date_filter:
                    get_ordr2_all = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Campaign=last_campaign_list)
                else:
                    get_ordr2_all = Order_Table_2.objects.filter(Campaign=last_campaign_list)


                get_row_grand_total_count_Quantity=0

                for i in get_ordr2_all:
                    get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

                print(get_row_grand_total_count_Quantity)

                item_product = get_ordr2_all.count()
                print("item_product")
                print(item_product)


                list_1_filrt_dt=None
                a=None


                if cat_Start_Date_filter and cat_End_Date_filter:
                    a = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Campaign=last_campaign_list)

                    cat_list = []
                    cat_lc = 0

                    for i in a:
                        if i.Product.Category in cat_list:
                            pass
                        else:
                            cat_list.append(i.Product.Category)
                            cat_lc = cat_lc+1



                    list_1_filrt_dt = []
                    for jj in cat_list:
                        bbbb = Order_Table_2.objects.filter(Q(Order_Date__range=[cat_Start_Date_filter, cat_End_Date_filter])).filter(Category=jj).filter(Campaign=last_campaign_list)

                        total_qtycat=0
                        total_mneycat=0
                        for yyuyyy in bbbb:
                            total_qtycat = total_qtycat + yyuyyy.Quantity
                            total_mneycat = total_mneycat + yyuyyy.SubTotal_Price


                        prod_calcul_date=0
                        lstprod_calcul_date=[]

                        for i in bbbb:
                            if i.Product in lstprod_calcul_date:
                                pass
                            else:
                                lstprod_calcul_date.append(i.Product)
                                prod_calcul_date = prod_calcul_date + 1


                        odr_calcul_date=0
                        lstodr_calcul_date=[]

                        for i in bbbb:
                            if i.Order_Id.Order_Id in lstodr_calcul_date:
                                pass
                            else:
                                lstodr_calcul_date.append(i.Order_Id.Order_Id)
                                odr_calcul_date = odr_calcul_date + 1


                        list_1_filrt_dt.append([jj, total_qtycat, total_mneycat, prod_calcul_date, odr_calcul_date])

                    highst_qty_cat = list_1_filrt_dt

                    total_cat = cat_lc

                    date_filter=True
                else:

                    highst_qty_cat = campaign_categories_percentage.objects.filter(campaign=last_campaign_list).order_by('-total_quantity_of_sell_cat_campaign')
                    total_cat = highst_qty_cat.count()


                campaign=True

                contex={
                    'net_sell_count_addition':net_sell_count_addition,
                    'grand_total_count_addition':grand_total_count_addition,
                    'item_product':item_product,
                    'total_order_count':total_order_count,
                    'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,

                    'highst_qty_cat':highst_qty_cat,
                    'name_analitics_cat':name_analitics_cat,
                    'campaign':campaign,
                    'all_campaign_list':all_campaign_list,
                    'last_campaign_list':last_campaign_list,
                    'total_cat':total_cat,
                    'page_template': page_template,
                    'cat_Start_Date_filter':cat_Start_Date_filter,
                    'cat_End_Date_filter':cat_End_Date_filter,
                    'list_1_filrt_dt':list_1_filrt_dt,
                    'date_filter':date_filter,
                }

                if request.is_ajax():
                    template = page_template

                return render(request, template, contex)




        else:
            get_row_grand_total_count = Order_Table.objects.all()

            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()
            print("total_order_count")
            print(total_order_count)

            get_ordr2_all = Order_Table_2.objects.all()

            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()
            print("item_product")
            print(item_product)


            highst_qty_cat = Category.objects.all().order_by('-total_quantity_of_sell')

            total_cat = highst_qty_cat.count()

            context={
                'net_sell_count_addition':net_sell_count_addition,
                'grand_total_count_addition':grand_total_count_addition,
                'item_product':item_product,
                'total_order_count':total_order_count,
                'get_row_grand_total_count_Quantity':get_row_grand_total_count_Quantity,
                'highst_qty_cat':highst_qty_cat,
                'total_cat':total_cat,
                'page_template': page_template,
            }

            if request.is_ajax():
                template = page_template
            return render(request, template, context)
    else:
        return redirect('deshboard_login')



# code for Revenue
def Analytics_Revenue(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        get_row_grand_total_count = Order_Table.objects.all()

        grand_total_count_addition = 0
        net_sell_count_addition = 0
        total_shipping_chrg = 0

        for i in get_row_grand_total_count:
            grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price
            total_shipping_chrg = total_shipping_chrg + i.Delivery_Charge

        for i in get_row_grand_total_count:
            net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

        total_order_count = get_row_grand_total_count.count()
        print("total_order_count")
        print(total_order_count)

        get_ordr2_all = Order_Table_2.objects.all()

        get_row_grand_total_count_Quantity=0

        for i in get_ordr2_all:
            get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

        print(get_row_grand_total_count_Quantity)

        item_product = get_ordr2_all.count()

        context = {'grand_total_count_addition':grand_total_count_addition, 'net_sell_count_addition':net_sell_count_addition, 'total_shipping_chrg':total_shipping_chrg}
        return render(request, 'Analytics_Revenue.html', context)
    else:
        return redirect('deshboard_login')
    
    
    
def Analytics_orders(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        name_analitics_ordr = request.GET.get('name_analitics_ordr')
        name_analitics_overview_cam_name = request.GET.get('name_analitics_overview_cam_name')

        order_Start_Date_filter = request.GET.get('order_Start_Date_filter')
        order_End_Date_filter = request.GET.get('order_End_Date_filter')

        name_analitics_ordr_status = request.GET.get('name_analitics_ordr_status')


        if name_analitics_ordr == "All":
            if order_Start_Date_filter and order_End_Date_filter:
                if name_analitics_ordr_status:
                    if name_analitics_ordr_status=="All":
                        get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Pending payment":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Pending payment").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Partially Paid":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Partially Paid").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Ready To Ship":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Ready To Ship").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Processing":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Processing").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Completed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Completed").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Cancelled":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Cancelled").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Refunded":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Refunded").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="Picked":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Picked").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
                    elif name_analitics_ordr_status=="On hold":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="On hold").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))

                    elif name_analitics_ordr_status=="Failed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Failed").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))

                else:
                    get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))


            else:
                if name_analitics_ordr_status:
                    if name_analitics_ordr_status=="All":
                        get_row_grand_total_count = Order_Table.objects.all()
                    elif name_analitics_ordr_status=="Pending payment":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Pending payment")
                    elif name_analitics_ordr_status=="Partially Paid":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Partially Paid")
                    elif name_analitics_ordr_status=="Ready To Ship":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Ready To Ship")
                    elif name_analitics_ordr_status=="Processing":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Processing")
                    elif name_analitics_ordr_status=="Completed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Completed")
                    elif name_analitics_ordr_status=="Cancelled":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Cancelled")
                    elif name_analitics_ordr_status=="Refunded":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Refunded")
                    elif name_analitics_ordr_status=="Picked":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Picked")
                    elif name_analitics_ordr_status=="On hold":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="On hold")

                    elif name_analitics_ordr_status=="Failed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Failed")


                else:
                    get_row_grand_total_count = Order_Table.objects.all()

            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()


            if order_Start_Date_filter and order_End_Date_filter:
                get_ordr2_all = Order_Table_2.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter]))
            else:
                get_ordr2_all = Order_Table_2.objects.all()


            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()

            if net_sell_count_addition==0:
                average_odr_value = 0
            else:
                average_odr_value = net_sell_count_addition/total_order_count

            # if get_row_grand_total_count_Quantity==0:
            #     Average_Item_Per_Order = 0
            # else:
            #     Average_Item_Per_Order = get_row_grand_total_count_Quantity/total_order_count

            context = {'total_order_count':total_order_count, 'net_sell_count_addition':net_sell_count_addition, 'average_odr_value':average_odr_value, 'name_analitics_ordr':name_analitics_ordr, 'order_Start_Date_filter':order_Start_Date_filter, 'order_End_Date_filter':order_End_Date_filter, 'name_analitics_ordr_status':name_analitics_ordr_status}
            return render(request, 'Analytics_orders.html', context)


        elif name_analitics_ordr == "Reguler":
            if order_Start_Date_filter and order_End_Date_filter:

                if name_analitics_ordr_status:
                    if name_analitics_ordr_status=="All":
                        get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Pending payment":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Pending payment").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Partially Paid":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Partially Paid").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Ready To Ship":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Ready To Ship").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Processing":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Processing").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Completed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Completed").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Cancelled":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Cancelled").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Refunded":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Refunded").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Picked":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Picked").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="On hold":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="On hold").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)

                    elif name_analitics_ordr_status=="Failed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Failed").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)

                else:
                    get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign__isnull=True)


            else:
                if name_analitics_ordr_status:
                    if name_analitics_ordr_status=="All":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Pending payment":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Pending payment").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Partially Paid":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Partially Paid").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Ready To Ship":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Ready To Ship").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Processing":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Processing").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Completed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Completed").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Cancelled":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Cancelled").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Refunded":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Refunded").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="Picked":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Picked").filter(Order_Campaign__isnull=True)
                    elif name_analitics_ordr_status=="On hold":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="On hold").filter(Order_Campaign__isnull=True)

                    elif name_analitics_ordr_status=="Failed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Failed").filter(Order_Campaign__isnull=True)


                else:
                    get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign__isnull=True)



            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()


            if order_Start_Date_filter and order_End_Date_filter:
                get_ordr2_all = Order_Table_2.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Campaign__isnull=True)
            else:
                get_ordr2_all = Order_Table_2.objects.filter(Campaign__isnull=True)

            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()


            if net_sell_count_addition == 0:
                average_odr_value = 0
            else:
                average_odr_value = net_sell_count_addition/total_order_count

            # if get_row_grand_total_count_Quantity == 0:
            #     Average_Item_Per_Order = 0
            # else:

            #     Average_Item_Per_Order = get_row_grand_total_count_Quantity/total_order_count

            context = {'total_order_count':total_order_count, 'net_sell_count_addition':net_sell_count_addition, 'average_odr_value':average_odr_value, 'name_analitics_ordr':name_analitics_ordr, 'order_Start_Date_filter':order_Start_Date_filter, 'order_End_Date_filter':order_End_Date_filter, 'name_analitics_ordr_status':name_analitics_ordr_status}
            return render(request, 'Analytics_orders.html', context)

        elif name_analitics_ordr == "Campaign":
            all_campaign_list = campaign_table.objects.all().order_by('-id')

            if name_analitics_overview_cam_name:
                last_campaign_list = campaign_table.objects.get(id=name_analitics_overview_cam_name)
            else:
                last_campaign_list = campaign_table.objects.last()


            if order_Start_Date_filter and order_End_Date_filter:

                if name_analitics_ordr_status:
                    if name_analitics_ordr_status=="All":
                        get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Pending payment":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Pending payment").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Partially Paid":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Partially Paid").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Ready To Ship":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Ready To Ship").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Processing":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Processing").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Completed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Completed").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Cancelled":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Cancelled").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Refunded":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Refunded").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Picked":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Picked").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="On hold":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="On hold").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)

                    elif name_analitics_ordr_status=="Failed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Failed").filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)

                else:
                    get_row_grand_total_count = Order_Table.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Order_Campaign=last_campaign_list)


            else:
                if name_analitics_ordr_status:
                    if name_analitics_ordr_status=="All":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Pending payment":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Pending payment").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Partially Paid":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Partially Paid").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Ready To Ship":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Ready To Ship").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Processing":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Processing").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Completed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Completed").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Cancelled":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Cancelled").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Refunded":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Refunded").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="Picked":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Picked").filter(Order_Campaign=last_campaign_list)
                    elif name_analitics_ordr_status=="On hold":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="On hold").filter(Order_Campaign=last_campaign_list)

                    elif name_analitics_ordr_status=="Failed":
                        get_row_grand_total_count = Order_Table.objects.filter(Order_Status="Failed").filter(Order_Campaign=last_campaign_list)


                else:

                    get_row_grand_total_count = Order_Table.objects.filter(Order_Campaign=last_campaign_list)


            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()




            if order_Start_Date_filter and order_End_Date_filter:
                get_ordr2_all = Order_Table_2.objects.filter(Q(Order_Date__range=[order_Start_Date_filter, order_End_Date_filter])).filter(Campaign=last_campaign_list)
            else:
                get_ordr2_all = Order_Table_2.objects.filter(Campaign=last_campaign_list)

            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()

            campaign = True


            if net_sell_count_addition==0:
                average_odr_value = 0
            else:
                average_odr_value = net_sell_count_addition/total_order_count

            # if get_row_grand_total_count_Quantity==0:
            #     Average_Item_Per_Order = 0
            # else:
            #     Average_Item_Per_Order = get_row_grand_total_count_Quantity/total_order_count

            context = {'total_order_count':total_order_count, 'net_sell_count_addition':net_sell_count_addition, 'average_odr_value':average_odr_value, 'all_campaign_list':all_campaign_list, 'campaign':campaign, 'last_campaign_list':last_campaign_list, 'name_analitics_ordr':name_analitics_ordr, 'order_Start_Date_filter':order_Start_Date_filter, 'order_End_Date_filter':order_End_Date_filter, 'name_analitics_ordr_status':name_analitics_ordr_status}
            return render(request, 'Analytics_orders.html', context)


        else:
            get_row_grand_total_count = Order_Table.objects.all()

            grand_total_count_addition = 0
            net_sell_count_addition = 0

            for i in get_row_grand_total_count:
                grand_total_count_addition = grand_total_count_addition + i.GrandTotal_Price

            for i in get_row_grand_total_count:
                net_sell_count_addition = net_sell_count_addition + i.SubTotal_Price

            total_order_count = get_row_grand_total_count.count()


            get_ordr2_all = Order_Table_2.objects.all()

            get_row_grand_total_count_Quantity=0

            for i in get_ordr2_all:
                get_row_grand_total_count_Quantity = get_row_grand_total_count_Quantity + i.Quantity

            print(get_row_grand_total_count_Quantity)

            item_product = get_ordr2_all.count()


            if net_sell_count_addition==0:
                average_odr_value = 0
            else:
                average_odr_value = net_sell_count_addition/total_order_count

            # if get_row_grand_total_count_Quantity==0:
            #     Average_Item_Per_Order = 0
            # else:
            #     Average_Item_Per_Order = get_row_grand_total_count_Quantity/total_order_count

            context = {'total_order_count':total_order_count, 'net_sell_count_addition':net_sell_count_addition, 'average_odr_value':average_odr_value, 'name_analitics_ordr':name_analitics_ordr}
            return render(request, 'Analytics_orders.html', context)
    else:
        return redirect('deshboard_login')



def Analytics_brands(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        return render(request, 'Analytics_brands.html')
    else:
        return redirect('deshboard_login')

def Analytics_vendor(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager:
        return render(request, 'Analytics_vendor.html')
    else:
        return redirect('deshboard_login')

#dashboard customers code here


def dashboard_Add_customer(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        return render(request, 'dashboard_Add_customer.html')
    else:
        return redirect('deshboard_login')
    
    

def dashboard_customer_id_making(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        First_Name = request.POST.get("First_Name")
        Last_Name = request.POST.get("Last_Name")
        Phone_number = request.POST.get("Phone_number")
        sign_email = request.POST.get("sign_email")
        sing_Password = request.POST.get("sing_Password")
        sign_Confirm_Password = request.POST.get("sign_Confirm_Password")

        deshboard_user_mobile_match_with_database = User.objects.filter(username = Phone_number)
        deshboard_email_match_with_database = User.objects.filter(email = sign_email)

        print(deshboard_user_mobile_match_with_database)

        massage = ""
        if deshboard_user_mobile_match_with_database:
            massage = "Phone number is already exists"

        else:
            if deshboard_email_match_with_database:
                massage = "Email is already exists"

            else:
                if sign_Confirm_Password != sing_Password:
                    massage = "Password dosn't match"

                else:

                    myuser1 = User.objects.create_user(Phone_number, sign_email, sing_Password)
                    myuser1.first_name = First_Name
                    myuser1.last_name = Last_Name
                    myuser1.is_active = True
                    myuser1.save()

                    massage = "New customer created successfully"
                    return render(request, 'dashboard_Add_customer.html', {'massage':massage})

        contex = {'First_Name':First_Name, 'Last_Name':Last_Name, 'Phone_number':Phone_number, 'sign_email':sign_email, 'sing_Password':sing_Password, 'sign_Confirm_Password':sign_Confirm_Password, 'massage':massage}


        return render(request, 'dashboard_Add_customer.html', contex)
    else:
        return redirect('deshboard_login')



    

def dashboard_view_all_customer(request, template='dashboard_view_all_customer.html', page_template='dashboard_view_all_customer_new.html'):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')


    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        var_all_users_show = User.objects.all()

        var_all_users_show_count = var_all_users_show.count()

        contex = {'var_all_users_show':var_all_users_show,
                  'var_all_users_show_count':var_all_users_show_count,
                  'page_template': page_template,
                  }

        if request.is_ajax():
            template = page_template
        return render(request, template, contex)
    else:
        return redirect('deshboard_login')



def dashboard_customer_profile_edit(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        print("pk")
        print(pk)
        get_dashboard_customer_profile_edit_from_user = User.objects.get(username = pk)
        print(get_dashboard_customer_profile_edit_from_user.username)
        c = get_dashboard_customer_profile_edit_from_user.password
        return render(request, 'dashboard_customer_profile_edit.html', {'pk':pk, 'get_dashboard_customer_profile_edit_from_user':get_dashboard_customer_profile_edit_from_user })
    else:
        return redirect('deshboard_login')


def resave_user_info_dashboard_customer_profile_edit(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        First_Name = request.POST.get("First_Name")
        Last_Name = request.POST.get("Last_Name")
        Phone_number = request.POST.get("Phone_number")
        sign_email = request.POST.get("sign_email")
        sing_Password = request.POST.get("sing_Password")
        pk = request.POST.get("pk")
        print("pk")
        print(pk)
        if sing_Password:
            new_all_users_show = User.objects.get(username=pk)

            new_all_users_show.first_name = First_Name
            new_all_users_show.last_name = Last_Name
            new_all_users_show.username = Phone_number
            new_all_users_show.email = sign_email
            h = make_password(sing_Password)
            new_all_users_show.password = h
            new_all_users_show.save()

        else:
            new_all_users_show = User.objects.get(username = pk)

            new_all_users_show.first_name = First_Name
            new_all_users_show.last_name = Last_Name
            new_all_users_show.username = Phone_number
            new_all_users_show.email = sign_email
            new_all_users_show.save()

        return redirect('dashboard_view_all_customer')
    else:
        return redirect('deshboard_login')
  
    
    
    
    
    
    

def dashbord_Attribute(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        all_Attribute_value = Attribute.objects.all()
        contex = {'all_Attribute_value':all_Attribute_value}
        return render(request, "dashbord_Attribute.html", contex)
    else:
        return redirect('deshboard_login')



def dashbord_Attribute_save(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == 'POST':
            try:
                Attribute_name = request.POST.get('Attribute_name')
                Attribute_slag = request.POST.get('Attribute_slag')
                Attribute_description = request.POST.get('Attribute_description')
                if Attribute_slag:
                    Attribute_slag =Attribute_slag
                else:
                    Attribute_slag = Attribute_name
                save_dashbord_Attribute_save = Attribute(Attribute_name = Attribute_name, Attribute_slag = Attribute_slag, Attribute_description = Attribute_description)
                save_dashbord_Attribute_save.save()
                return redirect("dashbord_Attribute")
            except:
                return redirect("dashbord_Attribute")

        return redirect("dashbord_Attribute")
    else:
        return redirect('deshboard_login')




def edit_dashbord_Attribute_save(request, pk_edit_dashbord_Attribute_save):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        one_row_of_edit_Attribute_value = Attribute.objects.get( id =pk_edit_dashbord_Attribute_save)
        contex = {'one_row_of_edit_Attribute_value':one_row_of_edit_Attribute_value}
        return render(request, "edit_dashbord_Attribute_save.html", contex)
    else:
        return redirect('deshboard_login')


def edited_dashbord_Attribute_save_final(request, pk_edited_save_again):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == 'POST':
            edited_Attribute_name = request.POST.get('edited_Attribute_name')
            edited_Attribute_slag = request.POST.get('edited_Attribute_slag')
            edited_Attribute_description = request.POST.get('edited_Attribute_description')

            if edited_Attribute_slag:
                edited_Attribute_slag =edited_Attribute_slag
            else:
                edited_Attribute_slag = edited_Attribute_name

            get_the_row_of_preveoius = Attribute.objects.get( id  = pk_edited_save_again)

            get_the_row_of_preveoius.Attribute_name = edited_Attribute_name
            get_the_row_of_preveoius.Attribute_slag = edited_Attribute_slag
            get_the_row_of_preveoius.Attribute_description = edited_Attribute_description
            get_the_row_of_preveoius.save()

        return redirect("dashbord_Attribute")
    else:
        return redirect('deshboard_login')



def value_dashbord_Attribute(request, pk_value_dashbord_Attribute):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        one_row_of_pk_value_dashbord_Attribute = Attribute.objects.get(id=pk_value_dashbord_Attribute)
        one_row_of_pk_value_dashbord_Attribute_value = Attribute_value.objects.filter(Attribute_name = one_row_of_pk_value_dashbord_Attribute)


        print("one_row_of_pk_value_dashbord_Attribute")
        print(one_row_of_pk_value_dashbord_Attribute.Attribute_description)
        print(one_row_of_pk_value_dashbord_Attribute.Attribute_name)

        contex_yy = {'one_row_of_pk_value_dashbord_Attribute': one_row_of_pk_value_dashbord_Attribute, 'one_row_of_pk_value_dashbord_Attribute_value':one_row_of_pk_value_dashbord_Attribute_value}


        return render(request, "value_dashbord_Attribute.html", contex_yy)
    else:
        return redirect('deshboard_login')


def save_value_of_attribute(request, pk_Attribute_value_dashbord_Attribute):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == 'POST':
            row_pk_Attribute_value_dashbord_Attribute = Attribute.objects.get(id = pk_Attribute_value_dashbord_Attribute)

            Attribute_value_1 = request.POST.get('Attribute_value_1')
            value_Attribute_slag_1 = request.POST.get('value_Attribute_slag_1')
            value_Attribute_description_1 = request.POST.get('value_Attribute_description_1')

            if value_Attribute_slag_1:
                value_Attribute_slag_1 = value_Attribute_slag_1
            else:
                value_Attribute_slag_1 = Attribute_value_1

            save_value_to_database = Attribute_value(Attribute_name =row_pk_Attribute_value_dashbord_Attribute, Attribute_value_slag = value_Attribute_slag_1, Attribute_value_description = value_Attribute_description_1, Attribute_value = Attribute_value_1)
            save_value_to_database.save()


            return redirect('value_dashbord_Attribute', pk_Attribute_value_dashbord_Attribute)

        return render(request, "value_dashbord_Attribute.html")
    else:
        return redirect('deshboard_login')




def dashboard_attribute_value_delete(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        one_row_of_pk_value_dashbord_Attribute_id = request.POST.get('one_row_of_pk_value_dashbord_Attribute_id')
        template_all_Attribute_value_id = request.POST.get('template_all_Attribute_value_id')
        row_dashboard_attribute_value_delete = Attribute_value.objects.get(id = template_all_Attribute_value_id)
        row_dashboard_attribute_value_delete.delete()

        return redirect('value_dashbord_Attribute', one_row_of_pk_value_dashbord_Attribute_id)
    else:
        return redirect('deshboard_login')


def dashboard_attribute_value_edit(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_upload_team:
        one_row_of_pk_value_dashbord_Attribute_id_for_edit = request.POST.get('one_row_of_pk_value_dashbord_Attribute_id_for_edit')
        template_all_Attribute_value_id_for_edit = request.POST.get('template_all_Attribute_value_id_for_edit')

        row_pk_Attribute_value_dashbord_Attributerr = Attribute_value.objects.get(id=template_all_Attribute_value_id_for_edit)
        context_6 = {
            'one_row_of_pk_value_dashbord_Attribute_id_for_edit':one_row_of_pk_value_dashbord_Attribute_id_for_edit,
            'row_pk_Attribute_value_dashbord_Attributerr':row_pk_Attribute_value_dashbord_Attributerr,
            'template_all_Attribute_value_id_for_edit':template_all_Attribute_value_id_for_edit


        }
        return render(request, 'save_dashboard_attribute_value_edit.html', context_6)
    else:
        return redirect('deshboard_login')



def save_dashboard_attribute_value_edit(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        main_attribute_id = request.POST.get('main_attribute_id')
        main_attribute_value_id = request.POST.get('main_attribute_value_id')
        edited_Attribute_value_1 = request.POST.get('edited_Attribute_value_1')
        edited_value_Attribute_slag_1 = request.POST.get('edited_value_Attribute_slag_1')
        edited_value_Attribute_description_1 = request.POST.get('edited_value_Attribute_description_1')

        print("Attribute_value")
        print(Attribute_value)
        print(Attribute_value)

        get_edited_Attribute_value = Attribute_value.objects.get(id=main_attribute_value_id)
        get_edited_Attribute = Attribute.objects.get(id=main_attribute_id)
        get_edited_Attribute_value.Attribute =get_edited_Attribute
        get_edited_Attribute_value.Attribute_value =edited_Attribute_value_1
        get_edited_Attribute_value.Attribute_value_slag =edited_value_Attribute_slag_1
        get_edited_Attribute_value.Attribute_value_description =edited_value_Attribute_description_1
        get_edited_Attribute_value.save()


        return redirect('value_dashbord_Attribute', main_attribute_id)
    else:
        return redirect('deshboard_login')








    
    
    

def deshboard_customer_find_by_search(request, template='dashboard_view_all_customer.html', page_template='dashboard_view_all_customer_new.html'):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        get_find_by_search = request.POST.get('find_by_search')
        var_all_users_show_phon = User.objects.filter(username__icontains = get_find_by_search)
        var_all_users_show_email = User.objects.filter(email__icontains = get_find_by_search)
        if var_all_users_show_phon:
            print("i am in phone")
            var_all_users_show = var_all_users_show_phon
        elif var_all_users_show_email:
            print("i am in email")
            var_all_users_show = var_all_users_show_email
        else:
            print("Not match")
            var_all_users_show = []

        contex = {'var_all_users_show': var_all_users_show,
                  'page_template': page_template,
                  }

        if request.is_ajax():
            template = page_template
        return render(request, template, contex)
    else:
        return redirect('deshboard_login')



def deshboard_product_find_by_search(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team or staff_upload_team:
        get_find_by_search_product = request.POST.get('find_by_search_Product_Name')


        all_product_show = Products.objects.filter(Product_Name__icontains = get_find_by_search_product)
        all_product_qunt = Products.objects.all().count()

        all_Category = Category.objects.all()
        print(all_Category)

        order_entries = request.GET.get('order_entries')

        # pagination
        if order_entries:
            p = Paginator(all_product_show, order_entries)
        else:
            p = Paginator(all_product_show, 20)

        # show list of pages
        number_of_pages_1 = p.num_pages + 1
        list_prod = []
        for i in range(1, number_of_pages_1):
            list_prod.append(i)

        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        all_product_show = page

        page_num = int(page_num)

        context = {'all_product_show': all_product_show, 'all_Category': all_Category, 'all_product_qunt': all_product_qunt,
                   'page_num': page_num, 'all_product_show': all_product_show, 'list_prod': list_prod,
                   'order_entries': order_entries}
        return render(request, "All_Products.html", context)
    else:
        return redirect('deshboard_login')
    
    
    
       
    
    
    
    
    
    

# start pdf code here


from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.colors import Color, black, blue, red

def dashboard_customer_order_edit_Generate_Invoice1(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # p.drawString((+)left, (+)Top, "Hello world.")
        p.drawString(320, 780, "Boom Boom Shopping")
        p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
        p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
        p.drawString(320, 735, "Phone : 09642601538")
        p.drawString(320, 720, "Mail: support@boomboom.com.bd")


        i = 'https://idjangoo.com/static/images/logo-main.png'
        p.drawImage(i, 40, 730, width=270, height=72)
        u ='kkk'
        p.setFont("Helvetica", 25)
        p.drawString(40, 655, "INVOICE")
        p.setFont("Helvetica", 12)
        p.drawString(300, 630, "Order:"+u)
        p.drawString(300, 618, "Date:")
        p.drawString(300, 606, "Payment:")
        p.drawString(300, 594, "Method:")

        p.drawString(40, 630, "Method:")
        p.drawString(40, 618, "Method:")
        p.drawString(40, 606, "Method:")
        p.drawString(40, 594, "Method:")
        p.drawString(40, 582, "Method:")
        p.drawString(40, 570, "Method:")

        # color(r,g,b, alpha)
        red50transparent = Color(0, 0, 205, alpha=0.2)
        Yellow = Color(205, 205, 0, alpha=1)
        p.setFillColor(Yellow)
        p.rect(40, 510, 520, 30, fill=True, stroke=False)

        p.setFillColor(black)
        p.drawString(70, 520, "Product")
        p.setFillColor(black)
        p.drawString(300, 520, "Quantity")
        p.setFillColor(black)
        p.drawString(450, 520, "Price")


        p.line(0, 60, 600, 60)

        p.setFillColor(blue)
        p.drawString(190, 45, "Thank you for shopping with BoomBoom")
        p.drawString(241, 30, "We Deliver Quality")
        p.drawString(225, 15, "WWW.boomboom.com.bd")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response
    else:
        return redirect('deshboard_login')
    

    
   


    
# end pdf code here



# start pdf code here it's for single invoice

from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.colors import Color, black, blue, red

#single system for one invoice making proccess is here start

# def dashboard_customer_order_edit_Generate_Invoice(request, pk):

#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
    
#     #ar necar la lekhla sorasore dawonlode korbe
#     # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'          
#     response['Content-Disposition'] = 'filename="somefilename.pdf"'

#     # Create the PDF object, using the response object as its "file."
#     p = canvas.Canvas(response)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     # p.drawString((+)left, (+)Top, "Hello world.")
#     p.drawString(320, 780, "Boom Boom Shopping")
#     p.drawString(320, 765, "House-11, Road-18, Flat-6E, Sector-04")
#     p.drawString(320, 750, "Uttara, Dhaka-1230, Bangladesh")
#     p.drawString(320, 735, "Phone : 09642601538")
#     p.drawString(320, 720, "Mail: support@boomboom.com.bd")
    
    
#     i = 'https://idjangoo.com/static/images/logo-main.png'
#     p.drawImage(i, 40, 730, width=270, height=72)
#     u ='kkk'
#     p.setFont("Helvetica", 25)
#     p.drawString(40, 655, "INVOICE")
#     p.setFont("Helvetica", 12)
#     p.drawString(300, 630, "Order:"+u)
#     p.drawString(300, 618, "Date:")
#     p.drawString(300, 606, "Payment:")
#     p.drawString(300, 594, "Method:")
    
#     p.drawString(40, 630, "Method:")
#     p.drawString(40, 618, "Method:")
#     p.drawString(40, 606, "Method:")
#     p.drawString(40, 594, "Method:")
#     p.drawString(40, 582, "Method:")
#     p.drawString(40, 570, "Method:")
    
#     # color(r,g,b, alpha)
#     red50transparent = Color(0, 0, 205, alpha=0.2)
#     Yellow = Color(205, 205, 0, alpha=1)
#     p.setFillColor(Yellow)
#     p.rect(40, 510, 520, 30, fill=True, stroke=False)
    
#     p.setFillColor(black)
#     p.drawString(70, 520, "Product")
#     p.setFillColor(black)
#     p.drawString(300, 520, "Quantity")
#     p.setFillColor(black)
#     p.drawString(450, 520, "Price")

#     Invoice_get_ordr_tbl = Order_Table.objects.get(id=pk)
#     Invoice_filter_ordr_tbl_2 = Order_Table_2.objects.filter(Order_Id=Invoice_get_ordr_tbl)


#     print("Invoice_filter_ordr_tbl_2")
#     print("Invoice_filter_ordr_tbl_2")
#     Product_list = []
#     Quantity_list = []
#     SubTotal_Price_list = []



#     for i in Invoice_filter_ordr_tbl_2:

#         if i.New_Order_Status:
#             pass

#         else:
#             Product_list.append(i.Product)
#             Quantity_list.append(i.Quantity)
#             SubTotal_Price_list.append(i.SubTotal_Price)

#     print("Product_list")
#     print(Product_list)


#     position_Product_list =490
#     for r in Product_list:
#         p.drawString(70, position_Product_list, str(r))

#         position_Product_list = position_Product_list-20


#     position_Quantity_list = 490
#     for r in Quantity_list:
#         p.drawString(300, position_Quantity_list, str(r))

#         position_Quantity_list = position_Quantity_list - 20


#     position_SubTotal_Price_list = 490
#     for r in SubTotal_Price_list:
#         p.drawString(450, position_SubTotal_Price_list, str(r))

#         position_SubTotal_Price_list = position_SubTotal_Price_list - 20

#     line_position_Quantity_list = position_Quantity_list+15
#     p.line(250, line_position_Quantity_list, 600, line_position_Quantity_list)
#     p.drawString(300, position_Quantity_list, "subtotal")
#     position_Quantity_list = position_Quantity_list - 20
#     p.drawString(300, position_Quantity_list, "shipping")
#     position_Quantity_list = position_Quantity_list - 20
#     line_position_Quantity_list = position_Quantity_list + 15
#     p.line(250, line_position_Quantity_list, 600, line_position_Quantity_list)
#     p.drawString(300, position_Quantity_list, "Total")


#     p.drawString(450, position_SubTotal_Price_list, "subtotal amount")
#     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
#     p.drawString(450, position_SubTotal_Price_list, Invoice_get_ordr_tbl.Shopping)
#     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
#     p.drawString(450, position_Quantity_list, "Total amount")



#     p.drawString(225, 15, "WWW.boomboom.com.bd")
    
#     p.line(0, 60, 600, 60)
    
#     p.setFillColor(blue)
#     p.drawString(190, 45, "Thank you for shopping with BoomBoom")
#     p.drawString(241, 30, "We Deliver Quality")
#     p.drawString(225, 15, "WWW.boomboom.com.bd")

#     # Close the PDF object cleanly, and we're done.
#     p.showPage()

#     # necar line ta 2 bar lekhla 2 ta page hoy
#     # p.showPage()
#     p.save()
#     return response
#     # return FileResponse( , as_attachment=True, filename='p.pdf')


#single system for one invoice making proccess is here start






def dashboard_customer_order_edit_Generate_Invoice(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        Invoice_get_ordr_tbl = Order_Table.objects.get(id=pk)
        Invoice_filter_ordr_tbl_2 = Order_Table_2.objects.filter(Order_Id=Invoice_get_ordr_tbl)

        invoice_subtotal_amount = Invoice_get_ordr_tbl.SubTotal_Price
        invoice_Delivery_Charge = Invoice_get_ordr_tbl.Delivery_Charge
        invoice_GrandTotal_Price = Invoice_get_ordr_tbl.GrandTotal_Price

        get_sub = Invoice_get_ordr_tbl.SubTotal_Price
        ggt = get_sub
        ggtt = Invoice_get_ordr_tbl.GrandTotal_Price
        ggtt_get = ggtt
        for i in Invoice_filter_ordr_tbl_2:

            if i.New_Order_Status:
                ggt = ggt - i.then_price * i.Quantity
                invoice_subtotal_amount = ggt
                ggtt_get = ggtt_get - i.then_price * i.Quantity

            else:
                invoice_subtotal_amount = ggt
                invoice_GrandTotal_Price = ggtt_get

        invoice_GrandTotal_Price = invoice_subtotal_amount + invoice_Delivery_Charge

        invoice_Delivery_Charge = Invoice_get_ordr_tbl.Delivery_Charge

        invoice_GrandTotal_Order = Invoice_get_ordr_tbl.Order_Id
        invoice_GrandTotal_date = Invoice_get_ordr_tbl.Order_Date
        invoice_GrandTotal_payment_method = Invoice_get_ordr_tbl.Payment_method

        Customer_delivery_information_first_name = Invoice_get_ordr_tbl.Customer_delivery_information.First_Name
        Customer_delivery_information_last_name = Invoice_get_ordr_tbl.Customer_delivery_information.Last_Name
        Customer_delivery_information_full_name = Customer_delivery_information_first_name+' '+Customer_delivery_information_last_name
        Customer_delivery_information_Street_Address = Invoice_get_ordr_tbl.Customer_delivery_information.Street_Address
        Customer_delivery_information_Town_City = Invoice_get_ordr_tbl.Customer_delivery_information.Town_City
        Customer_delivery_information_District = Invoice_get_ordr_tbl.Customer_delivery_information.District
        Customer_delivery_information_Post_Code = Invoice_get_ordr_tbl.Customer_delivery_information.Post_Code
        Customer_delivery_information_Phone_Number = Invoice_get_ordr_tbl.Customer_delivery_information.Phone_Number
        Customer_delivery_information_Email_Address = Invoice_get_ordr_tbl.Customer_delivery_information.Email_Address

        Product_list = []
        Quantity_list = []
        SubTotal_Price_list = []

        for i in Invoice_filter_ordr_tbl_2:
            if i.New_Order_Status:
                pass
            else:
                Product_list.append(i.Product)
                Quantity_list.append(i.Quantity)
                SubTotal_Price_list.append(i.SubTotal_Price)
                k = i.Order_Id.Order_Status

        new_Product_list_1 = []
        new_Product_list_2 = []
        new_Product_list_3 = []
        new_Product_list_4 = []
        new_Product_list_5 = []
        new_Product_list_6 = []

        new_Quantity_list_1 = []
        new_Quantity_list_2 = []
        new_Quantity_list_3 = []
        new_Quantity_list_4 = []
        new_Quantity_list_5 = []
        new_Quantity_list_6 = []

        new_SubTotal_Price_list_1 = []
        new_SubTotal_Price_list_2 = []
        new_SubTotal_Price_list_3 = []
        new_SubTotal_Price_list_4 = []
        new_SubTotal_Price_list_5 = []
        new_SubTotal_Price_list_6 = []

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f' filename="{invoice_GrandTotal_Order}.pdf"'
        p = canvas.Canvas(response)

        len_Product_list = len(Product_list)
        count_serial = 1

        if len_Product_list < 16:

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")

            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")

            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")


            print('MEDIA_ROOT')
            print(MEDIA_ROOT)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)


            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(385, 630, "Order:   "+str(invoice_GrandTotal_Order))
            p.drawString(385, 614, "Date:   "+str(invoice_GrandTotal_date))
            p.drawString(385, 600, "Payment   "+str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(385, 588, "Method:   "+str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)


            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            print("Invoice_filter_ordr_tbl_2")
            print("Invoice_filter_ordr_tbl_2")

            print("Product_list")
            print(Product_list)

            position_Product_list = 490
            for r in Product_list:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial =count_serial+1

            position_Quantity_list = 490
            for r in Quantity_list:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in SubTotal_Price_list:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "subtotal =")
            position_Quantity_list = position_Quantity_list - 20
            p.drawString(385, position_Quantity_list, "shipping =")
            position_Quantity_list = position_Quantity_list - 20
            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "Total =")



            p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

            if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "approx 90% Due =")

                # finding 10 percent of invoice_subtotal_amount

                _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                    _10pescent_pluse_delevary_invoice_subtotal_amount)

                _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


            elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "100% Paid =")

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")
            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response



        elif len_Product_list > 15 and len_Product_list < 31:
            for i in range(0, 15):
                new_Product_list_1.append(Product_list[i])
                new_Quantity_list_1.append(Quantity_list[i])
                new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_1:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_1:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_1:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(15, len_Product_list):
                new_Product_list_2.append(Product_list[i])
                new_Quantity_list_2.append(Quantity_list[i])
                new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_2:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_2:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_2:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "subtotal =")
            position_Quantity_list = position_Quantity_list - 20
            p.drawString(385, position_Quantity_list, "shipping =")
            position_Quantity_list = position_Quantity_list - 20
            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "Total =")



            p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

            if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "approx 90% Due =")

                # finding 10 percent of invoice_subtotal_amount

                _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                    _10pescent_pluse_delevary_invoice_subtotal_amount)

                _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


            elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "100% Paid =")

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response



        elif len_Product_list > 30 and len_Product_list < 46:
            for i in range(0, 15):
                new_Product_list_1.append(Product_list[i])
                new_Quantity_list_1.append(Quantity_list[i])
                new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_1:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_1:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_1:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(15, 30):
                new_Product_list_2.append(Product_list[i])
                new_Quantity_list_2.append(Quantity_list[i])
                new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_2:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_2:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_2:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(30, len_Product_list):
                new_Product_list_3.append(Product_list[i])
                new_Quantity_list_3.append(Quantity_list[i])
                new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_3:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_3:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_3:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "subtotal =")
            position_Quantity_list = position_Quantity_list - 20
            p.drawString(385, position_Quantity_list, "shipping =")
            position_Quantity_list = position_Quantity_list - 20
            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "Total =")



            p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

            if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "approx 90% Due =")

                # finding 10 percent of invoice_subtotal_amount

                _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                    _10pescent_pluse_delevary_invoice_subtotal_amount)

                _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


            elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "100% Paid =")

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response



        elif len_Product_list > 45 and len_Product_list < 61:
            for i in range(0, 15):
                new_Product_list_1.append(Product_list[i])
                new_Quantity_list_1.append(Quantity_list[i])
                new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_1:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_1:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_1:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(15, 30):
                new_Product_list_2.append(Product_list[i])
                new_Quantity_list_2.append(Quantity_list[i])
                new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_2:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_2:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_2:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(30, 45):
                new_Product_list_3.append(Product_list[i])
                new_Quantity_list_3.append(Quantity_list[i])
                new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_3:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_3:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_3:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20


            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(45, len_Product_list):
                new_Product_list_4.append(Product_list[i])
                new_Quantity_list_4.append(Quantity_list[i])
                new_SubTotal_Price_list_4.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_4:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_4:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_4:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "subtotal =")
            position_Quantity_list = position_Quantity_list - 20
            p.drawString(385, position_Quantity_list, "shipping =")
            position_Quantity_list = position_Quantity_list - 20
            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "Total =")



            p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

            if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "approx 90% Due =")

                # finding 10 percent of invoice_subtotal_amount

                _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                    _10pescent_pluse_delevary_invoice_subtotal_amount)

                _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


            elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "100% Paid =")

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response



        elif len_Product_list > 60 and len_Product_list < 76:
            for i in range(0, 15):
                new_Product_list_1.append(Product_list[i])
                new_Quantity_list_1.append(Quantity_list[i])
                new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_1:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_1:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_1:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(15, 30):
                new_Product_list_2.append(Product_list[i])
                new_Quantity_list_2.append(Quantity_list[i])
                new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_2:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_2:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_2:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(30, 45):
                new_Product_list_3.append(Product_list[i])
                new_Quantity_list_3.append(Quantity_list[i])
                new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_3:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_3:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_3:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20


            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(45, 60):
                new_Product_list_4.append(Product_list[i])
                new_Quantity_list_4.append(Quantity_list[i])
                new_SubTotal_Price_list_4.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_4:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_4:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_4:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(60, len_Product_list):
                new_Product_list_5.append(Product_list[i])
                new_Quantity_list_5.append(Quantity_list[i])
                new_SubTotal_Price_list_5.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_5:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_5:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_5:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "subtotal =")
            position_Quantity_list = position_Quantity_list - 20
            p.drawString(385, position_Quantity_list, "shipping =")
            position_Quantity_list = position_Quantity_list - 20
            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "Total =")



            p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

            if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "approx 90% Due =")

                # finding 10 percent of invoice_subtotal_amount

                _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                    _10pescent_pluse_delevary_invoice_subtotal_amount)

                _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


            elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "100% Paid =")

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            return response


        else:

            for i in range(0, 15):
                new_Product_list_1.append(Product_list[i])
                new_Quantity_list_1.append(Quantity_list[i])
                new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))
            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_1:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_1:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_1:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(15, 30):
                new_Product_list_2.append(Product_list[i])
                new_Quantity_list_2.append(Quantity_list[i])
                new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_2:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_2:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_2:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20


            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(30, 45):
                new_Product_list_3.append(Product_list[i])
                new_Quantity_list_3.append(Quantity_list[i])
                new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_3:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_3:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_3:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(45, 60):
                new_Product_list_4.append(Product_list[i])
                new_Quantity_list_4.append(Quantity_list[i])
                new_SubTotal_Price_list_4.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_4:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_4:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_4:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(60, 75):
                new_Product_list_5.append(Product_list[i])
                new_Quantity_list_5.append(Quantity_list[i])
                new_SubTotal_Price_list_5.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")


            position_Product_list = 490
            for r in new_Product_list_5:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_5:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_5:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            for i in range(75, len_Product_list):
                new_Product_list_6.append(Product_list[i])
                new_Quantity_list_6.append(Quantity_list[i])
                new_SubTotal_Price_list_6.append(SubTotal_Price_list[i])

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")


            p.setFont("Helvetica", 10)
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 780, "Boom Boom Shopping")
            p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
            p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
            p.drawString(320, 735, "Phone : 09642601538")
            p.drawString(320, 720, "Mail: support@boomboom.com.bd")

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            print(k)
            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Processing' or k == 'Ready To Ship':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 18)
            p.drawString(40, 655, "INVOICE")
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 9)

            p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
            p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
            p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
            p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

            p.drawString(40, 630, str(Customer_delivery_information_full_name))
            p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
            p.drawString(40, 606, str(Customer_delivery_information_Town_City))
            p.drawString(40, 594, str(Customer_delivery_information_District))
            p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
            p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
            p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            # Yellow = Color(205, 205, 0, alpha=1)
            # p.setFillColor(Yellow)
            # p.rect(40, 510, 520, 30, fill=True, stroke=False)

            # p.line(x1, y1, x2, y2)
            p.line(40, 510, 557, 510)
            p.line(40, 539, 557, 539)
            p.line(40, 510, 40, 539)
            p.line(557, 510, 557, 539)

            p.setFillColor(black)
            p.drawString(44, 520, "Product")
            p.setFillColor(black)
            p.drawString(385, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(480, 520, "Price")

            position_Product_list = 490
            for r in new_Product_list_6:
                p.drawString(44, position_Product_list, str(count_serial)+". "+str(r))
                position_Product_list = position_Product_list - 20
                count_serial = count_serial + 1

            position_Quantity_list = 490
            for r in new_Quantity_list_6:
                p.drawString(385, position_Quantity_list, str(r))
                position_Quantity_list = position_Quantity_list - 20

            position_SubTotal_Price_list = 490
            for r in new_SubTotal_Price_list_6:
                p.drawString(480, position_SubTotal_Price_list, str(r))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20

            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "subtotal =")
            position_Quantity_list = position_Quantity_list - 20
            p.drawString(385, position_Quantity_list, "shipping =")
            position_Quantity_list = position_Quantity_list - 20
            line_position_Quantity_list = position_Quantity_list + 15
            p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            p.drawString(385, position_Quantity_list, "Total =")



            p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
            position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

            if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "approx 90% Due =")

                # finding 10 percent of invoice_subtotal_amount

                _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                    _10pescent_pluse_delevary_invoice_subtotal_amount)

                _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


            elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "100% Paid =")

                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

            p.line(0, 60, 600, 60)
            p.setFillColor(blue)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")

            # Close the PDF object cleanly, and we're done.
            p.showPage()

            p.save()
            return response
    else:
        return redirect('deshboard_login')




    
# end pdf code here single invoice











# start pdf code here it's for Multiple invoice
#all is ok
import json


# def sending_value_to_creat_multiple_invoice(request):
#     rrrr3434 = request.POST.get('rrrr')
#     print(rrrr3434)
#     data = json.loads(rrrr3434)
#     print(data)
#     print(data)

#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = ' filename="somefilename.pdf"'

#     # Create the PDF object, using the response object as its "file."
#     p = canvas.Canvas(response)


#     for j in data:
#         print(j)
#         # Draw things on the PDF. Here's where the PDF generation happens.
#         # See the ReportLab documentation for the full list of functionality.
#         # p.drawString((+)left, (+)Top, "Hello world.")
#         p.drawString(320, 780, "Boom Boom Shopping")
#         p.drawString(320, 765, "House-11, Road-18, Flat-6E, Sector-04")
#         p.drawString(320, 750, "Uttara, Dhaka-1230, Bangladesh")
#         p.drawString(320, 735, "Phone : 09642601538")
#         p.drawString(320, 720, "Mail: support@boomboom.com.bd")

#         i = 'https://idjangoo.com/static/images/logo-main.png'
#         p.drawImage(i, 40, 730, width=270, height=72)
#         u = 'kkk'
#         p.setFont("Helvetica", 25)
#         p.drawString(40, 655, "INVOICE")
#         p.setFont("Helvetica", 12)
#         p.drawString(300, 630, "Order:" + u)
#         p.drawString(300, 618, "Date:")
#         p.drawString(300, 606, "Payment:")
#         p.drawString(300, 594, "Method:")

#         p.drawString(40, 630, "Method:")
#         p.drawString(40, 618, "Method:")
#         p.drawString(40, 606, "Method:")
#         p.drawString(40, 594, "Method:")
#         p.drawString(40, 582, "Method:")
#         p.drawString(40, 570, "Method:")

#         # color(r,g,b, alpha)
#         red50transparent = Color(0, 0, 205, alpha=0.2)
#         Yellow = Color(205, 205, 0, alpha=1)
#         p.setFillColor(Yellow)
#         p.rect(40, 510, 520, 30, fill=True, stroke=False)

#         p.setFillColor(black)
#         p.drawString(70, 520, "Product")
#         p.setFillColor(black)
#         p.drawString(300, 520, "Quantity")
#         p.setFillColor(black)
#         p.drawString(450, 520, "Price")

#         p.line(0, 60, 600, 60)

#         p.setFillColor(blue)
#         p.drawString(190, 45, "Thank you for shopping with BoomBoom")
#         p.drawString(241, 30, "We Deliver Quality")
#         p.drawString(225, 15, "WWW.boomboom.com.bd")

#         u = Order_Table.objects.get(id=j)

#         p.drawString(225, 70, str(u))

#         # Close the PDF object cleanly, and we're done.
#         p.showPage()

#     p.save()
#     return response






def sending_value_to_creat_multiple_invoice(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        rrrr3434 = request.POST.get('rrrr')
        print(rrrr3434)
        data = json.loads(rrrr3434)
        print('data')
        print(data)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ' filename="Multiplefile.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)


        for j in data:
            Invoice_get_ordr_tbl = Order_Table.objects.get(id=j)
            Invoice_filter_ordr_tbl_2 = Order_Table_2.objects.filter(Order_Id=Invoice_get_ordr_tbl)

            print('Invoice_get_ordr_tbl')
            print(Invoice_get_ordr_tbl)
            print('Invoice_filter_ordr_tbl_2')
            print(Invoice_filter_ordr_tbl_2)

            invoice_subtotal_amount = Invoice_get_ordr_tbl.SubTotal_Price
            invoice_GrandTotal_Price = Invoice_get_ordr_tbl.GrandTotal_Price

            get_sub = Invoice_get_ordr_tbl.SubTotal_Price
            ggt = get_sub
            ggtt = Invoice_get_ordr_tbl.GrandTotal_Price
            ggtt_get = ggtt
            for i in Invoice_filter_ordr_tbl_2:

                if i.New_Order_Status:
                    ggt = ggt - i.then_price * i.Quantity
                    invoice_subtotal_amount = ggt
                    ggtt_get = ggtt_get - i.then_price * i.Quantity
                    print('11111111111111')
                else:
                    invoice_subtotal_amount = ggt
                    invoice_GrandTotal_Price = ggtt_get
                    print('222222222')
                    k = i.Order_Id.Order_Status

            invoice_Delivery_Charge = Invoice_get_ordr_tbl.Delivery_Charge

            invoice_GrandTotal_Order = Invoice_get_ordr_tbl.Order_Id
            invoice_GrandTotal_date = Invoice_get_ordr_tbl.Order_Date
            invoice_GrandTotal_payment_method = Invoice_get_ordr_tbl.Payment_method

            Customer_delivery_information_first_name = Invoice_get_ordr_tbl.Customer_delivery_information.First_Name
            Customer_delivery_information_last_name = Invoice_get_ordr_tbl.Customer_delivery_information.Last_Name
            Customer_delivery_information_full_name = Customer_delivery_information_first_name + ' ' + Customer_delivery_information_last_name
            Customer_delivery_information_Street_Address = Invoice_get_ordr_tbl.Customer_delivery_information.Street_Address
            Customer_delivery_information_Town_City = Invoice_get_ordr_tbl.Customer_delivery_information.Town_City
            Customer_delivery_information_District = Invoice_get_ordr_tbl.Customer_delivery_information.District
            Customer_delivery_information_Post_Code = Invoice_get_ordr_tbl.Customer_delivery_information.Post_Code
            Customer_delivery_information_Phone_Number = Invoice_get_ordr_tbl.Customer_delivery_information.Phone_Number
            Customer_delivery_information_Email_Address = Invoice_get_ordr_tbl.Customer_delivery_information.Email_Address

            Product_list = []
            Quantity_list = []
            SubTotal_Price_list = []

            for i in Invoice_filter_ordr_tbl_2:
                print('iii')
                print(i)

                if i.New_Order_Status:
                    pass
                else:
                    Product_list.append(i.Product)
                    Quantity_list.append(i.Quantity)
                    SubTotal_Price_list.append(i.SubTotal_Price)

            new_Product_list_1 = []
            new_Product_list_2 = []
            new_Product_list_3 = []
            new_Product_list_4 = []
            new_Product_list_5 = []
            new_Product_list_6 = []

            new_Quantity_list_1 = []
            new_Quantity_list_2 = []
            new_Quantity_list_3 = []
            new_Quantity_list_4 = []
            new_Quantity_list_5 = []
            new_Quantity_list_6 = []

            new_SubTotal_Price_list_1 = []
            new_SubTotal_Price_list_2 = []
            new_SubTotal_Price_list_3 = []
            new_SubTotal_Price_list_4 = []
            new_SubTotal_Price_list_5 = []
            new_SubTotal_Price_list_6 = []

            len_Product_list = len(Product_list)
            count_serial = 1

            if len_Product_list < 16:

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)

                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)



                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                print("Invoice_filter_ordr_tbl_2")
                print("Invoice_filter_ordr_tbl_2")

                print("Product_list")
                print(Product_list)

                position_Product_list = 490
                for r in Product_list:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in Quantity_list:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in SubTotal_Price_list:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "subtotal =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "shipping =")
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "Total =")

                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))



                if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                    position_Quantity_list = position_Quantity_list - 20
                    p.drawString(385, position_Quantity_list, "approx 90% Due =")

                    # finding 10 percent of invoice_subtotal_amount

                    _10pescent_invoice_subtotal_amount = (10*invoice_subtotal_amount)/100
                    _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                    _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(_10pescent_pluse_delevary_invoice_subtotal_amount)

                    _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price-_10pescent_pluse_delevary_invoice_subtotal_amount

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


                elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "100% Paid =")

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))



                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")
                # Close the PDF object cleanly, and we're done.
                p.showPage()


            elif len_Product_list > 15 and len_Product_list < 31:
                for i in range(0, 15):
                    new_Product_list_1.append(Product_list[i])
                    new_Quantity_list_1.append(Quantity_list[i])
                    new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_1:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_1:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_1:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(15, len_Product_list):
                    new_Product_list_2.append(Product_list[i])
                    new_Quantity_list_2.append(Quantity_list[i])
                    new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_2:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_2:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_2:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "subtotal =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "shipping =")
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "Total =")

                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

                if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                    position_Quantity_list = position_Quantity_list - 20
                    p.drawString(385, position_Quantity_list, "approx 90% Due =")

                    # finding 10 percent of invoice_subtotal_amount

                    _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                    _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                    _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                        _10pescent_pluse_delevary_invoice_subtotal_amount)

                    _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


                elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "100% Paid =")

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

            elif len_Product_list > 30 and len_Product_list < 46:
                for i in range(0, 15):
                    new_Product_list_1.append(Product_list[i])
                    new_Quantity_list_1.append(Quantity_list[i])
                    new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_1:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_1:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_1:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(15, 30):
                    new_Product_list_2.append(Product_list[i])
                    new_Quantity_list_2.append(Quantity_list[i])
                    new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_2:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_2:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_2:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(30, len_Product_list):
                    new_Product_list_3.append(Product_list[i])
                    new_Quantity_list_3.append(Quantity_list[i])
                    new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_3:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_3:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_3:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "subtotal =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "shipping =")
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "Total =")

                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

                if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                    position_Quantity_list = position_Quantity_list - 20
                    p.drawString(385, position_Quantity_list, "approx 90% Due =")

                    # finding 10 percent of invoice_subtotal_amount

                    _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                    _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                    _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                        _10pescent_pluse_delevary_invoice_subtotal_amount)

                    _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


                elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "100% Paid =")

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

            elif len_Product_list > 45 and len_Product_list < 61:
                for i in range(0, 15):
                    new_Product_list_1.append(Product_list[i])
                    new_Quantity_list_1.append(Quantity_list[i])
                    new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_1:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_1:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_1:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(15, 30):
                    new_Product_list_2.append(Product_list[i])
                    new_Quantity_list_2.append(Quantity_list[i])
                    new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_2:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_2:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_2:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(30, 45):
                    new_Product_list_3.append(Product_list[i])
                    new_Quantity_list_3.append(Quantity_list[i])
                    new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_3:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_3:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_3:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(45, len_Product_list):
                    new_Product_list_4.append(Product_list[i])
                    new_Quantity_list_4.append(Quantity_list[i])
                    new_SubTotal_Price_list_4.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_4:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_4:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_4:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "subtotal =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "shipping =")
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "Total =")

                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

                if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                    position_Quantity_list = position_Quantity_list - 20
                    p.drawString(385, position_Quantity_list, "approx 90% Due =")

                    # finding 10 percent of invoice_subtotal_amount

                    _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                    _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                    _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                        _10pescent_pluse_delevary_invoice_subtotal_amount)

                    _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


                elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "100% Paid =")

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

            elif len_Product_list > 60 and len_Product_list < 76:
                for i in range(0, 15):
                    new_Product_list_1.append(Product_list[i])
                    new_Quantity_list_1.append(Quantity_list[i])
                    new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_1:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_1:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_1:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(15, 30):
                    new_Product_list_2.append(Product_list[i])
                    new_Quantity_list_2.append(Quantity_list[i])
                    new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_2:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_2:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_2:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(30, 45):
                    new_Product_list_3.append(Product_list[i])
                    new_Quantity_list_3.append(Quantity_list[i])
                    new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_3:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_3:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_3:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(45, 60):
                    new_Product_list_4.append(Product_list[i])
                    new_Quantity_list_4.append(Quantity_list[i])
                    new_SubTotal_Price_list_4.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_4:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_4:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_4:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(60, len_Product_list):
                    new_Product_list_5.append(Product_list[i])
                    new_Quantity_list_5.append(Quantity_list[i])
                    new_SubTotal_Price_list_5.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)


                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_5:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_5:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_5:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "subtotal =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "shipping =")
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "Total =")

                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

                if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                    position_Quantity_list = position_Quantity_list - 20
                    p.drawString(385, position_Quantity_list, "approx 90% Due =")

                    # finding 10 percent of invoice_subtotal_amount

                    _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                    _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                    _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                        _10pescent_pluse_delevary_invoice_subtotal_amount)

                    _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


                elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "100% Paid =")

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

            else:
                for i in range(0, 15):
                    new_Product_list_1.append(Product_list[i])
                    new_Quantity_list_1.append(Quantity_list[i])
                    new_SubTotal_Price_list_1.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))
                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_1:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_1:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_1:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(15, 30):
                    new_Product_list_2.append(Product_list[i])
                    new_Quantity_list_2.append(Quantity_list[i])
                    new_SubTotal_Price_list_2.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_2:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_2:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_2:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(30, 45):
                    new_Product_list_3.append(Product_list[i])
                    new_Quantity_list_3.append(Quantity_list[i])
                    new_SubTotal_Price_list_3.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_3:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_3:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_3:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(45, 60):
                    new_Product_list_4.append(Product_list[i])
                    new_Quantity_list_4.append(Quantity_list[i])
                    new_SubTotal_Price_list_4.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")
                p.setFont("Helvetica", 10)

                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_4:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_4:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_4:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(60, 75):
                    new_Product_list_5.append(Product_list[i])
                    new_Quantity_list_5.append(Quantity_list[i])
                    new_SubTotal_Price_list_5.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")
                p.setFont("Helvetica", 10)

                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)


                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_5:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_5:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_5:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()

                for i in range(75, len_Product_list):
                    new_Product_list_6.append(Product_list[i])
                    new_Quantity_list_6.append(Quantity_list[i])
                    new_SubTotal_Price_list_6.append(SubTotal_Price_list[i])

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                # p.drawString((+)left, (+)Top, "Hello world.")

                p.setFont("Helvetica", 10)
                p.drawString(320, 780, "Boom Boom Shopping")

                p.drawString(320, 780, "Boom Boom Shopping")
                p.drawString(320, 765, "Flat A-8 of Millennium Castle, House-47, Road-27,")
                p.drawString(320, 750, "Block-A, Banani, Dhaka-1213, Bangladesh.")
                p.drawString(320, 735, "Phone : 09642601538")
                p.drawString(320, 720, "Mail: support@boomboom.com.bd")

                # i = 'https://idjangoo.com/static/images/logo-main.png'
                # p.drawImage(i, 40, 730, width=270, height=72)


                i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
                p.drawImage(i, 40, 730, width=270, height=72)

                print(k)
                if k == 'Refunded':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                if k == 'Processing' or k == 'Ready To Ship':
                    i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                    p.drawImage(i, 40, 670, width=60, height=60)

                p.setFont("Helvetica", 18)
                p.drawString(40, 655, "INVOICE")
                p.drawString(40, 655, "INVOICE")
                p.setFont("Helvetica", 9)

                p.drawString(300, 630, "Order:   " + str(invoice_GrandTotal_Order))
                p.drawString(300, 614, "Date:   " + str(invoice_GrandTotal_date))
                p.drawString(300, 600, "Payment   " + str(invoice_GrandTotal_payment_method[0:39]))
                p.drawString(300, 588, "Method:   " + str(invoice_GrandTotal_payment_method[39:]))

                p.drawString(40, 630, str(Customer_delivery_information_full_name))
                p.drawString(40, 618, str(Customer_delivery_information_Street_Address))
                p.drawString(40, 606, str(Customer_delivery_information_Town_City))
                p.drawString(40, 594, str(Customer_delivery_information_District))
                p.drawString(40, 582, str(Customer_delivery_information_Post_Code))
                p.drawString(40, 570, str(Customer_delivery_information_Phone_Number))
                p.drawString(40, 558, str(Customer_delivery_information_Email_Address))

                # color(r,g,b, alpha)
                red50transparent = Color(0, 0, 205, alpha=0.2)
                # Yellow = Color(205, 205, 0, alpha=1)
                # p.setFillColor(Yellow)
                # p.rect(40, 510, 520, 30, fill=True, stroke=False)

                # p.line(x1, y1, x2, y2)
                p.line(40, 510, 557, 510)
                p.line(40, 539, 557, 539)
                p.line(40, 510, 40, 539)
                p.line(557, 510, 557, 539)

                p.setFillColor(black)
                p.drawString(44, 520, "Product")
                p.setFillColor(black)
                p.drawString(385, 520, "Quantity")
                p.setFillColor(black)
                p.drawString(480, 520, "Price")

                position_Product_list = 490
                for r in new_Product_list_6:
                    p.drawString(44, position_Product_list, str(count_serial) + ". " + str(r))
                    position_Product_list = position_Product_list - 20
                    count_serial = count_serial + 1

                position_Quantity_list = 490
                for r in new_Quantity_list_6:
                    p.drawString(385, position_Quantity_list, str(r))
                    position_Quantity_list = position_Quantity_list - 20

                position_SubTotal_Price_list = 490
                for r in new_SubTotal_Price_list_6:
                    p.drawString(480, position_SubTotal_Price_list, str(r))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20

                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "subtotal =")
                position_Quantity_list = position_Quantity_list - 20
                p.drawString(385, position_Quantity_list, "shipping =")
                position_Quantity_list = position_Quantity_list - 20
                line_position_Quantity_list = position_Quantity_list + 15
                p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                p.drawString(385, position_Quantity_list, "Total =")

                p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_SubTotal_Price_list, str(invoice_Delivery_Charge))
                position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                p.drawString(480, position_Quantity_list, str(invoice_GrandTotal_Price))

                if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "approx 10% Paid =")
                    position_Quantity_list = position_Quantity_list - 20
                    p.drawString(385, position_Quantity_list, "approx 10% Due =")

                    # finding 10 percent of invoice_subtotal_amount

                    _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
                    _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge

                    _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
                        _10pescent_pluse_delevary_invoice_subtotal_amount)

                    _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))


                elif Invoice_get_ordr_tbl.Order_Status == 'Processing':

                    position_Quantity_list = position_Quantity_list - 20
                    line_position_Quantity_list = position_Quantity_list + 15
                    p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
                    p.drawString(385, position_Quantity_list, "100% Paid =")

                    position_SubTotal_Price_list = position_SubTotal_Price_list - 20
                    p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

                p.line(0, 60, 600, 60)
                p.setFillColor(blue)
                p.drawString(190, 45, "Thank you for shopping with BoomBoom")
                p.drawString(241, 30, "We Deliver Quality")
                p.drawString(225, 15, "WWW.boomboom.com.bd")

                # Close the PDF object cleanly, and we're done.
                p.showPage()



        p.save()
        return response
    else:
        return redirect('deshboard_login')
 





    
# end pdf code here Multiple invoice



# start pdf code here Multiple csv

# import file for csv start here
import csv
from datetime import datetime
from datetime import timedelta
# import file for csv end here


def sending_value_to_creat_multiple_csv(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        date = datetime.now().strftime('%d-%m-%Y')
        rrrr_multiple_csv_val = request.POST.get('rrrr_multiple_csv')

        multiple_csv_data = json.loads(rrrr_multiple_csv_val)
        Invoice_get_ordr_tbl = Order_Table.objects.get(id=multiple_csv_data[0])

        if Invoice_get_ordr_tbl.Order_Campaign:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={date} campaign order.csv'

        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={date} reguler order.csv'

        writer = csv.writer(response)

        writer.writerow(['Order Number', 'Order Status', 'Order Date', 'First Name (Billing)', 'Last Name (Billing)',  'Email (Billing)', 'Phone (Billing)', 'First Name (Shipping)', 'Last Name (Shipping)', 'Address 1&2 (Shipping)', 'City (Shipping)', 'Postcode (Shipping)',  'Email (Shipping)', 'Phone (Shipping)', 'Payment Method Title', 'Order Total Amount', 'Delivery Charge', 'GrandTotalPrice', 'Item # #1', 'Item Name #1', 'Quantity #1', 'Item # #2', 'Item Name #2', 'Quantity #2', 'Item # #3', 'Item Name #3', 'Quantity #3', 'Item # #4', 'Item Name #4', 'Quantity #4', 'Item # #5', 'Item Name #5', 'Quantity #5', 'Item # #6', 'Item Name #6', 'Quantity #6', 'Item # #7', 'Item Name #7', 'Quantity #7', 'Item # #8', 'Item Name #8', 'Quantity #8', 'Item # #9', 'Item Name #9', 'Quantity #9', 'Item # #10', 'Item Name #10', 'Quantity #10', 'Item # #11', 'Item Name #11', 'Quantity #11', 'Item # #12', 'Item Name #12', 'Quantity #12', 'Item # #13', 'Item Name #13', 'Quantity #13', 'Item # #14', 'Item Name #14', 'Quantity #14', 'Item # #15', 'Item Name #15', 'Quantity #15', 'Item # #16', 'Item Name #16', 'Quantity #16', 'Item # #17', 'Item Name #17', 'Quantity #17', 'Item # #18', 'Item Name #18', 'Quantity #18', 'Item # #19', 'Item Name #19', 'Quantity #19', 'Item # #20', 'Item Name #20', 'Quantity #20',])



        for j in multiple_csv_data:
            Invoice_get_ordr_tbl = Order_Table.objects.get(id=j)
            Invoice_filter_ordr_tbl_2 = Order_Table_2.objects.filter(Order_Id=Invoice_get_ordr_tbl)

            print("Invoice_filter_ordr_tbl_2")
            print(Invoice_filter_ordr_tbl_2)

            pruduct_list_for_csv = []
            pruduct_quantity_list_for_csv = []

            POSSS = 0
            for i in Invoice_filter_ordr_tbl_2:
                POSSS = POSSS + 1
                pruduct_list_for_csv.append(POSSS)
                pruduct_list_for_csv.append(i.Product.Product_Name)
                pruduct_list_for_csv.append(i.Quantity)

            print("Product_list")
            print(pruduct_list_for_csv)
            print(type(pruduct_list_for_csv))

            # for_example = [1, 2, 3, 4, 5, 6]
            # writer.writerow([for_example[index]] for index in range(0, len(for_example)))
            writer.writerow([Invoice_get_ordr_tbl.Order_Id] + [Invoice_get_ordr_tbl.Order_Status]+ [Invoice_get_ordr_tbl.Order_Date] + [Invoice_get_ordr_tbl.Customer.first_name] + [Invoice_get_ordr_tbl.Customer.last_name]+ [Invoice_get_ordr_tbl.Customer.email]+ [Invoice_get_ordr_tbl.Customer.username]+  [Invoice_get_ordr_tbl.Customer_delivery_information.First_Name]+ [Invoice_get_ordr_tbl.Customer_delivery_information.Last_Name]+ [Invoice_get_ordr_tbl.Customer_delivery_information.Street_Address]+ [Invoice_get_ordr_tbl.Customer_delivery_information.Town_City]+ [Invoice_get_ordr_tbl.Customer_delivery_information.Post_Code]+ [Invoice_get_ordr_tbl.Customer_delivery_information.Email_Address]+ [Invoice_get_ordr_tbl.Customer_delivery_information.Phone_Number]+ [Invoice_get_ordr_tbl.Payment_method]+ [Invoice_get_ordr_tbl.SubTotal_Price] + [Invoice_get_ordr_tbl.Delivery_Charge]+ [Invoice_get_ordr_tbl.GrandTotal_Price] + [pruduct_list_for_csv[o] for o in range(0, len(pruduct_list_for_csv))] )
            # Spam = 'Spam'
            # writer.writerow([Spam] * 5 + ['Baked Beans'])
            # writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])


        return response
    else:
        return redirect('deshboard_login')



# end pdf code here Multiple csv



def create_flash_sale(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        all_flash = Flash_Sell.objects.all()
        context = {'all_flash':all_flash}
        return render(request, 'create_flash_sale.html', context)
    else:
        return redirect('deshboard_login')
    
    
def add_flash_sale(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        if request.method == 'POST':
            flash_sale_form = form_Flash_Sell_add(request.POST)
            if flash_sale_form.is_valid():
                flash_sale_form.save()
                messages.success(request, 'Successfully Added !!')
                return redirect('create_flash_sale')
            else:
                messages.success(request, 'Fail to Add !!')
                return redirect('create_flash_sale')
        else:
            flash_sale_form = form_Flash_Sell_add()
            context={'flash_sale_form':flash_sale_form}
            return render(request, 'add_flash_sale.html', context)
    else:
        return redirect('deshboard_login')
    
    
     
def edit_flash(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        aget_flash = Flash_Sell.objects.get(id=pk)
        flash_sale_form = form_Flash_Sell_add(instance=aget_flash)

        if request.method == 'POST':
            flash_sale_form = form_Flash_Sell_add(request.POST, instance=aget_flash)

            if flash_sale_form.is_valid():
                flash_sale_form.save()
                messages.success(request, 'Successfully Updated !!')
                return redirect('create_flash_sale')

        context4 = {
            'flash_sale_form':flash_sale_form
        }
        return render(request, 'add_flash_sale.html', context4)
    else:
        return redirect('deshboard_login')
 
   
def delete_flash(request, pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        get_flash = Flash_Sell.objects.get(id=pk)

        get_flash.delete()
        return redirect('create_flash_sale')
    else:
        return redirect('deshboard_login')

    
    
    
    
    
    
    
    
    


    
    