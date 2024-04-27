from django.contrib.sitemaps.views import index
from django.urls import path

from .views import *

urlpatterns=[
    path('', home, name='home'),
    path('howtobuy/', howtobuy, name='howtobuy'),
    path('contact/', contact, name='contact'),
    path('feedback/', feedback, name='feedback'),
    path('basket/', basket, name='basket'),
    path('category/<int:cat_id>/', category, name='category'),
    path('product_page/<int:prod_id>', product_page, name='product_page'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('client_page/', client_page, name='client_page'),
    path('confirm_page/', confirm_page, name='confirm_page'),
]
