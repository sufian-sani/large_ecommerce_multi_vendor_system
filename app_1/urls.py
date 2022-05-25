
from django.urls import path
from . import views, views2, views3, views4



urlpatterns = [
    path('', views.deshboard_index, name="deshboard_index"),
    path('deshboard_login/', views.deshboard_login, name="deshboard_login"),
    path('dashboard_logout_func/', views.dashboard_logout_func, name="dashboard_logout_func"),
    path('dashbord_order/', views.dashbord_order, name="dashbord_order"),
    path('dashboard_campaign_order/', views.dashboard_campaign_order, name="dashboard_campaign_order"),
    
    path('dashbord_all_product/', views.dashbord_all_product, name="dashbord_all_product"),
    path('dashbord_add_new_products/', views.dashbord_add_new_products, name="dashbord_add_new_products"),
    
    path('dashbord_add_new_products_attribute/', views.dashbord_add_new_products_attribute, name="dashbord_add_new_products_attribute"),
    
    
    path('edit_product_page_add_attribute/', views.edit_product_page_add_attribute, name="edit_product_page_add_attribute"),
    
    
    path('dashbord_Add_Brand/', views.dashbord_Add_Brand, name="dashbord_Add_Brand"),
    path('dashboard_brand_deleted/<str:dashboard_brand_deleted_pk>', views.dashboard_brand_deleted, name="dashboard_brand_deleted"),
    path('dashbord_Categories/', views.dashbord_Categories, name="dashbord_Categories"),
    
    
    #for report
    path('dashboard_csv_product', views2.dashboard_csv_product, name="dashboard_csv_product"),
    path('dashboard_csv_order', views2.dashboard_csv_order, name="dashboard_csv_order"),

    # for old report
    path('dashboard_old_order', views3.dashboard_old_order, name="dashboard_old_order"),
    path('save_the_csv_file_pp', views3.save_the_csv_file_pp, name="save_the_csv_file_pp"),
    path('password_rehash', views3.password_rehash, name="password_rehash"),
    path('old_single_invoice/<int:get_uniq_user_orders_id_pk>', views3.old_single_invoice, name="old_single_invoice"),
    path('old_dashboard_customer_order_edit/<int:dashboard_old_order_pk>', views3.old_dashboard_customer_order_edit, name="old_dashboard_customer_order_edit"),
    path('save_old_order_status_single/<int:save_old_order_status_single_pk>', views3.save_old_order_status_single, name="save_old_order_status_single"),
    path('old_order_table_3_change_status', views3.old_order_table_3_change_status, name="old_order_table_3_change_status"),
    path('old_sending_value_to_creat_multiple_invoice', views3.old_sending_value_to_creat_multiple_invoice, name="old_sending_value_to_creat_multiple_invoice"),
    path('old_sending_value_to_creat_multiple_csv', views3.old_sending_value_to_creat_multiple_csv, name="old_sending_value_to_creat_multiple_csv"),

    #ediet category
    path('edited_catagory_dashboard/<str:all_categories_id>', views2.edited_catagory_dashboard, name="edited_catagory_dashboard"),
    path('delete_catagory_dashboard/<str:all_categories_id>', views2.delete_catagory_dashboard, name="delete_catagory_dashboard"),
    path('save_edited_catagory_dashboard/', views2.save_edited_catagory_dashboard, name="save_edited_catagory_dashboard"),

    #subcategory 1
    path('edited_subcategories_1_dashboard/<str:all_subcategories_id>', views2.edited_subcategories_1_dashboard, name="edited_subcategories_1_dashboard"),
    path('delete_subcategories_1_dashboard/<str:all_subcategories_id>', views2.delete_subcategories_1_dashboard, name="delete_subcategories_1_dashboard"),
    path('save_edited_subcatagory_1_dashboard/', views2.save_edited_subcatagory_1_dashboard, name="save_edited_subcatagory_1_dashboard"),

    #subcategory 2
    path('edited_subcategories_2_dashboard/<str:all_subcategories2_id>', views2.edited_subcategories_2_dashboard, name="edited_subcategories_2_dashboard"),
    path('delete_subcategories_2_dashboard/<str:all_subcategories2_id>', views2.delete_subcategories_2_dashboard, name="delete_subcategories_2_dashboard"),
    path('save_edited_subcatagory_2_dashboard/', views2.save_edited_subcatagory_2_dashboard, name="save_edited_subcatagory_2_dashboard"),

    # this is for all csv
    path('all_product_order_for_csv/', views2.all_product_order_for_csv, name="all_product_order_for_csv"),

    #this for dashbord_Attribute
    path('dashbord_Attribute/', views.dashbord_Attribute, name="dashbord_Attribute"),
    path('dashbord_Attribute_save/', views.dashbord_Attribute_save, name="dashbord_Attribute_save"),
    path('edited_dashbord_Attribute_save_final/<int:pk_edited_save_again>', views.edited_dashbord_Attribute_save_final, name="edited_dashbord_Attribute_save_final"),
    path('edit_dashbord_Attribute_save/<int:pk_edit_dashbord_Attribute_save>', views.edit_dashbord_Attribute_save, name="edit_dashbord_Attribute_save"),
    
    path('value_dashbord_Attribute/<int:pk_value_dashbord_Attribute>', views.value_dashbord_Attribute, name="value_dashbord_Attribute"),
    path('save_value_of_attribute/<int:pk_Attribute_value_dashbord_Attribute>', views.save_value_of_attribute, name="save_value_of_attribute"),
    
    path('dashboard_attribute_value_delete/', views.dashboard_attribute_value_delete, name="dashboard_attribute_value_delete"),
    path('dashboard_attribute_value_edit/', views.dashboard_attribute_value_edit, name="dashboard_attribute_value_edit"),
    path('save_dashboard_attribute_value_edit/', views.save_dashboard_attribute_value_edit, name="save_dashboard_attribute_value_edit"),
    
    path('delete_edited_add_attribute_form_add_product/<str:i_connect_with_product_slug>', views.delete_edited_add_attribute_form_add_product, name="delete_edited_add_attribute_form_add_product"),
    path('EDIT_edited_add_attribute_form_add_product/<str:i_connect_with_product_slug>', views.EDIT_edited_add_attribute_form_add_product, name="EDIT_edited_add_attribute_form_add_product"),
    path('save_EDIT_edited_add_attribute_form_add_product/', views.save_EDIT_edited_add_attribute_form_add_product, name="save_EDIT_edited_add_attribute_form_add_product"),

    
    
    path('save_brand', views.save_brand, name="save_brand"),
    path('change_status_star', views.change_status_star, name="change_status_star"),
    path('change_undo_status_star', views.change_undo_status_star, name="change_undo_status_star"),
    path('delete_the_prod_row', views.delete_the_prod_row, name="delete_the_prod_row"),
    path('edited_product_page/<str:pk>', views.edited_product_page, name="edited_product_page"),
    path('edit_product_save', views.edit_product_save, name="edit_product_save"),
    path('filter_action', views.filter_action, name="filter_action"),
    path('get_sub_cat', views.get_sub_cat, name="get_sub_cat"),
    path('get_sub_cat2', views.get_sub_cat2, name="get_sub_cat2"),
    path('move_to_trash_selected_checkbox', views.move_to_trash_selected_checkbox, name="move_to_trash_selected_checkbox"),
    path('order_table_change_status', views.order_table_change_status, name="order_table_change_status"),
    path('dashboard_order_filter', views.dashboard_order_filter, name="dashboard_order_filter"),
    path('dashboard_order_filter_campaign', views.dashboard_order_filter_campaign, name="dashboard_order_filter_campaign"),
    path('search_order_id', views.search_order_id, name="search_order_id"),
    path('search_order_id_campaign', views.search_order_id_campaign, name="search_order_id_campaign"),
    path('activated_vendors', views.activated_vendors, name="activated_vendors"),
    path('vendor_deactivate', views.vendor_deactivate, name="vendor_deactivate"),
    path('filter_vendor_date', views.filter_vendor_date, name="filter_vendor_date"),
    path('search_vendor_other', views.search_vendor_other, name="search_vendor_other"),
    path('add_vendors_by_upload', views.add_vendors_by_upload, name="add_vendors_by_upload"),
    path('pending_vendors', views.pending_vendors, name="pending_vendors"),
    path('vendor_activate', views.vendor_activate, name="vendor_activate"),
    path('filter_vendor_date_deactive', views.filter_vendor_date_deactive, name="filter_vendor_date_deactive"),
    path('search_vendor_other_deactive', views.search_vendor_other_deactive, name="search_vendor_other_deactive"),
    path('upload_vendor_Store_details/<str:pk>', views.upload_vendor_Store_details, name="upload_vendor_Store_details"),
    path('upload_vendor_info_edit/<str:pk2>', views.upload_vendor_info_edit, name="upload_vendor_info_edit"),
    path('upload_save_vendor_info_edit/<str:pk3>', views.upload_save_vendor_info_edit, name="upload_save_vendor_info_edit"),
    path('upload_vendor_info_password_edit/<str:pk4>', views.upload_vendor_info_password_edit, name="upload_vendor_info_password_edit"),
    path('upload_save_vendor_info_password_edit/<str:pk4>', views.upload_save_vendor_info_password_edit, name="upload_save_vendor_info_password_edit"),
    path('dashboard_brand_edit/<str:dashboard_brand_edit_pk>', views.dashboard_brand_edit, name="dashboard_brand_edit"),
    
    path('dashboard_customer_order_edit/<str:pk>', views.dashboard_customer_order_edit, name="dashboard_customer_order_edit"),
    
    path('deshboard_customer_find_by_search', views.deshboard_customer_find_by_search, name="deshboard_customer_find_by_search"),
    path('deshboard_product_find_by_search', views.deshboard_product_find_by_search, name="deshboard_product_find_by_search"),
    
    path('delete_item_from_order/<str:pk>', views.delete_item_from_order, name='delete_item_from_order'),
    
    path('update_ordr_prdtble2', views.update_ordr_prdtble2, name="update_ordr_prdtble2"),
    
    path('submit_edited_order', views.submit_edited_order, name="submit_edited_order"),
    
    
    
    
    
    
    path('Analytics_Overview', views.Analytics_Overview, name="Analytics_Overview"),
    path('Analytics_Products', views.Analytics_Products, name="Analytics_Products"),
    path('Analytics_Categories', views.Analytics_Categories, name="Analytics_Categories"),
    path('Analytics_Revenue', views.Analytics_Revenue, name="Analytics_Revenue"),
    
    path('Analytics_orders', views.Analytics_orders, name="Analytics_orders"),
    path('Analytics_brands', views.Analytics_brands, name="Analytics_brands"),
    path('Analytics_vendor', views.Analytics_vendor, name="Analytics_vendor"),
    
    path('dashboard_Add_customer', views.dashboard_Add_customer, name="dashboard_Add_customer"),
    path('dashboard_view_all_customer', views.dashboard_view_all_customer, name="dashboard_view_all_customer"),
    
    
    path('dashboard_customer_profile_edit/<str:pk>', views.dashboard_customer_profile_edit, name="dashboard_customer_profile_edit"),
    path('resave_user_info_dashboard_customer_profile_edit', views.resave_user_info_dashboard_customer_profile_edit, name="resave_user_info_dashboard_customer_profile_edit"),
    
    
    
    path('dashboard_customer_order_edit_Generate_Invoice/<str:pk>', views.dashboard_customer_order_edit_Generate_Invoice, name="dashboard_customer_order_edit_Generate_Invoice"),
    
    
    path('dashboard_customer_id_making', views.dashboard_customer_id_making, name="dashboard_customer_id_making"),
    
    
    
    path('sending_value_to_creat_multiple_invoice', views.sending_value_to_creat_multiple_invoice, name="sending_value_to_creat_multiple_invoice"),
    
    path('sending_value_to_creat_multiple_csv', views.sending_value_to_creat_multiple_csv, name="sending_value_to_creat_multiple_csv"),
    
    path('create_flash_sale', views.create_flash_sale, name="create_flash_sale"),
    path('add_flash_sale', views.add_flash_sale, name="add_flash_sale"),
    path('edit_flash/<str:pk>', views.edit_flash, name="edit_flash"),
    path('delete_flash/<str:pk>', views.delete_flash, name="delete_flash"),
    
    
    path('add_attributes/<str:pk>', views.add_attributes, name="add_attributes"),



    path('dashboard_customer_order_edit_Generate_Refunded_Invoice/', views4.dashboard_customer_order_edit_Generate_Refunded_Invoice, name="dashboard_customer_order_edit_Generate_Refunded_Invoice"),
    # path('dashboard_customer_order_edit_Generate_completed_Invoice/', views4.dashboard_customer_order_edit_Generate_completed_Invoice, name="dashboard_customer_order_edit_Generate_completed_Invoice"),

    
]