from  django import template
from ..models import Order_Table, Order_Table_3


register = template.Library()



# reguler order count


@register.simple_tag
def count_old_order():
    get_count_old_order = Order_Table_3.objects.all().count()
    return get_count_old_order


@register.simple_tag
def count_Pending_payment():
    get_count_Pending_payment = Order_Table.objects.filter(Order_Status="Pending payment").filter(Campaign_Status="Reguler").count()
    return get_count_Pending_payment

@register.simple_tag
def count_Processing():
    get_count_Processing = Order_Table.objects.filter(Order_Status="Processing").filter(Campaign_Status="Reguler").count()
    return get_count_Processing

@register.simple_tag
def count_Completed():
    get_count_Completed = Order_Table.objects.filter(Order_Status="Completed").filter(Campaign_Status="Reguler").count()
    return get_count_Completed

@register.simple_tag
def count_Cancelled():
    get_count_Cancelled = Order_Table.objects.filter(Order_Status="Cancelled").filter(Campaign_Status="Reguler").count()
    return get_count_Cancelled

@register.simple_tag
def count_Refunded():
    get_count_Refunded = Order_Table.objects.filter(Order_Status="Refunded").filter(Campaign_Status="Reguler").count()
    return get_count_Refunded

@register.simple_tag
def count_Picked():
    get_count_Picked = Order_Table.objects.filter(Order_Status="Picked").filter(Campaign_Status="Reguler").count()
    return get_count_Picked

@register.simple_tag
def count_On_hold():
    get_count_On_hold = Order_Table.objects.filter(Order_Status="On hold").filter(Campaign_Status="Reguler").count()
    return get_count_On_hold

@register.simple_tag
def count_All_Orders():
    get_count_All_Orders = Order_Table.objects.filter(Campaign_Status="Reguler").count()
    return get_count_All_Orders
    

@register.simple_tag
def count_deposit_slip():
    # get_count_deposit_slip_none = Order_Table.objects.filter(Deposit_slip__exact='').count()
    get_count_deposit_slip_none = Order_Table.objects.exclude(Deposit_slip='').filter(Campaign_Status="Reguler").count()
    return get_count_deposit_slip_none
    
    
    
    # campaign order count


@register.simple_tag
def count_Pending_payment_campaign():
    get_count_Pending_payment = Order_Table.objects.filter(Order_Status="Pending payment").filter(Campaign_Status="Campaign").count()
    return get_count_Pending_payment

@register.simple_tag
def count_Processing_campaign():
    get_count_Processing = Order_Table.objects.filter(Order_Status="Processing").filter(Campaign_Status="Campaign").count()
    return get_count_Processing

@register.simple_tag
def count_Completed_campaign():
    get_count_Completed = Order_Table.objects.filter(Order_Status="Completed").filter(Campaign_Status="Campaign").count()
    return get_count_Completed

@register.simple_tag
def count_Cancelled_campaign():
    get_count_Cancelled = Order_Table.objects.filter(Order_Status="Cancelled").filter(Campaign_Status="Campaign").count()
    return get_count_Cancelled

@register.simple_tag
def count_Refunded_campaign():
    get_count_Refunded = Order_Table.objects.filter(Order_Status="Refunded").filter(Campaign_Status="Campaign").count()
    return get_count_Refunded

@register.simple_tag
def count_Picked_campaign():
    get_count_Picked = Order_Table.objects.filter(Order_Status="Picked").filter(Campaign_Status="Campaign").count()
    return get_count_Picked

@register.simple_tag
def count_On_hold_campaign():
    get_count_On_hold = Order_Table.objects.filter(Order_Status="On hold").filter(Campaign_Status="Campaign").count()
    return get_count_On_hold

@register.simple_tag
def count_All_Orders_campaign():
    get_count_All_Orders = Order_Table.objects.filter(Campaign_Status="Campaign").count()
    return get_count_All_Orders
    

@register.simple_tag
def count_deposit_slip_campaign():
    # get_count_deposit_slip_none = Order_Table.objects.filter(Deposit_slip__exact='').count()
    get_count_deposit_slip_none = Order_Table.objects.exclude(Deposit_slip='').filter(Campaign_Status="Campaign").count()
    return get_count_deposit_slip_none
    
    
    
    # base show
    
    
    
@register.simple_tag
def count_reguler_order():
    filter_count_reguler_order = Order_Table.objects.filter(Campaign_Status="Reguler").count()
    return filter_count_reguler_order
    
    
@register.simple_tag
def count_campaign_order():
    filter_count_campaign_order = Order_Table.objects.filter(Campaign_Status="Campaign").count()
    return filter_count_campaign_order
    
    
    
