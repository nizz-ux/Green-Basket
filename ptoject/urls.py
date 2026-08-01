"""
URL configuration for ptoject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("contact/", views.contact, name="contact"),
    path("register_fetch_data/", views.register_fetch_data, name="register_fetch_data"),
    path("login_fetch_data/", views.login_fetch_data,name="login_fetch_data"),
    path("logout/", views.logout, name="logout"),
    path("product_view/", views.product_view ,  name="product_view"),
    path("about_view/", views.about_view, name="about_view"),
    path("cart_view/", views.cart_view, name="cart_view"),
    path("add_product/", views.add_product, name="add_product"),
    path("product_details/<int:pid>/",views.product_details),
    path("categorywayproduct/<int:id>/", views.categorywayproduct),
    path("manageproduct/", views.manageproduct),
    path("editproduct/<int:id>/", views.editproduct),
    path("updateproductdata", views.updateproductdata),
    path("deleteproduct/<int:id>/", views.deleteproduct),
    path("seller_orders/", views.seller_orders),
    path("insertintocart/" ,views.insertintocart),
    path("project/",views.project),
    path("project_detail/", views.project_detail),
    path("team/", views.team),
    path("team_details/", views.team_details),
    path("reviews/", views.reviews),
    path("packages/", views.packages),
    path("fag/", views.fag),
    path("error/", views.error),
    path("services/", views.services),
    path("service_fresh/",views. service_fresh),
    path("service_farming/", views.service_farming),
    path("service_organic/", views.service_organic),
    path("service_agriculture/", views.service_agriculture),
    path("service_growth/", views.service_growth),
    path("service_plants/", views. service_plants),
    path("checkout/",views.checkout),
    path("grid/", views.grid),
    path("grid_detail/", views.grid_detail),
    path("blog/", views.blog),
    path("blog_list/", views.blog_list),
    path( "realtime_news/", views.realtime_news),
    path("increase/<int:id>/", views.increase),
    path("descrease/<int:id>/", views.descrease),
    path("delete_product/<int:id>/", views.delete_product),
    path('search/', views.search_products, name='search_products'),
    path("placeorder/", views.placeorder),
    path('payment-success/', views.payment_success),
    path('payment_manage/', views.payment_manage),
    path('order_manage/', views.order_manage),
    path('wish_list/', views.wish_list),
    path('remove_wishlist/<int:id>/', views.remove_wishlist),
    path('add_wishlist/<int:id>', views.add_wishlist),
    path('orders/', views.orders),
    path('yourorderdetails/<int:id>/', views.yourorderdetails),
    path('cancelorder/<int:id>/', views.cancelorder),
    path('productfeedback/<int:order_id>/', views.productfeedback),
    path('storefeedback/', views.storefeedback),
    path('find_products/', views.find_products),
    path('edit_profile/<int:id>/', views.edit_profile),
    path('update_profile/', views.update_profile),
    path('insert_profile/', views.insert_profile),






] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
