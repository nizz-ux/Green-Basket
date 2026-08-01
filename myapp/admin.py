from django.contrib import admin
from .models import *
# Register your models here.

class show_register(admin.ModelAdmin):
    list_display = ("first_name", "last_name","email","password","confirm_password","select_role", "save_data_check")

admin.site.register(register , show_register)

class show_category(admin.ModelAdmin):
    list_display = ("id" , "category_name")

admin.site.register(category , show_category)

class show_product(admin.ModelAdmin):
    list_display = ('prod_name','prod_cate','product_photo','prod_price','prod_desc','prod_state', 'sell_id')


admin.site.register(product , show_product)

class show_order(admin.ModelAdmin):
    list_display = ('userid','finaltotal','phone','address','paymode','timestamp', 'status','razorpay_order_id')


admin.site.register(ordermodel , show_order)

class show_coupon(admin.ModelAdmin):

    list_display = ('code' ,'discount', 'is_active')

admin.site.register(coupon,show_coupon)

class show_wishlist(admin.ModelAdmin):
    list_display = ('userid', 'product_id', 'added_on')

admin.site.register(Wishlist,show_wishlist)

class show_contact_details(admin.ModelAdmin):
    list_display = ('name','email','subject','message','timestamp')

admin.site.register(Contact_detail, show_contact_details)

class show_feedback(admin.ModelAdmin):
  list_display = ('user','order_id','ratings','comment','timestamp')

admin.site.register(Feedback,show_feedback)

