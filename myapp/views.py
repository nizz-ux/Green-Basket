from django.shortcuts import render , redirect
from django.contrib import messages
from .models import *
import json
import requests
import razorpay
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.db.models import Sum

from django.http import JsonResponse

# Create your views here.
def index(request):
    catedetails = category.objects.all()
    context = {
        'catedetails':catedetails,
    }
    return render(request,"index.html", context)

def login_view(request):
    return render(request,"login.html")

def register_view(request):
    return render(request,"register.html")

def project(request):
    return render(request,"project.html")
def project_detail(request):
    return render(request,"project-details.html")
def team(request):
    return render(request,"team.html")
def team_details(request):
    return render(request,"team-details.html")

def reviews(request):
    return render(request,"reviews.html")
def packages(request):
    return render(request,"packages.html")
def fag(request):
    return render(request,"fag.html")

def error(request):
    return render(request,"404.html")
def services(request):
    return render(request, "services-02.html")
def service_fresh(request):
    return render(request,"service-d-fresh.html")
def service_farming(request):
    return render(request,"service-d-farming.html")

def service_organic(request):
    return render(request,"service-d-organic.html")
def service_agriculture(request):
    return render(request,"service-d-agriculture.html")
def service_growth(request):
    return render(request,"service-d-growth.html")

def service_plants(request):
    return render(request,"service-d-plants.html")



def checkout(request):
    return render(request,"checkout.html")
def grid(request):
    return render(request,"blog-grid-right.html")
def grid_detail(request):
    return render(request,"blog-details-right.html")

def blog(request):
    return render(request,"blog-carousel.html")
def blog_list(request):
    return render(request,"blog-list-right.html")


def register_fetch_data(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        select_role = request.POST.get("select_role")
        save_data_check = request.POST.get("save_data_check")


        if register.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("/register/")


        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("/register/")

        insert = register(
            first_name =first_name,
            last_name=last_name,
            email =email,
            password =password,
            confirm_password = confirm_password,
            select_role =select_role,
            save_data_check =save_data_check

        )
        insert.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("/login/")


    return render(request ,"register.html")



def login_fetch_data(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:

      data = register.objects.get(email= email,password = password)
      print(data)

      request.session["log_id"] = data.id
      request.session["log_name"] = data.first_name
      request.session["log_email"] = data.email
      request.session["log_role"] = data.select_role

      usersessionid = request.session["log_id"]
      print("Session id:", usersessionid)
      print("success")

    except:
      data = None

    if data is not None:
         # print("Testing data")
         messages.success(request,"successfully login",)
         return redirect("/")

    else:
         # print("data enter invalid")
         messages.error(request,"Invalid email or password")

    return render(request,"login.html")


def logout(request):
    try:
        del request.session["log_id"]
        del request.session["log_name"]
        del request.session["log_email"]
        del request.session["log_password"]
        del request.session["log_role"]
    except:
        pass
    return render(request,"index.html")

def contact(request):
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Subject = request.POST.get('subject')
        Message = request.POST.get('message')

        if Contact_detail.objects.filter(email=Email).exists():
            messages.error(request, 'You have already filled out contact details.')
            return redirect('contact')
        else:
            contactdata = Contact_detail(name=Name, email=Email, subject=Subject, message=Message)
            contactdata.save()
            messages.success(request, 'Your contact details have been saved.')
            return redirect('index')

    return render(request,'contact.html')


def product_view(request):
    product_data = product.objects.all()
    catename = category.objects.all()
    context = {
        "product_data" : product_data,
         "catename": catename
    }

    return render(request,"products.html" , context)
def search_products(request):
    all_product = product.objects.exclude(prod_name =None, prod_cate=None)
    query = request.GET.get('q', '').strip()
    products_by_name = all_product.filter(prod_name__icontains=query)
    products_by_category = all_product.filter(prod_cate__category_name__icontains=query)
    products = products_by_name | products_by_category


    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price.isdigit():
        products = products.filter(prod_price__gte=int(min_price))

    if max_price and max_price.isdigit():
        products = products.filter(prod_price__lte=int(max_price))

    return render(request, 'products.html', {
        'product_data': products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    })

def about_view(request):
    return render(request,"about.html")
# def cart_view(request):
#     return render(request,"cart.html")

def add_product(request):
   alldata = category.objects.all()
   context = {
        "category_data": alldata,
   }
   if request.method == "POST":
      p_name = request.POST.get("prod_name")
      p_cate_id = request.POST.get("prod_cate")
      p_image = request.FILES.get("prod_image")
      p_price = request.POST.get("prod_price")
      p_desc = request.POST.get("prod_desc")
      p_state = request.POST.get("prod_state")

      print(p_name, p_cate_id, p_image, p_desc, p_state, p_price)
      sell_id = request.session['log_id']
      insert = product(prod_name = p_name ,
                     prod_cate = category(id= p_cate_id),
                     prod_image=p_image,
                     prod_price= p_price,
                     prod_desc= p_desc,
                     prod_state= p_state,
                     sell_id =register(id=sell_id)
                     )
      insert.save()
      messages.success(request,"Product added successfully!!")
      return redirect("/product_view/")

   else:
       messages.error(request, "please enter valid data!")

   return render(request,"addproduct.html", context)


def product_details(request,pid):
  print(id)
  if id is None:
        return redirect("/product_view/")
  try:
    fetchdata = product.objects.get(id=pid)
  except product.DoesNotExist:
     return  redirect("/error/")
  context = {
         "data" : fetchdata
    }

  return render(request ,"product-details.html", context)

def categorywayproduct(request,id):
    print(id)
    catename = category.objects.all()
    product_data = product.objects.filter(prod_cate = id)
    context = {
        "catename": catename,
        "product_data" : product_data
    }
    return render(request,"category_product.html", context)

def manageproduct(request):
    log_sell_id = request.session["log_id"]
    fetch_role = product.objects.filter(sell_id=  log_sell_id)

    total_payment = fetch_role.aggregate(Sum('prod_price'))['prod_price__sum'] or 0
    context = {
        "data": fetch_role,
        "total_products": fetch_role.count(),
        "total_payment": total_payment
    }
    return render(request , "manageproduct.html", context)

def editproduct(request,id):
    print(id)
    fetchdata=product.objects.get(id=id)
    allcatdata=category.objects.all()

    context={
        "data":fetchdata,
        "catdata":allcatdata
    }
    return render(request,"editproduct.html",context)


def updateproductdata(request):
    if request.method == "POST":
        pid = request.POST.get("pid")
        pname = request.POST.get("pname")
        pcat = request.POST.get("pcat")
        pprice = request.POST.get("pprice")
        pdesc = request.POST.get("pdesc")
        farmerid = request.session["log_id"]

        fetchdata = product.objects.get(id=pid)

        # Update fields
        fetchdata.prod_name = pname
        fetchdata.prod_cate = category.objects.get(id=pcat)  # Ensure category is fetched correctly
        fetchdata.prod_price = pprice
        fetchdata.prod_desc = pdesc
        fetchdata.farmerid = register.objects.get(id=farmerid)

        # Handle image update (keep old image if not updated)
        if "pimage" in request.FILES:
            fetchdata.image = request.FILES["pimage"]

        fetchdata.save()

        messages.success(request, "Data Updated Successfully")
        return redirect("/manageproduct")

    messages.error(request, "Invalid Request")
    return redirect("/editproduct")

def deleteproduct(request,id):
    product.objects.get(id=id).delete()
    messages.success(request,"Item Deleted")
    return redirect("/manageproduct")



from django.shortcuts import redirect
from django.contrib import messages

def insertintocart(request):
    if request.method == "POST":
        userid = request.session.get("log_id")  # Use .get() to avoid KeyError
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")

        if not all([userid, product_id, quantity, price]):  # Ensure all values exist
            messages.error(request, "Invalid data submitted.")
            return redirect("/")

        try:
            total_amount = int(quantity) * float(price)
            insert = cart(
                userid=register(id=userid),
                product_id=product(id=product_id),
                quantity=quantity,
                total_amount=total_amount,
                order_id=0,
                order_status=1
            )
            insert.save()
            messages.success(request, "Successfully added to cart.")
            return redirect("/cart_view/")
        except Exception as e:
            messages.error(request, f"Error adding to cart: {str(e)}")
            return redirect("/")
    else:
        messages.error(request, "Please enter valid data!")
        return redirect("/")


def add_wishlist(request,id):
     userid = request.session["log_id"]
     insert = Wishlist(
         userid=register(id=userid),
         product_id=product(id=id)
     )
     insert.save()
     messages.success(request, "successfull add into Wishlist")
     print("success")
     return redirect("/wish_list")

def wish_list(request):
    userid = request.session.get("log_id")
    wishlist_items =Wishlist.objects.filter(userid=userid)
    context = {
        "wishlist_items": wishlist_items,
    }
    return render(request,"wishlist.html", context)

def cart_view(request):
    userid = request.session["log_id"]
    card_data = cart.objects.filter(userid = userid ,order_status =1)
    total =sum(i.total_amount for i in card_data)
    gst = total * 0.18  # 18% GST
    shipping_charge = 50.00 if total > 0 else 0.00
    discount = 0
    coupon_code = request.POST.get("coupon_code")

    if coupon_code:
        try:
            off = coupon.objects.get(code=coupon_code, is_active=True)
            discount = (total * off.discount) / 100
        except coupon.DoesNotExist:
            discount = 0
    final_total = total + gst + shipping_charge - discount

    context = {
        "card_data" : card_data,
        "total":total,
        "gst": gst,
        "shipping_charge": shipping_charge,
        "discount": discount,
        "applied_coupon": coupon_code if discount > 0 else None,
        "final_total": final_total,
    }
    return render(request,"cart.html" , context)


def realtime_news(request):
    api_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",
        "category": "business",
        "apiKey": "0a15138fb9e34a93aa0ba589bf79b7b8"
    }

    response = requests.get(api_url, params=params)
    data = response.json() if response.status_code == 200 else {}
    articles = data.get('articles', [])

    return render(request, 'api_news.html', {'articles': articles} )


def increase(request, id):
     fetchdata = cart.objects.get(id = id)
     fetchdata.quantity += 1
     fetchdata.total_amount += fetchdata.product_id.prod_price
     fetchdata.save()

     return redirect("/cart_view/")

def descrease(request , id):
    fetchdata = cart.objects.get(id = id)
    if fetchdata.quantity == 1:
        fetchdata.delete()
    else:
        fetchdata.quantity -= 1
        fetchdata.total_amount -= fetchdata.product_id.prod_price
        fetchdata.save()

    return redirect("/cart_view/")

def remove_wishlist(request , id):
    fetchdata = Wishlist.objects.get(id = id)
    if fetchdata.quantity == 1:
        fetchdata.delete()
    else:
        fetchdata.quantity -= 1
        fetchdata.total_amount -= fetchdata.product_id.prod_price
        fetchdata.save()

    return redirect("/wish_list/")

def delete_product(request , id):

    fetchdata = cart.objects.get(id = id).delete()
    return redirect("/cart_view/")


def placeorder(request):
   userid = request.session["log_id"]
   finaltotal = request.POST.get("total")
   phone = request.POST.get("phone")
   address = request.POST.get("address")
   paymode = request.POST.get("payment")

   if paymode=="Cash on Delivery":
        storedata = ordermodel(
            userid=register(id=userid),
            finaltotal=finaltotal,
            phone=phone,
            address=address,
            paymode=paymode,
            status=True

        )
        storedata.save()
        lastid = storedata.id

        fetchdata = cart.objects.filter(userid=userid, order_status=1)
        for i in fetchdata:
            i.order_status = 0
            i.order_id = lastid
            i.save()

        messages.success(request, "Order Placed Successfully")
   else:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order_amount =int(float(finaltotal)*100)
        razorpay_order = client.order.create(
            {
                "amount":order_amount,
                "currency":"INR",
                "receipt":f"order_rcptid_{userid}",
                "payment_capture":"1",
            }

        )
        storedata = ordermodel(
            userid=register(id=userid),
            finaltotal=finaltotal,
            phone=phone,
            address=address,
            paymode="Online",
            status=True,
            razorpay_order_id=razorpay_order['id'],
        )
        storedata.save()

        lastid = storedata.id
        cart_items = cart.objects.filter(userid=userid, order_status=1)
        for item in cart_items:
            item.order_status = 0
            item.order_id = lastid
            item.save()

        return render(request, "payment.html", {
            "razorpay_order_id": razorpay_order['id'],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR",
        })

   return redirect("/")

def payment_success(request):
  return render(request, "payment.html")

def payment_manage(request):
    user_id = request.session['log_id']
    farmer = register.objects.get(id=user_id)

    farmer_products = product.objects.filter(sell_id=farmer)
    related_carts = cart.objects.filter(product_id__in=farmer_products)
    order_ids = related_carts.values_list('order_id', flat=True).distinct()

    delivered_orders = ordermodel.objects.filter(status=True, id__in=order_ids)

    total_orders =   delivered_orders.count()
    total_payment = delivered_orders.aggregate(Sum('finaltotal'))['finaltotal__sum'] or 0


    return render(request, "payment_manage.html", {

        "delivered_orders": delivered_orders,
        "total_orders": total_orders,
        "total_payment": total_payment,

    })
def order_manage(request):
    return render(request,"order.html")

def orders(request):
    customerid = request.session["log_id"]
    fetchdata = ordermodel.objects.filter(userid=customerid)
    context = {
        "data": fetchdata,
    }
    return render(request,"order_history.html",context)

def yourorderdetails(request,id):
    user_id = request.session['log_id']
    order = ordermodel.objects.get(id=id, userid=user_id)
    orderid = order.id
    fetchdata = cart.objects.filter(userid=user_id, order_id=orderid, order_status=0)
    context = {
        "mydata": fetchdata,
    }
    return render(request,"yourorderdetails.html",context)

def cancelorder(request,id):
    fetchdata = ordermodel.objects.get(id=id)
    fetchdata.status = False
    fetchdata.save()
    messages.success(request,"your order is cancelled")
    return redirect("/orders/")

def seller_orders(request):
    uid = request.session['log_id']
    sellers_products = product.objects.filter(sell_id=register(id=uid))
    getdetails = cart.objects.filter(product_id__in=sellers_products, order_status=0)
    total_amount = getdetails.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_count = getdetails.filter(order_status=0).count()
    delivered_count = getdetails.filter(order_status=1).count()
    context = {
        "data": getdetails,
        "grand_total": total_amount,
        "pending_count": pending_count,
        "delivered_count": delivered_count,
    }
    return render(request,"seller_order.html",context)

def productfeedback(request, order_id):
    context = {"order_id" : order_id}
    return render(request, 'feedback.html', context)

def storefeedback(request):
    user_id = request.session.get('log_id')
    if request.method == 'POST':
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')
        order_id = request.POST.get('order_id')

        if Feedback.objects.filter(order_id=order_id).exists():
            messages.error(request, 'you have already filled feedback.')
            return redirect('/storefeedback/')
        else:

            feedback = Feedback.objects.create(
                user=register(id=user_id),
                order_id=ordermodel(id=order_id),
                ratings=ratings,
                comment=feedback_message,
            )

        messages.success(request, "feedback is submitted")
        return redirect(orders)
    return render(request, 'index.html' )

def find_products(request):
    context = {}
    catedetails = category.objects.all()
    # Get selected property type if any
    category_type = request.GET.get('category_type')
    product_data = product.objects.all()
    if category_type:
        product_data = product_data.filter(prod_cate__id=category_type)

    context['product_data'] = product_data
    context["catedetails"] = catedetails
    return render(request, 'products.html', context)


def edit_profile(request, id):
    print(id)
    fetchdata = register.objects.get(id=id)
    context = {
        "data": fetchdata,
    }
    return render(request,"edit_profile.html", context)

def insert_profile(request):
    userid = request.session.get("log_id")
    user_detail = register.objects.filter(id=userid).first()
    context = {
        "user_detail": user_detail,
    }


    return render(request,'profile.html', context)


def update_profile(request):
    if request.method == "POST":
        id = request.POST.get("userid")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("/insert_profile/")

        try:
            fetchdata = register.objects.get(id=id)
            fetchdata.first_name = first_name
            fetchdata.last_name = last_name
            fetchdata.email = email
            fetchdata.password = password
            fetchdata.confirm_password = confirm_password
            fetchdata.save()
            messages.success(request, "Data Updated Successfully")
        except register.DoesNotExist:
            messages.error(request, "User not found.")

        return redirect("/insert_profile/")

    messages.error(request, "Invalid Request")
    return redirect("/insert_profile/")







