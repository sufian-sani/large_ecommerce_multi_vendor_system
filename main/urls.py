from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


from .views import CategoriesListView


urlpatterns=[
    path('',views.home,name='home'),
    
    #path('', CategoriesListView.as_view(), name='home'),
    
    path('category_list',views.category_list,name='category-list'),
    path('brand_list', views.brand_list, name='brand_list'),
    path('showing_product_by_brands/<str:s_brand_pk>', views.showing_product_by_brands, name='showing_product_by_brands'),

    
    
    path('product_list', views.product_list, name='product-list'),
    path('product_list_Z_to_A', views.product_list_Z_to_A, name='product_list_Z_to_A'),
    path('product_list_Price_Lowest_first', views.product_list_Price_Lowest_first, name='product_list_Price_Lowest_first'),
    path('product_list_Price_Highest_first', views.product_list_Price_Highest_first, name='product_list_Price_Highest_first'),
    #path('product_list', product_ListView.as_view(), name="product-list"),
    
    path('product_details/<str:slug>',views.product_details,name='product_details'),
    
    path('campaign_product_details/<str:slug>', views.campaign_product_details, name="campaign_product_details"),
    
    path('customer_dashboard',views.customer_dashboard,name='customer-dashboard'),
    path('cart_page/',views.cart_page,name='cart_page'),
    
    path('stores/',views.stores,name='stores'),
    path('search_store_user_page/',views.search_store_user_page,name='search_store_user_page'),
    
    path('single_vendor/<str:s_v_pk>',views.single_vendor,name='single_vendor'),
    path('vendor_price_filter', views.vendor_price_filter, name="vendor_price_filter"),
    path('vendor_category', views.vendor_category, name="vendor_category"),
    
    # campaign
    path('campaign_page', views.campaign_page, name='campaign_page'),
    path('campaign_landing/<str:pk>',views.campaign_landing,name='campaign_landing'),
    path('category_campaign_product/<int:pk>',views.category_campaign_product,name='category_campaign_product'),
    path('camcat_land/<int:pk>',views.camcat_land,name='camcat_land'),
    path('show_campaign_brands_products',views.show_campaign_brands_products,name='show_campaign_brands_products'),

    path('customer_order_view/<str:pk>',views.customer_order_view,name='customer_order_view'),
    path('old_customer_order_view/<str:pk>',views.old_customer_order_view,name='old_customer_order_view'),


    path('customer_pay_order/<str:pk>', views.customer_pay_order, name="customer_pay_order"),
    
    path('bank_deposite_submit', views.bank_deposite_submit, name="bank_deposite_submit"),
    
    path('cancel_order', views.cancel_order, name="cancel_order"),
    
    path('save_customer_review', views.save_customer_review, name="save_customer_review"),
    path('update_avarage_rat_url', views.update_avarage_rat_url, name="update_avarage_rat_url"),
    path('func_update_star_rat_url', views.func_update_star_rat_url, name="func_update_star_rat_url"),
    
    path('get_all_cats', views.get_all_cats, name="get_all_cats"),
    path('category_products/<int:pk>', views.category_products, name="category_products"),
    path('subcategory_products/<int:pk>', views.subcategory_products, name="subcategory_products"),
    
    path('flash_details_product/<str:pk>', views.flash_details_product, name="flash_details_product"),
    
    path('search_main_box', views.search_main_box, name="search_main_box"),
    path('submit_search_word', views.submit_search_word, name="submit_search_word"),
    
    path('product_list_sort', views.product_list_sort, name="product_list_sort"),
    
    path('price_filter', views.price_filter, name="price_filter"),
    
    path('wishlist', views.wishlist, name="wishlist"),
    path('campaign_wishlist', views.campaign_wishlist, name="campaign_wishlist"),
    path('add_campaign_product_wishlist', views.add_campaign_product_wishlist, name="add_campaign_product_wishlist"),
    path('remove_campaign_product_wishlist', views.remove_campaign_product_wishlist, name="remove_campaign_product_wishlist"),
    
    path('add_reguler_product_wishlist', views.add_reguler_product_wishlist, name="add_reguler_product_wishlist"),
    path('remove_reguler_product_wishlist', views.remove_reguler_product_wishlist, name="remove_reguler_product_wishlist"),
    
    path('check_and_send_otp', views.check_and_send_otp, name="check_and_send_otp"),
    path('change_password_confirm', views.change_password_confirm, name="change_password_confirm"),

    # sslcommerz call back url
    path('payment-successful', views.payment_success, name="payment-successful"),


    path('send_sms', views.send_sms, name="send_sms"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
