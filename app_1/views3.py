from django.shortcuts import render,HttpResponse, redirect
from checkout.models import Order_Table_3, order_table_3_logs
from app_1.models import User,Staff_Access
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse
import csv
import json
from checkout.models import Order_Table_3
from .resources import name_database_y
from tablib import Dataset
from datetime import datetime


from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')





def save_the_csv_file_pp(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        if request.method == 'POST':
            name_database_yooo = name_database_y()
            dataset = Dataset()
            files_are = request.FILES['thefile']
            import_data_to_model = dataset.load(files_are.read(), format='xlsx')
            for data in import_data_to_model:
                date_time_str = data[5]
                # date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

                value = Order_Table_3(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11],
                    data[12],
                    data[13],
                    data[14],
                    data[15],
                    data[16],
                    data[17],
                    data[18],
                    data[19],
                    data[20],
                    data[21],
                    data[22],
                    data[23],
                    data[24],
                    data[25],
                    data[26],
                    data[27],
                    data[28],
                    data[29],
                    data[30],
                    data[31],
                    data[32],
                    data[33],
                    data[34],
                    data[35],
                    data[36],
                    data[37],
                )
                value.save()
        return render(request, 'old order.html')
    else:
        return redirect('deshboard_login')


def password_rehash(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    from app_1.models import User
    from django.contrib.auth.hashers import get_hasher

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        all_wp_usr = User.objects.filter(password__startswith='$P$B')
        hasher = get_hasher('phpass')

        for user in all_wp_usr:
            user.password = hasher.from_orig(user.password)
            user.save()
        return HttpResponse('Done')




def dashboard_old_order(request, template='old order.html', page_template='old order_next.html'):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        get_Order_Table_3 = Order_Table_3.objects.all()

        get_Order_Table_3_count_all = get_Order_Table_3.count()
        get_Order_Table_3_count_Cancelled = get_Order_Table_3.filter(old_order_status = 'Cancelled').count()
        get_Order_Table_3_count_Pending_Payment = get_Order_Table_3.filter(old_order_status = 'Pending Payment').count()
        get_Order_Table_3_count_Processing = get_Order_Table_3.filter(old_order_status = 'Processing').count()
        get_Order_Table_3_count_Refunded = get_Order_Table_3.filter(old_order_status = 'Refunded').count()
        get_Order_Table_3_count_Partially_Paid = get_Order_Table_3.filter(old_order_status = 'Partially Paid').count()
        get_Order_Table_3_count_Shifted_To_Courier = get_Order_Table_3.filter(old_order_status = 'Shifted To Courier').count()
        get_Order_Table_3_count_Picked = get_Order_Table_3.filter(old_order_status = 'Picked').count()
        get_Order_Table_3_count_Completed = get_Order_Table_3.filter(old_order_status = 'Completed').count()
        get_Order_Table_3_count_On_Hold = get_Order_Table_3.filter(old_order_status = 'On Hold').count()
        get_Order_Table_3_count_Cash_On_Delivery = get_Order_Table_3.filter(old_order_status = 'Cash On Delivery').count()


        old_order_Pending_payment_filtere = request.GET.get('old_order_Pending_payment_filtere')
        old_order_Processing_filter = request.GET.get('old_order_Processing_filter')
        old_order_Partially_Paid_filter = request.GET.get('old_order_Partially_Paid_filter')
        old_order_Shifted_To_Courier_filter = request.GET.get('old_order_Shifted_To_Courier_filter')
        old_order_Completed_filter = request.GET.get('old_order_Completed_filter')
        old_order_Cancelled_filter = request.GET.get('old_order_Cancelled_filter')
        old_order_Refunded_filter = request.GET.get('old_order_Refunded_filter')
        old_order_Picked_filter = request.GET.get('old_order_Picked_filter')
        old_order_On_hold_filter = request.GET.get('old_order_On_hold_filter')
        old_order_Cash_On_Delivery_filter = request.GET.get('old_order_Cash_On_Delivery_filter')
        old_order_All_Orders_filter = request.GET.get('old_order_All_Orders_filter')

        print('old_order_Processing_filter')
        print(old_order_Processing_filter)
        if old_order_All_Orders_filter:
            get_Order_Table_3 = Order_Table_3.objects.all()
        else:
            if old_order_Pending_payment_filtere:
                pass
            elif old_order_Processing_filter:
                pass
            elif old_order_Partially_Paid_filter:
                pass
            elif old_order_Shifted_To_Courier_filter:
                pass
            elif old_order_Completed_filter:
                pass
            elif old_order_Cancelled_filter:
                pass
            elif old_order_Refunded_filter:
                pass
            elif old_order_Picked_filter:
                pass
            elif old_order_On_hold_filter:
                pass
            elif old_order_Cash_On_Delivery_filter:
                pass
            else:
                old_order_All_Orders_filter = 'i am first'
            get_Order_Table_3 = Order_Table_3.objects.all()


        if old_order_Pending_payment_filtere:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Pending_payment_filtere)

        elif old_order_Processing_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Processing_filter)

        elif old_order_Partially_Paid_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Partially_Paid_filter)

        elif old_order_Shifted_To_Courier_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Shifted_To_Courier_filter)

        elif old_order_Completed_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Completed_filter)

        elif old_order_Cancelled_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Cancelled_filter)

        elif old_order_Refunded_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Refunded_filter)

        elif old_order_Picked_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Picked_filter)

        elif old_order_On_hold_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_On_hold_filter)

        elif old_order_Cash_On_Delivery_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_status = old_order_Cash_On_Delivery_filter)


        hidden_old_order_Pending_payment_filtere = request.GET.get('hidden_old_order_Pending_payment_filtere')
        hidden_old_order_Processing_filter = request.GET.get('hidden_old_order_Processing_filter')
        hidden_old_order_Partially_Paid_filter = request.GET.get('hidden_old_order_Partially_Paid_filter')
        hidden_old_order_Shifted_To_Courier_filter = request.GET.get('hidden_old_order_Shifted_To_Courier_filter')
        hidden_old_order_Completed_filter = request.GET.get('hidden_old_order_Completed_filter')
        hidden_old_order_Cancelled_filter = request.GET.get('hidden_old_order_Cancelled_filter')
        hidden_old_order_Refunded_filter = request.GET.get('hidden_old_order_Refunded_filter')
        hidden_old_order_Picked_filter = request.GET.get('hidden_old_order_Picked_filter')
        hidden_old_order_On_hold_filter = request.GET.get('hidden_old_order_On_hold_filter')
        hidden_old_order_Cash_On_Delivery_filter = request.GET.get('hidden_old_order_Cash_On_Delivery_filter')
        hidden_old_order_All_Orders_filter = request.GET.get('hidden_old_order_All_Orders_filter')

        get_old_order_Start_Date_filter = request.GET.get('get_old_order_Start_Date_filter')
        get_old_order_End_Date_filter = request.GET.get('get_old_order_End_Date_filter')


        if  get_old_order_Start_Date_filter:
            get_Order_Table_3 = Order_Table_3.objects.filter(old_order_date__range = [get_old_order_Start_Date_filter, get_old_order_End_Date_filter])
            if hidden_old_order_Pending_payment_filtere:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status  = 'Pending Payment')
                old_order_Pending_payment_filtere = 'old_order_Pending_payment_filtere'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Processing_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Processing')
                old_order_Processing_filter = 'old_order_Processing_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Partially_Paid_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Partially Paid')
                old_order_Partially_Paid_filter  ='old_order_Partially_Paid_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Shifted_To_Courier_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Shifted To Courier')
                old_order_Shifted_To_Courier_filter = 'old_order_Shifted_To_Courier_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Completed_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Completed')
                old_order_Completed_filter = 'old_order_Completed_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Cancelled_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Cancelled')
                old_order_Cancelled_filter = 'old_order_Cancelled_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Refunded_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Refunded')
                old_order_Refunded_filter = 'old_order_Refunded_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Picked_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Picked')
                old_order_Picked_filter = 'old_order_Picked_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_On_hold_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='On Hold')
                old_order_On_hold_filter = 'old_order_On_hold_filter'
                old_order_All_Orders_filter = None
            elif hidden_old_order_Cash_On_Delivery_filter:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_status='Cash On Delivery')
                old_order_Cash_On_Delivery_filter = 'old_order_Cash_On_Delivery_filter'
                old_order_All_Orders_filter = None

        old_order_search_input = request.GET.get('old_order_search_input')
        if old_order_search_input:
            if len(old_order_search_input) > 5:
                get_Order_Table_3 = get_Order_Table_3.filter(old_Customer_Email=old_order_search_input)
            else:
                get_Order_Table_3 = get_Order_Table_3.filter(old_order_id=old_order_search_input)

        all_ordr_qty  = get_Order_Table_3.count()

        if request.is_ajax():
            template = page_template

        contex = {
                  'page_template': page_template,
                  'get_Order_Table_3': get_Order_Table_3,
                  'all_ordr_qty': all_ordr_qty,
                  'get_Order_Table_3_count_all':get_Order_Table_3_count_all,
                  'get_Order_Table_3_count_Cancelled':get_Order_Table_3_count_Cancelled,
                  'get_Order_Table_3_count_Pending_Payment':get_Order_Table_3_count_Pending_Payment,
                  'get_Order_Table_3_count_Processing':get_Order_Table_3_count_Processing,
                  'get_Order_Table_3_count_Refunded':get_Order_Table_3_count_Refunded,
                  'get_Order_Table_3_count_Partially_Paid':get_Order_Table_3_count_Partially_Paid,
                  'get_Order_Table_3_count_Shifted_To_Courier':get_Order_Table_3_count_Shifted_To_Courier,
                  'get_Order_Table_3_count_Picked':get_Order_Table_3_count_Picked,
                  'get_Order_Table_3_count_Completed':get_Order_Table_3_count_Completed,
                  'get_Order_Table_3_count_On_Hold':get_Order_Table_3_count_On_Hold,
                  'get_Order_Table_3_count_Cash_On_Delivery':get_Order_Table_3_count_Cash_On_Delivery,

                  'old_order_Pending_payment_filtere':old_order_Pending_payment_filtere,
                  'old_order_Processing_filter':old_order_Processing_filter,
                  'old_order_Partially_Paid_filter':old_order_Partially_Paid_filter,
                  'old_order_Shifted_To_Courier_filter':old_order_Shifted_To_Courier_filter,
                  'old_order_Completed_filter':old_order_Completed_filter,
                  'old_order_Cancelled_filter':old_order_Cancelled_filter,
                  'old_order_Completed_filter':old_order_Completed_filter,
                  'old_order_Refunded_filter':old_order_Refunded_filter,
                  'old_order_Picked_filter':old_order_Picked_filter,
                  'old_order_On_hold_filter':old_order_On_hold_filter,
                  'old_order_Cash_On_Delivery_filter':old_order_Cash_On_Delivery_filter,
                  'old_order_All_Orders_filter':old_order_All_Orders_filter,
                  'get_old_order_Start_Date_filter':get_old_order_Start_Date_filter,
                  'get_old_order_End_Date_filter':get_old_order_End_Date_filter,
                  }

        return render(request, template, contex)
    else:
        return redirect('deshboard_login')



@csrf_exempt
def old_order_table_3_change_status(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        order_id = request.POST.get('order_id')
        bulk_action_id = request.POST.get('bulk_action_id')
        print(order_id)
        print(bulk_action_id)
        get_the_row_order_table3 = Order_Table_3.objects.get(id = order_id)
        get_the_row_order_table3.old_order_status = bulk_action_id
        get_the_row_order_table3.save()
        return HttpResponse(True)
    else:
        return redirect('deshboard_login')


def old_dashboard_customer_order_edit(request, dashboard_old_order_pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        print('dashboard_old_order_pk')
        print(dashboard_old_order_pk)
        get_uniq_user_orders = Order_Table_3.objects.get(id = dashboard_old_order_pk)

        get_uniq_order_table_3_logs = order_table_3_logs.objects.filter(order_table_3=get_uniq_user_orders).order_by('-logs_time')

        print(get_uniq_user_orders)
        contex = {'dashboard_old_order_pk':dashboard_old_order_pk,
                  'get_uniq_user_orders':get_uniq_user_orders,
                  'get_uniq_order_table_3_logs':get_uniq_order_table_3_logs
                  }
        return render(request, 'old_dashboard_customer_order_edit.html', contex)
    else:
        return redirect('deshboard_login')








def save_old_order_status_single(request, save_old_order_status_single_pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:

        if staff_admin:
            rol = staff_admin
        elif staff_shop_manager:
            rol = staff_shop_manager
        elif staff_customer_support:
            rol = staff_customer_support
        Staff_r = Staff_Access.objects.get(Username=rol)


        old_order_status_get = request.POST.get('old_order_status_get')
        get_uniq_user_orders = Order_Table_3.objects.get(id=save_old_order_status_single_pk)

        ager_status = get_uniq_user_orders.old_order_status

        get_uniq_user_orders.old_order_status =old_order_status_get
        get_uniq_user_orders.save()

        log_text_forold_logs = f'Order Status is Changed from - {ager_status} to {old_order_status_get}'
        new_log = order_table_3_logs(staff_role=Staff_r, order_table_3=get_uniq_user_orders, logs_status=log_text_forold_logs)
        new_log.save()

        return redirect('old_dashboard_customer_order_edit', save_old_order_status_single_pk)
    else:
        return redirect('deshboard_login')


from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.colors import Color, black, blue, red




def old_sending_value_to_creat_multiple_invoice(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        old_rrrr = request.POST.get('old_rrrr')
        print('old_rrrr')
        print(old_rrrr)

        data = json.loads(old_rrrr)
        print(data)
        print(data)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ' filename="somefilename.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        for j in data:
            u = Order_Table_3.objects.get(id=j)
            print(j)
            k = u.old_order_status
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            # p.drawString((+)left, (+)Top, "Hello world.")
            p.setFont("Helvetica", 10)
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

            if k == 'Processing' or k == 'Shifted To Courier':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            p.setFont("Helvetica", 25)
            p.drawString(40, 655, "INVOICE")
            p.setFont("Helvetica", 10)
            p.drawString(300, 630, "Order: "+ u.old_order_id)
            p.drawString(300, 618, "Date: "+str(u.old_order_date))
            p.drawString(300, 606, "Payment Method: " +u.old_Payment_method[0:35])
            p.drawString(300, 594, u.old_Payment_method[35:])
            # p.drawString(300, 594, "Method:")

            p.drawString(40, 630, str(u.old_customer_first_name)+' '+str(u.old_customer_last_name))
            p.drawString(40, 618, str(u.old_Customer_Address)[:40])
            p.drawString(40, 606, str(u.old_Customer_City))
            p.drawString(40, 594, str(u.old_Customer_Postcode))
            p.drawString(40, 582, str(u.old_Customer_Phone))
            p.drawString(40, 570, str(u.old_Customer_Email))

            # color(r,g,b, alpha)
            red50transparent = Color(0, 0, 205, alpha=0.2)
            Yellow = Color(205, 205, 0, alpha=1)
            p.setFillColor(Yellow)
            p.rect(40, 510, 520, 30, fill=False, stroke=True)

            p.setFillColor(black)
            p.drawString(70, 520, "Product")
            p.setFillColor(black)
            p.drawString(300, 520, "Quantity")
            p.setFillColor(black)
            p.drawString(450, 520, "Price")

            p.line(0, 60, 600, 60)

            p.setFillColor(black)
            p.drawString(190, 45, "Thank you for shopping with BoomBoom")
            p.drawString(241, 30, "We Deliver Quality")
            p.drawString(225, 15, "WWW.boomboom.com.bd")


            if u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7 and u.old_product_8 and u.old_product_9 and u.old_product_10:

                p.drawString(44, 490, '1. '+ str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445, '4. '+  str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.drawString(44, 430, '5. '+  str(u.old_product_5))
                p.drawString(300, 430, str(u.old_product_5_quenity))
                total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
                p.drawString(450, 430, str(total_of_item_5))

                p.drawString(44, 415, '6. '+  str(u.old_product_6))
                p.drawString(300, 415, str(u.old_product_6_quenity))
                total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
                p.drawString(450, 415, str(total_of_item_6))

                p.drawString(44, 400, '7. '+  str(u.old_product_7))
                p.drawString(300, 400, str(u.old_product_7_quenity))
                total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
                p.drawString(450, 400, str(total_of_item_7))

                p.drawString(44, 385, '8. '+  str(u.old_product_8))
                p.drawString(300, 385, str(u.old_product_8_quenity))
                total_of_item_8 = int(u.old_product_8_quenity) * int(u.old_product_8_price)
                p.drawString(450, 385, str(total_of_item_8))

                p.drawString(44, 370, '9. '+  str(u.old_product_9))
                p.drawString(300, 370, str(u.old_product_9_quenity))
                total_of_item_9 = int(u.old_product_9_quenity) * int(u.old_product_9_price)
                p.drawString(450, 370, str(total_of_item_9))

                p.drawString(44, 355, '10. '+  str(u.old_product_10))
                p.drawString(300, 355, str(u.old_product_10_quenity))
                total_of_item_10 = int(u.old_product_10_quenity) * int(u.old_product_10_price)
                p.drawString(450, 355, str(total_of_item_10))

                p.line(260, 350, 560, 350)

                p.drawString(300, 335, 'Sub Total = ')
                p.drawString(450, 335, str(u.old_Subtotal_Amount))
                p.drawString(300, 320, 'Delivery = ')
                p.drawString(450, 320, str(u.old_delivery_charge))
                p.drawString(300, 305, 'Greand Total = ')
                p.drawString(450, 305, str(u.old_order_total))

            elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7 and u.old_product_8 and u.old_product_9:
                p.drawString(44, 490,'1. '+ str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity)*int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475,'2. '+ str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460,'3. '+ str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445,'4. '+ str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.drawString(44, 430,'5. '+ str(u.old_product_5))
                p.drawString(300, 430, str(u.old_product_5_quenity))
                total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
                p.drawString(450, 430, str(total_of_item_5))

                p.drawString(44, 415,'6. '+ str(u.old_product_6))
                p.drawString(300, 415, str(u.old_product_6_quenity))
                total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
                p.drawString(450, 415, str(total_of_item_6))

                p.drawString(44, 400,'7. '+ str(u.old_product_7))
                p.drawString(300, 400, str(u.old_product_7_quenity))
                total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
                p.drawString(450, 400, str(total_of_item_7))

                p.drawString(44, 385,'8. '+ str(u.old_product_8))
                p.drawString(300, 385, str(u.old_product_8_quenity))
                total_of_item_8 = int(u.old_product_8_quenity) * int(u.old_product_8_price)
                p.drawString(450, 385, str(total_of_item_8))

                p.drawString(44, 370,'9. '+ str(u.old_product_9))
                p.drawString(300, 370, str(u.old_product_9_quenity))
                total_of_item_9 = int(u.old_product_9_quenity) * int(u.old_product_9_price)
                p.drawString(450, 370, str(total_of_item_9))


                p.line(260, 365, 560, 365)

                p.drawString(300, 350, 'Sub Total = ')
                p.drawString(450, 350, str(u.old_Subtotal_Amount))
                p.drawString(300, 335, 'Delivery = ')
                p.drawString(450, 335, str(u.old_delivery_charge))
                p.drawString(300, 320, 'Greand Total = ')
                p.drawString(450, 320, str(u.old_order_total))

            elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7 and u.old_product_8:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445,'4. '+ str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.drawString(44, 430,'5. '+ str(u.old_product_5))
                p.drawString(300, 430, str(u.old_product_5_quenity))
                total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
                p.drawString(450, 430, str(total_of_item_5))

                p.drawString(44, 415,'6. '+ str(u.old_product_6))
                p.drawString(300, 415, str(u.old_product_6_quenity))
                total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
                p.drawString(450, 415, str(total_of_item_6))

                p.drawString(44, 400,'7. '+ str(u.old_product_7))
                p.drawString(300, 400, str(u.old_product_7_quenity))
                total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
                p.drawString(450, 400, str(total_of_item_7))

                p.drawString(44, 385,'8. '+ str(u.old_product_8))
                p.drawString(300, 385, str(u.old_product_8_quenity))
                total_of_item_8 = int(u.old_product_8_quenity) * int(u.old_product_8_price)
                p.drawString(450, 385, str(total_of_item_8))


                p.line(260, 380, 560, 380)

                p.drawString(300, 365, 'Sub Total = ')
                p.drawString(450, 365, str(u.old_Subtotal_Amount))
                p.drawString(300, 350, 'Delivery = ')
                p.drawString(450, 350, str(u.old_delivery_charge))
                p.drawString(300, 335, 'Greand Total = ')
                p.drawString(450, 335, str(u.old_order_total))

            elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445, '4. '+  str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.drawString(44, 430, '5. '+  str(u.old_product_5))
                p.drawString(300, 430, str(u.old_product_5_quenity))
                total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
                p.drawString(450, 430, str(total_of_item_5))

                p.drawString(44, 415, '6. '+  str(u.old_product_6))
                p.drawString(300, 415, str(u.old_product_6_quenity))
                total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
                p.drawString(450, 415, str(total_of_item_6))

                p.drawString(44, 400, '7. '+  str(u.old_product_7))
                p.drawString(300, 400, str(u.old_product_7_quenity))
                total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
                p.drawString(450, 400, str(total_of_item_7))


                p.line(260, 395, 560, 395)

                p.drawString(300, 380, 'Sub Total = ')
                p.drawString(450, 380, str(u.old_Subtotal_Amount))
                p.drawString(300, 365, 'Delivery = ')
                p.drawString(450, 365, str(u.old_delivery_charge))
                p.drawString(300, 350, 'Greand Total = ')
                p.drawString(450, 350, str(u.old_order_total))

            elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445, '4. '+  str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.drawString(44, 430, '5. '+  str(u.old_product_5))
                p.drawString(300, 430, str(u.old_product_5_quenity))
                total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
                p.drawString(450, 430, str(total_of_item_5))

                p.drawString(44, 415, '6. '+  str(u.old_product_6))
                p.drawString(300, 415, str(u.old_product_6_quenity))
                total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
                p.drawString(450, 415, str(total_of_item_6))


                p.line(260, 410, 560, 410)

                p.drawString(300, 395, 'Sub Total = ')
                p.drawString(450, 395, str(u.old_Subtotal_Amount))
                p.drawString(300, 380, 'Delivery = ')
                p.drawString(450, 380, str(u.old_delivery_charge))
                p.drawString(300, 365, 'Greand Total = ')
                p.drawString(450, 365, str(u.old_order_total))



            elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445, '4. '+  str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.drawString(44, 430, '5. '+  str(u.old_product_5))
                p.drawString(300, 430, str(u.old_product_5_quenity))
                total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
                p.drawString(450, 430, str(total_of_item_5))

                p.line(260, 425, 560, 425)

                p.drawString(300, 410, 'Sub Total = ')
                p.drawString(450, 410, str(u.old_Subtotal_Amount))
                p.drawString(300, 395, 'Delivery = ')
                p.drawString(450, 395, str(u.old_delivery_charge))
                p.drawString(300, 380, 'Greand Total = ')
                p.drawString(450, 380, str(u.old_order_total))


            elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.drawString(44, 445, '4. '+  str(u.old_product_4))
                p.drawString(300, 445, str(u.old_product_4_quenity))
                total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
                p.drawString(450, 445, str(total_of_item_4))

                p.line(260, 440, 560, 440)

                p.drawString(300, 415, 'Sub Total = ')
                p.drawString(450, 415, str(u.old_Subtotal_Amount))
                p.drawString(300, 400, 'Delivery = ')
                p.drawString(450, 400, str(u.old_delivery_charge))
                p.drawString(300, 385, 'Greand Total = ')
                p.drawString(450, 385, str(u.old_order_total))

            elif u.old_product_1 and u.old_product_2 and u.old_product_3:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.drawString(44, 460, '3. '+  str(u.old_product_3))
                p.drawString(300, 460, str(u.old_product_3_quenity))
                total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
                p.drawString(450, 460, str(total_of_item_3))

                p.line(260, 455, 560, 455)

                p.drawString(300, 440, 'Sub Total = ')
                p.drawString(450, 440, str(u.old_Subtotal_Amount))
                p.drawString(300, 425, 'Delivery = ')
                p.drawString(450, 425, str(u.old_delivery_charge))
                p.drawString(300, 410, 'Greand Total = ')
                p.drawString(450, 410, str(u.old_order_total))


            elif u.old_product_1 and u.old_product_2:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.drawString(44, 475, '2. '+  str(u.old_product_2))
                p.drawString(300, 475, str(u.old_product_2_quenity))
                total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
                p.drawString(450, 475, str(total_of_item_2))

                p.line(260, 470, 560, 470)

                p.drawString(300, 455, 'Sub Total = ')
                p.drawString(450, 455, str(u.old_Subtotal_Amount))
                p.drawString(300, 440, 'Delivery = ')
                p.drawString(450, 440, str(u.old_delivery_charge))
                p.drawString(300, 425, 'Greand Total = ')
                p.drawString(450, 425, str(u.old_order_total))

            elif u.old_product_1:
                p.drawString(44, 490, '1. '+  str(u.old_product_1))
                p.drawString(300, 490, str(u.old_product_1_quenity))
                total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
                p.drawString(450, 490, str(total_of_item_1))

                p.line(260, 485, 560, 485)

                p.drawString(300, 470, 'Sub Total = ')
                p.drawString(450, 470, str(u.old_Subtotal_Amount))

                p.drawString(300, 455, 'Delivery = ')
                p.drawString(450, 455, str(u.old_delivery_charge))
                p.drawString(300, 440, 'Greand Total = ')
                p.drawString(450, 440, str(u.old_order_total))


            # Close the PDF object cleanly, and we're done.
            p.showPage()

        p.save()
        return response
    else:
        return redirect('deshboard_login')





def old_single_invoice(request, get_uniq_user_orders_id_pk):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ' filename="somefilename.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)


        u = Order_Table_3.objects.get(id=get_uniq_user_orders_id_pk)
        k = u.old_order_status

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # p.drawString((+)left, (+)Top, "Hello world.")
        p.setFont("Helvetica", 10)
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

        if k == 'Processing' or k == 'Shifted To Courier':
            i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Paid Seal.png'
            p.drawImage(i, 40, 670, width=60, height=60)

        p.setFont("Helvetica", 25)
        p.drawString(40, 655, "INVOICE")
        p.setFont("Helvetica", 10)
        p.drawString(300, 630, "Order: " + u.old_order_id)
        p.drawString(300, 618, "Date: " + str(u.old_order_date))
        p.drawString(300, 606, "Payment Method: " + u.old_Payment_method[0:35])
        p.drawString(300, 594, u.old_Payment_method[35:])
        # p.drawString(300, 594, "Method:")

        p.drawString(40, 630, str(u.old_customer_first_name) + ' ' + str(u.old_customer_last_name))
        p.drawString(40, 618, str(u.old_Customer_Address)[:40])
        p.drawString(40, 606, str(u.old_Customer_City))
        p.drawString(40, 594, str(u.old_Customer_Postcode))
        p.drawString(40, 582, str(u.old_Customer_Phone))
        p.drawString(40, 570, str(u.old_Customer_Email))

        # color(r,g,b, alpha)
        red50transparent = Color(0, 0, 205, alpha=0.2)
        Yellow = Color(205, 205, 0, alpha=1)
        p.setFillColor(Yellow)
        p.rect(40, 510, 520, 30, fill=False, stroke=True)

        p.setFillColor(black)
        p.drawString(70, 520, "Product")
        p.setFillColor(black)
        p.drawString(300, 520, "Quantity")
        p.setFillColor(black)
        p.drawString(450, 520, "Price")

        p.line(0, 60, 600, 60)

        p.setFillColor(black)
        p.drawString(190, 45, "Thank you for shopping with BoomBoom")
        p.drawString(241, 30, "We Deliver Quality")
        p.drawString(225, 15, "WWW.boomboom.com.bd")

        if u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7 and u.old_product_8 and u.old_product_9 and u.old_product_10:

            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.drawString(44, 430, '5. ' + str(u.old_product_5))
            p.drawString(300, 430, str(u.old_product_5_quenity))
            total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
            p.drawString(450, 430, str(total_of_item_5))

            p.drawString(44, 415, '6. ' + str(u.old_product_6))
            p.drawString(300, 415, str(u.old_product_6_quenity))
            total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
            p.drawString(450, 415, str(total_of_item_6))

            p.drawString(44, 400, '7. ' + str(u.old_product_7))
            p.drawString(300, 400, str(u.old_product_7_quenity))
            total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
            p.drawString(450, 400, str(total_of_item_7))

            p.drawString(44, 385, '8. ' + str(u.old_product_8))
            p.drawString(300, 385, str(u.old_product_8_quenity))
            total_of_item_8 = int(u.old_product_8_quenity) * int(u.old_product_8_price)
            p.drawString(450, 385, str(total_of_item_8))

            p.drawString(44, 370, '9. ' + str(u.old_product_9))
            p.drawString(300, 370, str(u.old_product_9_quenity))
            total_of_item_9 = int(u.old_product_9_quenity) * int(u.old_product_9_price)
            p.drawString(450, 370, str(total_of_item_9))

            p.drawString(44, 355, '10. ' + str(u.old_product_10))
            p.drawString(300, 355, str(u.old_product_10_quenity))
            total_of_item_10 = int(u.old_product_10_quenity) * int(u.old_product_10_price)
            p.drawString(450, 355, str(total_of_item_10))

            p.line(260, 350, 560, 350)

            p.drawString(300, 335, 'Sub Total = ')
            p.drawString(450, 335, str(u.old_Subtotal_Amount))
            p.drawString(300, 320, 'Delivery = ')
            p.drawString(450, 320, str(u.old_delivery_charge))
            p.drawString(300, 305, 'Greand Total = ')
            p.drawString(450, 305, str(u.old_order_total))

        elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7 and u.old_product_8 and u.old_product_9:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.drawString(44, 430, '5. ' + str(u.old_product_5))
            p.drawString(300, 430, str(u.old_product_5_quenity))
            total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
            p.drawString(450, 430, str(total_of_item_5))

            p.drawString(44, 415, '6. ' + str(u.old_product_6))
            p.drawString(300, 415, str(u.old_product_6_quenity))
            total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
            p.drawString(450, 415, str(total_of_item_6))

            p.drawString(44, 400, '7. ' + str(u.old_product_7))
            p.drawString(300, 400, str(u.old_product_7_quenity))
            total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
            p.drawString(450, 400, str(total_of_item_7))

            p.drawString(44, 385, '8. ' + str(u.old_product_8))
            p.drawString(300, 385, str(u.old_product_8_quenity))
            total_of_item_8 = int(u.old_product_8_quenity) * int(u.old_product_8_price)
            p.drawString(450, 385, str(total_of_item_8))

            p.drawString(44, 370, '9. ' + str(u.old_product_9))
            p.drawString(300, 370, str(u.old_product_9_quenity))
            total_of_item_9 = int(u.old_product_9_quenity) * int(u.old_product_9_price)
            p.drawString(450, 370, str(total_of_item_9))

            p.line(260, 365, 560, 365)

            p.drawString(300, 350, 'Sub Total = ')
            p.drawString(450, 350, str(u.old_Subtotal_Amount))
            p.drawString(300, 335, 'Delivery = ')
            p.drawString(450, 335, str(u.old_delivery_charge))
            p.drawString(300, 320, 'Greand Total = ')
            p.drawString(450, 320, str(u.old_order_total))

        elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7 and u.old_product_8:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.drawString(44, 430, '5. ' + str(u.old_product_5))
            p.drawString(300, 430, str(u.old_product_5_quenity))
            total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
            p.drawString(450, 430, str(total_of_item_5))

            p.drawString(44, 415, '6. ' + str(u.old_product_6))
            p.drawString(300, 415, str(u.old_product_6_quenity))
            total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
            p.drawString(450, 415, str(total_of_item_6))

            p.drawString(44, 400, '7. ' + str(u.old_product_7))
            p.drawString(300, 400, str(u.old_product_7_quenity))
            total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
            p.drawString(450, 400, str(total_of_item_7))

            p.drawString(44, 385, '8. ' + str(u.old_product_8))
            p.drawString(300, 385, str(u.old_product_8_quenity))
            total_of_item_8 = int(u.old_product_8_quenity) * int(u.old_product_8_price)
            p.drawString(450, 385, str(total_of_item_8))

            p.line(260, 380, 560, 380)

            p.drawString(300, 365, 'Sub Total = ')
            p.drawString(450, 365, str(u.old_Subtotal_Amount))
            p.drawString(300, 350, 'Delivery = ')
            p.drawString(450, 350, str(u.old_delivery_charge))
            p.drawString(300, 335, 'Greand Total = ')
            p.drawString(450, 335, str(u.old_order_total))

        elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6 and u.old_product_7:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.drawString(44, 430, '5. ' + str(u.old_product_5))
            p.drawString(300, 430, str(u.old_product_5_quenity))
            total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
            p.drawString(450, 430, str(total_of_item_5))

            p.drawString(44, 415, '6. ' + str(u.old_product_6))
            p.drawString(300, 415, str(u.old_product_6_quenity))
            total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
            p.drawString(450, 415, str(total_of_item_6))

            p.drawString(44, 400, '7. ' + str(u.old_product_7))
            p.drawString(300, 400, str(u.old_product_7_quenity))
            total_of_item_7 = int(u.old_product_7_quenity) * int(u.old_product_7_price)
            p.drawString(450, 400, str(total_of_item_7))

            p.line(260, 395, 560, 395)

            p.drawString(300, 380, 'Sub Total = ')
            p.drawString(450, 380, str(u.old_Subtotal_Amount))
            p.drawString(300, 365, 'Delivery = ')
            p.drawString(450, 365, str(u.old_delivery_charge))
            p.drawString(300, 350, 'Greand Total = ')
            p.drawString(450, 350, str(u.old_order_total))

        elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5 and u.old_product_6:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.drawString(44, 430, '5. ' + str(u.old_product_5))
            p.drawString(300, 430, str(u.old_product_5_quenity))
            total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
            p.drawString(450, 430, str(total_of_item_5))

            p.drawString(44, 415, '6. ' + str(u.old_product_6))
            p.drawString(300, 415, str(u.old_product_6_quenity))
            total_of_item_6 = int(u.old_product_6_quenity) * int(u.old_product_6_price)
            p.drawString(450, 415, str(total_of_item_6))

            p.line(260, 410, 560, 410)

            p.drawString(300, 395, 'Sub Total = ')
            p.drawString(450, 395, str(u.old_Subtotal_Amount))
            p.drawString(300, 380, 'Delivery = ')
            p.drawString(450, 380, str(u.old_delivery_charge))
            p.drawString(300, 365, 'Greand Total = ')
            p.drawString(450, 365, str(u.old_order_total))



        elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4 and u.old_product_5:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.drawString(44, 430, '5. ' + str(u.old_product_5))
            p.drawString(300, 430, str(u.old_product_5_quenity))
            total_of_item_5 = int(u.old_product_5_quenity) * int(u.old_product_5_price)
            p.drawString(450, 430, str(total_of_item_5))

            p.line(260, 425, 560, 425)

            p.drawString(300, 410, 'Sub Total = ')
            p.drawString(450, 410, str(u.old_Subtotal_Amount))
            p.drawString(300, 395, 'Delivery = ')
            p.drawString(450, 395, str(u.old_delivery_charge))
            p.drawString(300, 380, 'Greand Total = ')
            p.drawString(450, 380, str(u.old_order_total))


        elif u.old_product_1 and u.old_product_2 and u.old_product_3 and u.old_product_4:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.drawString(44, 445, '4. ' + str(u.old_product_4))
            p.drawString(300, 445, str(u.old_product_4_quenity))
            total_of_item_4 = int(u.old_product_4_quenity) * int(u.old_product_4_price)
            p.drawString(450, 445, str(total_of_item_4))

            p.line(260, 440, 560, 440)

            p.drawString(300, 415, 'Sub Total = ')
            p.drawString(450, 415, str(u.old_Subtotal_Amount))
            p.drawString(300, 400, 'Delivery = ')
            p.drawString(450, 400, str(u.old_delivery_charge))
            p.drawString(300, 385, 'Greand Total = ')
            p.drawString(450, 385, str(u.old_order_total))

        elif u.old_product_1 and u.old_product_2 and u.old_product_3:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.drawString(44, 460, '3. ' + str(u.old_product_3))
            p.drawString(300, 460, str(u.old_product_3_quenity))
            total_of_item_3 = int(u.old_product_3_quenity) * int(u.old_product_3_price)
            p.drawString(450, 460, str(total_of_item_3))

            p.line(260, 455, 560, 455)

            p.drawString(300, 440, 'Sub Total = ')
            p.drawString(450, 440, str(u.old_Subtotal_Amount))
            p.drawString(300, 425, 'Delivery = ')
            p.drawString(450, 425, str(u.old_delivery_charge))
            p.drawString(300, 410, 'Greand Total = ')
            p.drawString(450, 410, str(u.old_order_total))


        elif u.old_product_1 and u.old_product_2:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.drawString(44, 475, '2. ' + str(u.old_product_2))
            p.drawString(300, 475, str(u.old_product_2_quenity))
            total_of_item_2 = int(u.old_product_2_quenity) * int(u.old_product_2_price)
            p.drawString(450, 475, str(total_of_item_2))

            p.line(260, 470, 560, 470)

            p.drawString(300, 455, 'Sub Total = ')
            p.drawString(450, 455, str(u.old_Subtotal_Amount))
            p.drawString(300, 440, 'Delivery = ')
            p.drawString(450, 440, str(u.old_delivery_charge))
            p.drawString(300, 425, 'Greand Total = ')
            p.drawString(450, 425, str(u.old_order_total))

        elif u.old_product_1:
            p.drawString(44, 490, '1. ' + str(u.old_product_1))
            p.drawString(300, 490, str(u.old_product_1_quenity))
            total_of_item_1 = int(u.old_product_1_quenity) * int(u.old_product_1_price)
            p.drawString(450, 490, str(total_of_item_1))

            p.line(260, 485, 560, 485)

            p.drawString(300, 470, 'Sub Total = ')
            p.drawString(450, 470, str(u.old_Subtotal_Amount))

            p.drawString(300, 455, 'Delivery = ')
            p.drawString(450, 455, str(u.old_delivery_charge))
            p.drawString(300, 440, 'Greand Total = ')
            p.drawString(450, 440, str(u.old_order_total))

        # Close the PDF object cleanly, and we're done.
        p.showPage()

        p.save()
        return response
    else:
        return redirect('deshboard_login')




def old_sending_value_to_creat_multiple_csv(request):
    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')
    if staff_admin or staff_shop_manager or staff_customer_support or staff_upload_team:
        old_rrrr_multiple_csv = request.POST.get('old_rrrr_multiple_csv')
        old_rrrr_multiple_csv_json = json.loads(old_rrrr_multiple_csv)
        print('old_rrrr')
        print(old_rrrr_multiple_csv)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename= reguler order.csv'

        writer = csv.writer(response)

        writer.writerow(
            ['Order Number', 'Order Status', 'Order Date','Paid Date', 'First Name (Shipping)', 'Last Name (Shipping)', 'Address 1&2 (Shipping)',
             'City (Shipping)', 'Postcode (Shipping)', 'Email (Shipping)', 'Phone (Shipping)', 'Payment Method Title',
             'Order Total Amount', 'Delivery Charge', 'GrandTotalPrice', 'Shipping Method', 'Item # #1', 'Item Name #1', 'Quantity #1','Price #1',
             'Item # #2', 'Item Name #2', 'Quantity #2','Price #2', 'Item # #3', 'Item Name #3', 'Quantity #3','Price #3', 'Item # #4',
             'Item Name #4', 'Quantity #4','Price #4', 'Item # #5', 'Item Name #5', 'Quantity #5','Price #5', 'Item # #6', 'Item Name #6',
             'Quantity #6','Price #6', 'Item # #7', 'Item Name #7', 'Quantity #7','Price #7', 'Item # #8', 'Item Name #8', 'Quantity #8','Price #8',
             'Item # #9', 'Item Name #9', 'Quantity #9','Price #9', 'Item # #10', 'Item Name #10', 'Quantity #10','Price #10', ])

        # for i in old_rrrr_multiple_csv_json:

        get_row = Order_Table_3.objects.filter(id__in = old_rrrr_multiple_csv_json)
        print('get_row')
        print(get_row)
        for i in get_row:

            writer.writerow([i.old_order_id] + [i.old_order_status]+ [i.old_order_date]+ [i.old_paid_date]+ [i.old_customer_first_name]+ [i.old_customer_last_name]+ [i.old_Customer_Address]+ [i.old_Customer_City]+ [i.old_Customer_Postcode]+ [i.old_Customer_Email]+ [i.old_Customer_Phone]+ [i.old_Payment_method]+ [i.old_Subtotal_Amount]+ [i.old_delivery_charge]+ [i.old_order_total]+ [i.old_Shopping_method]+ [' ']+ [i.old_product_1]+ [i.old_product_1_quenity]+[i.old_product_1_price] + [' ']+ [i.old_product_2]+ [i.old_product_2_quenity]+[i.old_product_2_price]+ [' ']+ [i.old_product_3]+ [i.old_product_3_quenity]+[i.old_product_3_price]+ [' ']+ [i.old_product_4]+ [i.old_product_4_quenity]+[i.old_product_4_price]+ [' ']+ [i.old_product_5]+ [i.old_product_5_quenity]+[i.old_product_5_price]+ [' ']+ [i.old_product_6]+ [i.old_product_6_quenity]+[i.old_product_6_price]+ [' ']+ [i.old_product_7]+ [i.old_product_7_quenity]+[i.old_product_7_price]+ [' ']+ [i.old_product_8]+ [i.old_product_8_quenity]+[i.old_product_8_price]+ [' ']+ [i.old_product_9]+ [i.old_product_9_quenity]+[i.old_product_9_price]+ [' ']+ [i.old_product_10]+ [i.old_product_10_quenity]+[i.old_product_10_price])

        return response
    else:
        return redirect('deshboard_login')