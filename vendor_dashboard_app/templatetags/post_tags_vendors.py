from  django import template
from ..models import vendor_registration_table
from checkout.models import Order_Table


register = template.Library()


@register.simple_tag
def count_active_vendors():
    filter_count_active_vendors = vendor_registration_table.objects.filter(vendor_activation=True).count()
    return filter_count_active_vendors

@register.simple_tag
def count_pending_vendors():
    filter_count_pending_vendors = vendor_registration_table.objects.filter(vendor_activation=False).count()
    return filter_count_pending_vendors

    
    
    
    
    
