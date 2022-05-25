from django.forms import ModelForm
from .models import Category, Subcategory_1, Subcategory_2, Products, Brand, Flash_Sell
from checkout.models import Order_Table, Customer_delivery_information


class edit_order_detail(ModelForm):
    class Meta:
        model = Order_Table
        fields = ['Order_Status', 'Shopping', 'shipping_note', 'Delivery_Charge']


class edit_Customer_delivery_info(ModelForm):
    class Meta:
        model = Customer_delivery_information
        fields = ['First_Name', 'Last_Name', 'Street_Address', 'Town_City', 'District', 'Post_Code', 'Phone_Number', 'Email_Address']



class add_brand(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'



class add_category(ModelForm):
    class Meta:
        model = Category
        fields = ['Category_Name', 'Category_title', 'Category_discription', 'Category_benner']


# for making subcategories
class add_Subcategory_1(ModelForm):
    class Meta:
        model = Subcategory_1
        fields = '__all__'


# for making subcategories
class add_Subcategory_2(ModelForm):
    class Meta:
        model = Subcategory_2
        fields = '__all__'


# Add product- category, brand, stock status
class add_product_alements(ModelForm):
    class Meta:
        model = Products
        fields = ['Discount_Percentage', 'Brand', 'Vendors', 'Stock_status', 'Product_Description', 'Long_Product_Description', 'KG_or_Liter', 'flash_sell']





class edit_product_field(ModelForm):
    class Meta:
        model = Products
        fields = ['Discount_Percentage', 'Brand', 'Vendors', 'Stock_status', 'make_star', 'Product_Description', 'Long_Product_Description', 'KG_or_Liter', 'flash_sell']
        
        
class vendor_edit_product_field(ModelForm):
    class Meta:
        model = Products
        fields = ['Brand', 'Category', 'Subcategory_1', 'Subcategory_2', 'Stock_status', 'Product_Description', 'Long_Product_Description', 'KG_or_Liter']
        

        
class s_vendor_edit_product_field(ModelForm):
    class Meta:
        model = Products
        fields = ['Brand', 'Stock_status', 'Product_Description', 'Long_Product_Description', 'KG_or_Liter']


        
class form_Flash_Sell_add(ModelForm):
    class Meta:
        model = Flash_Sell
        fields = '__all__'
