from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.

class register(models.Model):
    first_name = models.CharField(max_length=20)
    last_name =  models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20)
    select_role = models.CharField(max_length=20)
    save_data_check = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name


class category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
     return self.category_name

class product(models.Model):
    prod_name = models.CharField(max_length=20)
    prod_cate = models.ForeignKey(category, on_delete=models.CASCADE)
    prod_image = models.ImageField(upload_to='photos')
    prod_price = models.IntegerField()
    prod_desc = models.TextField()
    prod_state = models.CharField(max_length=20)
    sell_id = models.ForeignKey(register, on_delete=models.CASCADE)

    def __str__(self):
        return self.prod_name

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.prod_image.url))

    product_photo.allow_tags = True

class cart(models.Model):
    userid = models.ForeignKey(register,on_delete=models.CASCADE)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.FloatField()
    order_id = models.IntegerField()
    order_status = models.IntegerField()


class ordermodel(models.Model):
   userid = models.ForeignKey(register, on_delete=models.CASCADE)
   finaltotal = models.FloatField()
   phone = models.BigIntegerField()
   address = models.TextField()
   paymode = models.CharField(max_length=40)
   timestamp = models.DateTimeField(auto_now_add=True)
   status = models.BooleanField(default=False)
   razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)


class coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Wishlist(models.Model):
    userid = models.ForeignKey(register, on_delete=models.CASCADE)  # Linking to users
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)  # Linking to products
    quantity = models.IntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.added_on

class Contact_detail(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=30)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user = models.ForeignKey('register', on_delete=models.CASCADE, default="")
    order_id = models.ForeignKey('ordermodel', on_delete=models.CASCADE, null=True, blank=True, default='')
    ratings = models.IntegerField()
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.user.first_name}"