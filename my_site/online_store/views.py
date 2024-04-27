from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.
from .forms import RegistrationForm
from .models import *

menu = [
        {'title':'Оплата і доставка', 'url_name': 'howtobuy'},
        {'title':'Контакти', 'url_name': 'contact'},
        {'title':"Зворотній зв'язок", 'url_name': 'feedback'},
        {'title':'Кошик', 'url_name': 'basket'},
        # {'title':'Увійти', 'url_name': 'login'},
]

def home(request):
    query = request.GET.get('q')
    if query:
        prod = Product.objects.filter(name__icontains=query)
    else:
        prod = Product.objects.all()
    paginator = Paginator(prod, 3)
    page = request.GET.get('page')
    if page:
        prod = paginator.get_page(page)
    else:
        prod = paginator.get_page(1)

    goods = Category.objects.all()

    context = {'menu': menu, 'goods': goods, 'prod': prod}
    return render(request, 'home.html', context=context)

def category(request, cat_id):
    search_query = request.GET.get('q')

    if search_query:
        prod = Product.objects.filter(cat_id=cat_id, name__icontains=search_query)
    else:
        prod = Product.objects.filter(cat_id=cat_id)
    paginator = Paginator(prod, 3)
    page = request.GET.get('page')
    if page:
        prod = paginator.get_page(page)
    else:
        prod = paginator.get_page(1)
    goods = Category.objects.filter(id=cat_id)
    context = {'menu': menu, 'prod': prod, 'goods': goods, 'cat_selected': cat_id, 'search_query': search_query}
    return render(request, 'category.html', context=context)

def search(request):
    query = request.GET.get('q')
    prod = Product.objects.filter(name__icontains=query)
    context = {'menu': menu, 'prod': prod, 'query': query}
    return render(request, 'home.html', context=context)

def product_page(request, prod_id):
    prod = Product.objects.filter(id=prod_id)
    goods = Category.objects.all()
    context = {'menu': menu, 'prod': prod, 'goods': goods, 'cat_selected': prod_id}
    return render(request, 'product_page.html', context=context)

def howtobuy(request):
    goods = Category.objects.all()
    context = {'menu': menu, 'goods': goods}
    return render(request, 'howtobuy.html', context=context)

def feedback(request):
    goods = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        feedback = Feedback(name=name, email=email, message=message)
        feedback.save()
        return redirect('confirm_page')

    context = {'menu': menu, 'goods': goods}
    return render(request, 'feedback.html', context=context)

def contact(request):
    goods = Category.objects.all()
    context = {'menu': menu, 'goods': goods}
    return render(request, 'contact.html', context=context)


def basket(request):
    goods = Category.objects.all()
    selected_product_ids = request.session.get('selected_product_ids', [])

    if request.method == 'POST':
        selected_product_ids += request.POST.getlist('product_id')

        if 'remove_product_id' in request.POST:
            remove_product_id = request.POST.get('remove_product_id')
            selected_product_ids.remove(remove_product_id)
        elif 'continue_shopping' in request.POST:
            return redirect('home')

        request.session['selected_product_ids'] = selected_product_ids

    selected_products = Product.objects.filter(id__in=selected_product_ids)

    total_sum = Decimal(0)
    product_quantities = {}
    for product in selected_products:
        quantity = int(request.POST.get(f'quantity{product.id}', 1))
        product_quantities[product.id] = quantity
        subtotal = product.price * Decimal(quantity)
        total_sum += subtotal

    context = {
        'menu': menu,
        'goods': goods,
        'selected_products': selected_products,
        'product_quantities': product_quantities,
        'total_sum': total_sum
    }
    return render(request, 'basket.html', context=context)


def register(request):
    goods = Category.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('client_page')
    else:
        form = RegistrationForm()
    context = {'menu': menu, 'goods': goods, 'form': form}
    return render(request, 'registration.html', context=context)

def login(request):
    goods = Category.objects.all()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('client_page')
    else:
        form = AuthenticationForm()

    context = {'menu': menu, 'goods': goods, 'form': form, 'user': request.user}
    return render(request, 'login.html', context=context)


def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required(login_url='login')
def client_page(request):
    goods = Category.objects.all()
    orders = Order.objects.filter(name=request.user.username)
    context = {'menu': menu, 'goods': goods, 'orders': orders}
    return render(request, 'client_page.html', context=context)


def confirm_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        submit_order = request.POST.get('submit_order')

        if submit_order:
            selected_product_ids = request.session.get('selected_product_ids')
            products = Product.objects.filter(id__in=selected_product_ids)
            total_sum = 0
            for product in products:
                quantity = request.POST.get(f'quantity{product.id}')
                if quantity:
                    quantity = int(quantity)
                    total_sum += product.price * quantity
            products_str = ', '.join([f'{product.name} ({product.price})' for product in products])
            order = Order.objects.create(
                name=name,
                phone=phone,
                email=email,
                products=products_str,
                total_sum=total_sum
            )
            request.session.pop('selected_product_ids', None)
            return redirect('confirm_page')

    goods = Category.objects.all()
    request.session.pop('selected_product_ids', None)
    context = {'menu': menu, 'goods': goods}
    return render(request, 'confirm_page.html', context=context)

