from  django import template
from ..models import campaign_product_table, campaign_table


register = template.Library()



# reguler order count



@register.simple_tag
def count_active_campaign_product():
    
    filter_active_campaign = campaign_table.objects.filter(finish_campaign=False)
    
    total_qty_active_product = 0
    for i in filter_active_campaign:
        filter_active_campaign_product = campaign_product_table.objects.filter(add_item_campaign=True).filter(campaign=i).count()
        total_qty_active_product = total_qty_active_product + filter_active_campaign_product
        
    return total_qty_active_product
