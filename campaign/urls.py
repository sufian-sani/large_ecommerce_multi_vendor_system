from django.urls import path
from . import views


urlpatterns = [
    path('create_campaign', views.create_campaign, name="create_campaign"),
    path('add_category_percentage/<int:pk>', views.add_category_percentage, name="add_category_percentage"),
    path('add_campaign_name/', views.add_campaign_name, name="add_campaign_name"),
    path('save_categories_percentages', views.save_categories_percentages, name="save_categories_percentages"),
    path('campaign_details/<int:pk>', views.campaign_details, name="campaign_details"),
    path('edit_categories_percentages', views.edit_categories_percentages, name="edit_categories_percentages"),
    path('products_campaign', views.products_campaign, name="products_campaign"),
    path('cam_cat/<int:pk>', views.cam_cat, name="cam_cat"),
    path('add_products_to_cam/<int:pk>', views.add_products_to_cam, name="add_products_to_cam"),
    path('save_product_campaign', views.save_product_campaign, name="save_product_campaign"),
    path('save_unselected_product_campaign', views.save_unselected_product_campaign, name="save_unselected_product_campaign"),
    
    
    path('remove_products_campaign', views.remove_products_campaign, name="remove_products_campaign"),
    path('add_availble_products_campaign', views.add_availble_products_campaign, name="add_availble_products_campaign"),
    path('edit_add_products_to_camp/<int:pk>', views.edit_add_products_to_camp, name='edit_add_products_to_camp'),
    path('adding_more_products_campaign', views.adding_more_products_campaign, name="adding_more_products_campaign"),
    path('campaign_change_status_star', views.campaign_change_status_star, name="campaign_change_status_star"),
    path('campaign_change_status_home_star', views.campaign_change_status_home_star, name="campaign_change_status_home_star"),
    
    path('campaign_change_undo_status_star', views.campaign_change_undo_status_star, name="campaign_change_undo_status_star"),
    path('campaign_change_undo_status_home_star', views.campaign_change_undo_status_home_star, name="campaign_change_undo_status_home_star"),
    
    path('save_blank_categories_percentages', views.save_blank_categories_percentages, name="save_blank_categories_percentages"),
    path('save_change_percentage_prod', views.save_change_percentage_prod, name="save_change_percentage_prod"),
    path('save_change_price_prod', views.save_change_price_prod, name="save_change_price_prod"),
    path('finish_campaign_deshbrd', views.finish_campaign_deshbrd, name="finish_campaign_deshbrd"),
    path('summery_campaign', views.summery_campaign, name="summery_campaign"),
    
    path('campaign_product_add_attribute/<str:pk>', views.campaign_product_add_attribute, name="campaign_product_add_attribute"),
    
    path('edit_campaign_product_attr', views.edit_campaign_product_attr, name="edit_campaign_product_attr"),
]