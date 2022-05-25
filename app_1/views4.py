from django.shortcuts import render,HttpResponse, redirect
from checkout.models import Order_Table, Order_Table_2
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.colors import Color, black, blue, red
import math
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def dashboard_customer_order_edit_Generate_Refunded_Invoice1(request):
    print('lllll')
    Generate_Refunded_Invoice_order_id = request.POST.get('Generate_Refunded_Invoice_order_id')
    return HttpResponse(Generate_Refunded_Invoice_order_id)


def dashboard_customer_order_edit_Generate_Refunded_Invoice(request):

    staff_admin = request.session.get('deshboard_admin_username')
    staff_shop_manager = request.session.get('deshboard_shop_manager_username')
    staff_customer_support = request.session.get('deshboard_customer_support_username')
    staff_upload_team = request.session.get('deshboard_upload_team_username')

    if staff_admin or staff_shop_manager or staff_upload_team:
        Generate_Refunded_Invoice_order_id = request.POST.get('Generate_Refunded_Invoice_order_id')
        hidden_Refunded = request.POST.get('hidden_Refunded')
        Invoice_get_ordr_tbl = Order_Table.objects.get(Order_Id=Generate_Refunded_Invoice_order_id)
        Invoice_filter_ordr_tbl_2 = Order_Table_2.objects.filter(Order_Id=Invoice_get_ordr_tbl)

        invoice_subtotal_amount = Invoice_get_ordr_tbl.SubTotal_Price
        invoice_Delivery_Charge = Invoice_get_ordr_tbl.Delivery_Charge
        invoice_GrandTotal_Price = Invoice_get_ordr_tbl.GrandTotal_Price

        get_sub = Invoice_get_ordr_tbl.SubTotal_Price
        ggt = get_sub
        ggtt = Invoice_get_ordr_tbl.GrandTotal_Price
        ggtt_get = ggtt
        for i in Invoice_filter_ordr_tbl_2:

            # if i.New_Order_Status =='Refunded':
            #     invoice_subtotal_amount = ggt
            #     invoice_GrandTotal_Price = ggtt_get
            #
            # else:
            #     ggt = ggt - i.then_price * i.Quantity
            #     invoice_subtotal_amount = ggt
            #     ggtt_get = ggtt_get - i.then_price * i.Quantity

            if hidden_Refunded == 'Refunded':
                if i.New_Order_Status =='Refunded':
                    invoice_subtotal_amount = ggt
                else:
                    ggt = ggt - i.then_price * i.Quantity
                    invoice_subtotal_amount = ggt
                    ggtt_get = ggtt_get - i.then_price * i.Quantity

            if hidden_Refunded == 'Compleated':
                if i.New_Order_Status =='Completed':
                    invoice_subtotal_amount = ggt
                else:
                    ggt = ggt - i.then_price * i.Quantity
                    invoice_subtotal_amount = ggt
                    ggtt_get = ggtt_get - i.then_price * i.Quantity

        invoice_GrandTotal_Price = invoice_subtotal_amount+invoice_Delivery_Charge









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

            if hidden_Refunded == 'Refunded':
                if i.New_Order_Status =='Refunded':
                    Product_list.append(i.Product)
                    Quantity_list.append(i.Quantity)
                    SubTotal_Price_list.append(i.SubTotal_Price)
                    k = i.New_Order_Status
                else:
                    pass
            if hidden_Refunded == 'Compleated':
                if i.New_Order_Status =='Completed':
                    Product_list.append(i.Product)
                    Quantity_list.append(i.Quantity)
                    SubTotal_Price_list.append(i.SubTotal_Price)
                    k = i.New_Order_Status
                else:
                    pass

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

            # i = 'https://idjangoo.com/static/images/logo-main.png'
            # p.drawImage(i, 40, 730, width=270, height=72)
            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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
            #
            # if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "approx 10% Paid =")
            #     position_Quantity_list = position_Quantity_list - 20
            #     p.drawString(385, position_Quantity_list, "approx 90% Due =")
            #
            #     # finding 10 percent of invoice_subtotal_amount
            #
            #     _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge
            #
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
            #         _10pescent_pluse_delevary_invoice_subtotal_amount)
            #
            #     _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))
            #
            #
            # elif Invoice_get_ordr_tbl.Order_Status == 'Processing':
            #
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "100% Paid =")
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount)+'ssss')

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

            i = f'{MEDIA_ROOT}\Product invoice logo\logo-main.png'
            p.drawImage(i, 40, 730, width=270, height=72)

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            # if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "approx 10% Paid =")
            #     position_Quantity_list = position_Quantity_list - 20
            #     p.drawString(385, position_Quantity_list, "approx 90% Due =")
            #
            #     # finding 10 percent of invoice_subtotal_amount
            #
            #     _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge
            #
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
            #         _10pescent_pluse_delevary_invoice_subtotal_amount)
            #
            #     _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))
            #
            #
            # elif Invoice_get_ordr_tbl.Order_Status == 'Processing':
            #
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "100% Paid =")
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            # if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "approx 10% Paid =")
            #     position_Quantity_list = position_Quantity_list - 20
            #     p.drawString(385, position_Quantity_list, "approx 90% Due =")
            #
            #     # finding 10 percent of invoice_subtotal_amount
            #
            #     _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge
            #
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
            #         _10pescent_pluse_delevary_invoice_subtotal_amount)
            #
            #     _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))
            #
            #
            # elif Invoice_get_ordr_tbl.Order_Status == 'Processing':
            #
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "100% Paid =")
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            # if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "approx 10% Paid =")
            #     position_Quantity_list = position_Quantity_list - 20
            #     p.drawString(385, position_Quantity_list, "approx 90% Due =")
            #
            #     # finding 10 percent of invoice_subtotal_amount
            #
            #     _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge
            #
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
            #         _10pescent_pluse_delevary_invoice_subtotal_amount)
            #
            #     _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))
            #
            #
            # elif Invoice_get_ordr_tbl.Order_Status == 'Processing':
            #
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "100% Paid =")
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            # if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "approx 10% Paid =")
            #     position_Quantity_list = position_Quantity_list - 20
            #     p.drawString(385, position_Quantity_list, "approx 90% Due =")
            #
            #     # finding 10 percent of invoice_subtotal_amount
            #
            #     _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge
            #
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
            #         _10pescent_pluse_delevary_invoice_subtotal_amount)
            #
            #     _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))
            #
            #
            # elif Invoice_get_ordr_tbl.Order_Status == 'Processing':
            #
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "100% Paid =")
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            if k == 'Refunded':
                i = f'{MEDIA_ROOT}\Product invoice logo\BoomBoom Refund Seal.png'
                p.drawImage(i, 40, 670, width=60, height=60)

            if k == 'Completed':
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

            # if Invoice_get_ordr_tbl.Order_Status == 'Partially Paid':
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "approx 10% Paid =")
            #     position_Quantity_list = position_Quantity_list - 20
            #     p.drawString(385, position_Quantity_list, "approx 90% Due =")
            #
            #     # finding 10 percent of invoice_subtotal_amount
            #
            #     _10pescent_invoice_subtotal_amount = (10 * invoice_subtotal_amount) / 100
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = _10pescent_invoice_subtotal_amount + invoice_Delivery_Charge
            #
            #     _10pescent_pluse_delevary_invoice_subtotal_amount = math.floor(
            #         _10pescent_pluse_delevary_invoice_subtotal_amount)
            #
            #     _10pescent_leving_invoice_GrandTotal_Price = invoice_GrandTotal_Price - _10pescent_pluse_delevary_invoice_subtotal_amount
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_pluse_delevary_invoice_subtotal_amount))
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(_10pescent_leving_invoice_GrandTotal_Price))
            #
            #
            # elif Invoice_get_ordr_tbl.Order_Status == 'Processing':
            #
            #     position_Quantity_list = position_Quantity_list - 20
            #     line_position_Quantity_list = position_Quantity_list + 15
            #     p.line(250, line_position_Quantity_list, 557, line_position_Quantity_list)
            #     p.drawString(385, position_Quantity_list, "100% Paid =")
            #
            #     position_SubTotal_Price_list = position_SubTotal_Price_list - 20
            #     p.drawString(480, position_SubTotal_Price_list, str(invoice_subtotal_amount))

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

