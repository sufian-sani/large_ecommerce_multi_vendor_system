from django.db import models
import uuid
# Create your models here.
# from main.models import customer_review


from datetime import datetime
from vendor_dashboard_app.models import vendor_registration_table
from ckeditor.fields import RichTextField

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   old_customer_uniqe_id = models.CharField(max_length=255, null=True, blank=True)


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Category'
    Category_Slug = models.CharField(max_length=255, blank=True, null=True)
    Category_Name = models.CharField(max_length=255)
    Category_title = models.CharField(max_length=255, blank=True, null=True)
    Category_discription = models.TextField(blank=True, null=True)
    total_quantity_of_sell = models.IntegerField(blank=True, null=True)
    total_money_of_sell = models.IntegerField(blank=True, null=True)
    total_quantity_of_sell_reguler = models.IntegerField(blank=True, null=True)
    total_money_of_sell_reguler = models.IntegerField(blank=True, null=True)
    Category_benner = models.FileField(upload_to='Category_benner', blank=True, null=True,
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])],
                                    help_text="Choose Only .jpg, .jpeg, .png and files PLease..")

    def __str__(self):
        return str(self.id) + ' - ' + self.Category_Name
    
        
        
    def filter_the_subcat1_by_mainCat(self):
        subcat1s = Subcategory_1.objects.filter(Category=self)
        
        return subcat1s
        
    def filter_product_by_cat(self):
        cat_prod = Products.objects.filter(Category=self)[:4]
        return cat_prod
        
    def product_qty_cat(self):
        return Products.objects.filter(Category=self).count()
        
        
    
    def subcat1_by_cat(self):
        return Subcategory_1.objects.filter(Category=self)
    
        

class Subcategory_1(models.Model):
    class Meta:
        verbose_name_plural = 'Subcategory_1'
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Subcategory_1 = models.CharField(max_length=255)
    add_home = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + ' - ' + self.Category.Category_Name +", "+ self.Subcategory_1
        
    def filter_cam_subcat_2(self):
        return Subcategory_2.objects.filter(Subcategory_1=self)

    def home_side_featured_products(self):
        return Products.objects.filter(Subcategory_1=self).filter(make_star=True)[:5]
        
    
    
    
        


class Subcategory_2(models.Model):
    class Meta:
        verbose_name_plural = 'Subcategory_2'

    Subcategory_1 = models.ForeignKey(Subcategory_1, on_delete=models.CASCADE)
    Subcategory_2 = models.CharField(max_length=255)

    def __str__(self):
        return self.Subcategory_1.Category.Category_Name +", "+ self.Subcategory_1.Subcategory_1+", "+ self.Subcategory_2
        
    
        
        
    


class Brand(models.Model):
    class Meta:
        verbose_name_plural = 'Brand'
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Brand_Name = models.CharField(max_length=255)
    Description = RichTextField(blank=True, null=True)
    Brand_logo = models.ImageField(upload_to='Brand_logo/', blank=True, null=True)
    Featured_Brand = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Brand_Name

    def filter_brand_prod_cam(self):
        return Products.objects.filter(Brand=self).filter(Subcategory_2__isnull=False)
        
    def filter_brand_prod_cam_sub2less(self):
        return Products.objects.filter(Brand=self).filter(Subcategory_1__isnull=False).filter(Subcategory_2__isnull=True)
    
    def filter_brand_prod_cam_sub2with(self):
        return Products.objects.filter(Brand=self).filter(Subcategory_2__isnull=False)
        
        
    def subless_cat_brand(self):
        return Products.objects.filter(Brand=self).filter(Subcategory_1__isnull=True).filter(Subcategory_2__isnull=True)
        


class Attribute(models.Model):
    Attribute_name = models.CharField(max_length=100)
    Attribute_slag = models.CharField(max_length=100, blank=True, null=True, unique=True)
    Attribute_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Attribute_name



class Attribute_value(models.Model):
    Attribute_name = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    Attribute_value_slag = models.CharField(max_length=100, blank=True, null=True, unique=True)
    Attribute_value_description = models.TextField(blank=True, null=True)
    Attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return self.Attribute_value





class Products(models.Model):
    class Meta:
        verbose_name_plural = 'Products'

    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Product_slug = models.CharField(max_length=255, blank=True, null=True, unique=True)
    Product_Name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=255, blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    Subcategory_1 = models.ManyToManyField(Subcategory_1, blank=True, null=True)
    Subcategory_2 = models.ManyToManyField(Subcategory_2, blank=True, null=True)
    TYPE_OF_PRODUCTS = models.CharField(max_length=20, blank=True, null=True)
    Cost_Price = models.IntegerField(blank=True, null=True)
    MRP_Price = models.IntegerField(blank=True, null=True)
    Discount_Price = models.IntegerField(blank=True, null=True)
    Discount_Percentage = models.IntegerField(blank=True, null=True)
    KG_or_Liter = models.IntegerField(blank=True, null=True)
    Product_Description = RichTextField(blank=True, null=True)
    Long_Product_Description = RichTextField(blank=True, null=True)
    Meta_Title = models.CharField(max_length=255, blank=True, null=True)
    Meta_Keyword = models.CharField(max_length=255, blank=True, null=True)
    Product_Image = models.TextField(max_length=255, blank=True, null=True)
    Product_Image2 = models.TextField(max_length=255, blank=True, null=True)
    Product_Image3 = models.TextField(max_length=255, blank=True, null=True)
    Product_Image4 = models.TextField(max_length=255, blank=True, null=True)
    status = (
        ("In stock", "In stock"),
        ("Out stock", "Out stock"),
        ("On backorder", "On backorder"),
    )
    Stock_status = models.CharField(max_length=20, choices=status, default="In stock")
    Product_stock_Quantity = models.CharField(max_length=255, blank=True, null=True)
    Vendors= models.ForeignKey(vendor_registration_table, on_delete=models.CASCADE, blank=True, null=True)
    Brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    Time = models.DateTimeField(default=datetime.now(), blank=True)
    make_star = models.BooleanField(default=False)
    flash_sell = models.BooleanField(default=False)
    flash_sell_start_time = models.DateField(default=datetime.now(), blank=True)
    flash_sell_end_time = models.DateField(default=datetime.now(), blank=True)
    product_wishlist = models.ManyToManyField(User, related_name='product_wishlist', default=None, blank=True, null=True)
    Review_Quantity = models.IntegerField(blank=True, null=True)
    total_quantity_of_sell_product = models.IntegerField(blank=True, null=True)
    total_money_of_sell_product = models.IntegerField(blank=True, null=True)
    total_quantity_of_sell_reguler_product = models.IntegerField(blank=True, null=True)
    total_money_of_sell_reguler_product = models.IntegerField(blank=True, null=True)
    

    def __str__(self):
        return self.Product_Name
        
    # def review_qty(self):
    #     return customer_review.objects.filter(Product=self).count()
    
    
    def only_campaign_active_product(self):
        return campaign_product_table.objects.filter(product=self).filter(add_item_campaign=True)
        
    def only_campaign_active_product222(self):
        chck_prd = campaign_product_table.objects.filter(product=self).filter(add_item_campaign=True)
        if chck_prd:
            return True
        else:
            return False
            
    def get_campaign_product(self):
        return campaign_product_table.objects.get(product=self).filter(add_item_campaign=True)

    
    def vendr_prod_qty(self):
        get_vendor = vendor_registration_table.objects.get(id=self.Vendors.id)
        return Products.objects.filter(Vendors=get_vendor).count()
        
    def first_attr_low_cost_prod(self):
        var_lp = attribute_connect_with_product.objects.filter(connect_with_product=self).filter(MRP_Price__isnull=False).order_by('MRP_Price')[:1]
        
        return var_lp
        
        
    def count_rattings(self):
        get_review_total = customer_review.objects.filter(Product=self)
        get_review = get_review_total.count()
    
        Total_sum_of_reviews_quentity = 0
        for i in get_review_total:
            Total_sum_of_reviews_quentity = Total_sum_of_reviews_quentity + i.Ratting_qty
    
        if Total_sum_of_reviews_quentity == 0:
            avarage_Total_sum_of_reviews_quentity = 0
        else:
            avarage_Total_sum_of_reviews_quentity_1 = Total_sum_of_reviews_quentity / get_review
            avarage_Total_sum_of_reviews_quentity = format(avarage_Total_sum_of_reviews_quentity_1, ".1f")
    
    
    
        int_avarage_Total_sum_of_reviews_quentity = float(avarage_Total_sum_of_reviews_quentity)
        
        
        ratting_qty=0
        
    
        if int_avarage_Total_sum_of_reviews_quentity == 0:
            ratting_qty = 0
        elif int_avarage_Total_sum_of_reviews_quentity > 0 and int_avarage_Total_sum_of_reviews_quentity < 1:
            ratting_qty = 0.5
        elif int_avarage_Total_sum_of_reviews_quentity ==1:
            ratting_qty = 1
        elif int_avarage_Total_sum_of_reviews_quentity > 1 and int_avarage_Total_sum_of_reviews_quentity < 2:
            ratting_qty = 1.5
        elif int_avarage_Total_sum_of_reviews_quentity == 2:
            ratting_qty = 2
        elif int_avarage_Total_sum_of_reviews_quentity > 2 and int_avarage_Total_sum_of_reviews_quentity <3:
            ratting_qty = 2.5
        elif int_avarage_Total_sum_of_reviews_quentity == 3:
            ratting_qty = 3
        elif int_avarage_Total_sum_of_reviews_quentity > 3 and int_avarage_Total_sum_of_reviews_quentity <4:
            ratting_qty = 3.5
        elif int_avarage_Total_sum_of_reviews_quentity == 4:
            ratting_qty = 4
        elif int_avarage_Total_sum_of_reviews_quentity > 4 and int_avarage_Total_sum_of_reviews_quentity < 5:
            ratting_qty = 4.5
        elif int_avarage_Total_sum_of_reviews_quentity == 5:
            ratting_qty = 5
    
        return ratting_qty
        
        
    def count_rattings_qty(self):
        get_review_total = customer_review.objects.filter(Product=self)
        get_review = get_review_total.count()
    
        return get_review






# rattings for customer review
class customer_review(models.Model):
    class Meta:
        verbose_name_plural = 'Customer Review'
        
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.ForeignKey(Products, on_delete=models.CASCADE)
    Ratting_qty = models.IntegerField()
    Review_Text = models.TextField(null=True, blank=True)
    Review_Time = models.DateTimeField(default=datetime.now(), blank=True)


class attribute_connect_with_product(models.Model):
    connect_with_product = models.ForeignKey(Products, on_delete=models.CASCADE)

    Size = models.CharField(max_length=90, blank=True, null=True)
    Color = models.CharField(max_length=90, blank=True, null=True)
    Flavor = models.CharField(max_length=90, blank=True, null=True)
    Variation = models.CharField(max_length=90, blank=True, null=True)
    Weight = models.CharField(max_length=90, blank=True, null=True)
    Volume = models.CharField(max_length=90, blank=True, null=True)
    Quantity = models.CharField(max_length=90, blank=True, null=True)
    Values = models.CharField(max_length=90, blank=True, null=True)
    Material_Type = models.CharField(max_length=90, blank=True, null=True)
    Product_Type = models.CharField(max_length=90, blank=True, null=True)
    Verification = models.CharField(max_length=90, blank=True, null=True)
    Quality = models.CharField(max_length=90, blank=True, null=True)
    Marketing_Claims = models.CharField(max_length=90, blank=True, null=True)
    Design = models.CharField(max_length=90, blank=True, null=True)
    Smell = models.CharField(max_length=90, blank=True, null=True)
    Reliability = models.CharField(max_length=90, blank=True, null=True)
    Content = models.CharField(max_length=90, blank=True, null=True)
    Safety = models.CharField(max_length=90, blank=True, null=True)
    Package = models.CharField(max_length=90, blank=True, null=True)
    Model = models.CharField(max_length=90, blank=True, null=True)
    Taste = models.CharField(max_length=90, blank=True, null=True)
    Feel = models.CharField(max_length=90, blank=True, null=True)
    Defferent_Type = models.CharField(max_length=90, blank=True, null=True)
    attribute_image_of_product = models.ImageField(blank=True, null=True)
    Cost_Price = models.IntegerField(blank=True, null=True)
    MRP_Price = models.IntegerField(blank=True, null=True)
    Discount_Price = models.IntegerField(blank=True, null=True)
    Attribute_Quantity = models.IntegerField(blank=True, null=True)
    status = (
        ("In stock", "In stock"),
        ("Out stock", "Out stock"),
        ("On backorder", "On backorder"),
    )
    Stock_status = models.CharField(max_length=20, choices=status, default="In stock")

    def __str__(self):
        return self.connect_with_product.Product_Name







  

class Flash_Sell(models.Model):
    class Meta:
        verbose_name_plural = 'Flash Sell'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=255)
    flash_sell_start_time = models.DateField(default=datetime.now(), blank=True)
    flash_sell_end_time = models.DateField(default=datetime.now(), blank=True)
    
    

class Staff_Access(models.Model):
    class Meta:
        verbose_name_plural = 'Staff Access'
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    role = (
        ("Admin", "Admin"),
        ("Shop Manager", "Shop Manager"),
        ("Customer Support", "Customer Support"),
        ("Upload Team", "Upload Team"),
    )
    Staff_Role = models.CharField(max_length=20, choices=role, default="Admin")
    First_Register_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Last_login_Time = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.Username
        
        
        
        
        

class campaign_table(models.Model):
    class Meta:
        verbose_name_plural = 'campaign_table'
    campaign_slug = models.CharField(max_length=255)
    campaign_name = models.CharField(max_length=255)
    start_time = models.DateField(default=datetime.now(), blank=True, null=True)
    end_time = models.DateField(default=datetime.now(), blank=True, null=True)
    campaign_logo = models.ImageField(upload_to='campaign_logo/', blank=True, null=True)
    campaign_benner = models.ImageField(upload_to='campaign_benner/', blank=True, null=True)
    finish_campaign = models.BooleanField(default=False)
    free_delivery = models.BooleanField(default=False)
    
    def __str__(self):
        return self.campaign_name
        
    def campaign_home_featured_product(self):
        return campaign_product_table.objects.filter(campaign=self, make_index_star=True, add_item_campaign=True)[:5]
 
        
class campaign_categories_percentage(models.Model):
    class Meta:
        verbose_name_plural = 'campaign_categories_percentage'
    campaign = models.ForeignKey(campaign_table, on_delete = models.CASCADE)
    Category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    
    total_quantity_of_sell_cat_campaign = models.IntegerField(blank=True, null=True)
    total_money_of_sell_cat_campaign = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.campaign.campaign_name+" - "+self.Category.Category_Name+ " - "+str(self.percentage)+"%"
        
    def star_products(self):
        return campaign_product_table.objects.filter(make_campaign_star=True, add_item_campaign=True, category_percentage=self)
        
    def calculate_max_percent(self):
        cat_project = campaign_product_table.objects.filter(category_percentage=self).filter(add_item_campaign=True)
        
        lst = []
        for i in cat_project:
            lst.append(i.campaign_percentage)
            
        max_percentage_var = max(lst, default=0)
        return max_percentage_var

    def product_qty_cam_cat(self):
        return campaign_product_table.objects.filter(category_percentage=self).count()


        
class campaign_product_table(models.Model):
    class Meta:
        verbose_name_plural = 'Campaign Product Table'
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(campaign_table, on_delete = models.CASCADE, blank=True, null=True , default='1')
    category_percentage = models.ForeignKey(campaign_categories_percentage, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    make_campaign_star = models.BooleanField(default=False)
    make_index_star = models.BooleanField(default=False)
    add_item_campaign = models.BooleanField(default=False)
    campaign_percentage = models.IntegerField(blank=True, null=True)
    campaign_price = models.IntegerField(blank=True, null=True)
    wishlist = models.ManyToManyField(User, related_name='wishlist', default=None, blank=True, null=True)
    total_quantity_of_sell_campaign_product = models.IntegerField(blank=True, null=True)
    total_money_of_sell_campaign_product = models.IntegerField(blank=True, null=True)
    
    
    def first_attr_low_cost_campaign_prod(self):
        var_lp = campaign_product_attribute.objects.filter(campaign_product=self).filter(MRP_Price__isnull=False).order_by('MRP_Price')[:1]
        return var_lp
        
    
        
class campaign_product_attribute(models.Model):
    class Meta:
        verbose_name_plural = 'Campaign Product Attribute'
    campaign_product = models.ForeignKey(campaign_product_table, on_delete = models.CASCADE, blank=True, null=True)
    attribute = models.ForeignKey(attribute_connect_with_product, on_delete = models.CASCADE, blank=True, null=True)
    Cost_Price = models.IntegerField(blank=True, null=True)
    MRP_Price = models.IntegerField(blank=True, null=True)
    Discount_Price = models.IntegerField(blank=True, null=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    