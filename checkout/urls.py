from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkout_func, name='checkout_func'),
    path('save_customer_delivery_info', views.save_customer_delivery_info, name='save_customer_delivery_info'),
    path('get_last_oder_ID', views.get_last_oder_ID, name='get_last_oder_ID'),
    path('save_all_orders_one_by_one', views.save_all_orders_one_by_one, name='save_all_orders_one_by_one'),
    path('save_all_campaign_orders_one_by_one', views.save_all_campaign_orders_one_by_one, name='save_all_campaign_orders_one_by_one'),
    path('order_save_with_all_info', views.order_save_with_all_info, name='order_save_with_all_info'),
    path('Offer_not_available', views.Offer_not_available, name="Offer_not_available"),
]