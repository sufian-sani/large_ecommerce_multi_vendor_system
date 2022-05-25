from django.urls import path
from . import views


urlpatterns = [
    path('', views.vendor_dashboard_index, name='vendor_dashboard_index'),
    path('vendor_registration/', views.vendor_registration, name='vendor_registration'),
    path('vendor_login/', views.vendor_login, name='vendor_login'),
    path('save_vendor_registration/', views.save_vendor_registration, name='save_vendor_registration'),
    
    path('cheake_otp_for_vendor_registration/', views.cheake_otp_for_vendor_registration, name='cheake_otp_for_vendor_registration'),
    path('third_stap_to_save_vendor_registration/', views.third_stap_to_save_vendor_registration, name='third_stap_to_save_vendor_registration'),

    
    path('cheake_vendor_login_details', views.cheake_vendor_login_details, name='cheake_vendor_login_details'),
    path('vendor_dashboard_logout_func', views.vendor_dashboard_logout_func, name='vendor_dashboard_logout_func'),
    path('vendor_Store_details', views.vendor_Store_details, name='vendor_Store_details'),
    path('vendor_info_edit', views.vendor_info_edit, name='vendor_info_edit'),
    path('vendor_info_password_edit', views.vendor_info_password_edit, name='vendor_info_password_edit'),
    path('save_vendor_info_edit', views.save_vendor_info_edit, name='save_vendor_info_edit'),
    path('save_vendor_info_password_edit', views.save_vendor_info_password_edit, name='save_vendor_info_password_edit'),
    path('vendor_dashbord_add_new_products', views.vendor_dashbord_add_new_products, name='vendor_dashbord_add_new_products'),  
    path('save_vendor_dashbord_add_new_products', views.save_vendor_dashbord_add_new_products, name='save_vendor_dashbord_add_new_products'),
    path('vendor_All_Products_show', views.vendor_All_Products_show, name='vendor_All_Products_show'),
    path('move_to_trash_selected_checkbox_vendors', views.move_to_trash_selected_checkbox_vendors, name="move_to_trash_selected_checkbox_vendors"),
    path('filter_action_vendor', views.filter_action_vendor, name="filter_action_vendor"),
    
    path('vendor_personal_orders', views.vendor_personal_orders, name='vendor_personal_orders'),
    
    path('vendor_edited_product_page/<str:pk>', views.vendor_edited_product_page, name='vendor_edited_product_page'),
    path('vendor_edit_product_save', views.vendor_edit_product_save, name='vendor_edit_product_save'),
    
    
    path('get_vendor_pending_payments_qty', views.get_vendor_pending_payments_qty, name="get_vendor_pending_payments_qty"),
    path('get_vendor_processing_qty', views.get_vendor_processing_qty, name="get_vendor_processing_qty"),
    
    path('get_vendor_complete_qty', views.get_vendor_complete_qty, name="get_vendor_complete_qty"),
    path('get_vendor_cencel_qty', views.get_vendor_cencel_qty, name="get_vendor_cencel_qty"),
    path('get_vendor_refunded_qty', views.get_vendor_refunded_qty, name="get_vendor_refunded_qty"),
    path('get_vendor_picked_qty', views.get_vendor_picked_qty, name="get_vendor_picked_qty"),
    path('get_vendor_hold_qty', views.get_vendor_hold_qty, name="get_vendor_hold_qty"),
    path('get_vendor_deposite_qty', views.get_vendor_deposite_qty, name="get_vendor_deposite_qty"),
    path('get_vendor_all_qty', views.get_vendor_all_qty, name="get_vendor_all_qty"),
    
    
    
    path('vendor_dashboard_order_filter', views.vendor_dashboard_order_filter, name="vendor_dashboard_order_filter"),
    path('vendor_search_order_id', views.vendor_search_order_id, name="vendor_search_order_id"),
    path('vendor_check_and_send_otp', views.vendor_check_and_send_otp, name="vendor_check_and_send_otp"),
    path('vendor_change_password_confirm', views.vendor_change_password_confirm, name="vendor_change_password_confirm"),

]