# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.views import View
# from .models import *
# from .utils import DataMixin
# menu = [
#             {'title': 'Оплата і доставка', 'url_name': 'howtobuy'},
#             {'title': 'Контакти', 'url_name': 'contact'},
#             {'title': "Зворотній зв'язок", 'url_name': 'feedback'},
#             {'title': 'Кошик', 'url_name': 'basket'},
#             {'title': 'Увійти', 'url_name': 'login'}
#         ]
#
#
# class HomeView(View, DataMixin):
#     def get(self, request):
#         query = request.GET.get('q')
#         if query:
#             prod = Product.objects.filter(name__icontains=query)
#         else:
#             prod = Product.objects.all()
#             goods = Category.objects.all()
#         context = self.get_data()
#         context['goods'] = goods
#         context['prod'] = prod
#         if not prod:
#             return redirect('home')
#         return render(request, 'home.html', context=context)
#
#
# class CategoryView(View, DataMixin):
#     def get(self, request, cat_id):
#         search_query = request.GET.get('q')
#         if search_query:
#             prod = Product.objects.filter(cat_id=cat_id, name__icontains=search_query)
#         else:
#             prod = Product.objects.filter(cat_id=cat_id)
#         goods = Category.objects.filter(id=cat_id)
#         context = self.get_data()
#         context['prod'] = prod
#         context['goods'] = goods
#         context['cat_selected'] = cat_id
#         context['search_query'] = search_query
#         if not prod:
#             return redirect('home')
#         return render(request, 'category.html', context=context)
#
#
# class SearchView(View, DataMixin):
#     def get(self, request):
#         query = request.GET.get('q')
#         prod = Product.objects.filter(name__icontains=query) if query else []
#         context = self.get_data()
#         context['prod'] = prod
#         context['query'] = query
#         return render(request, 'home.html', context=context)
#
#
# class ProductPageView(View, DataMixin):
#     def get(self, request, prod_id):
#         prod = Product.objects.filter(id=prod_id)
#         goods = Category.objects.all()
#         context = self.get_data()
#         context['prod'] = prod
#         context['goods'] = goods
#         context['cat_selected'] = prod_id
#         return render(request, 'product_page.html', context=context)
#
#
# class HowToBuyView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         context = self.get_data()
#         context['goods'] = goods
#         return render(request, 'howtobuy.html', context=context)
#
#
# class FeedbackView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         context = self.get_data()
#         context['goods'] = goods
#         return render(request, 'feedback.html', context=context)
#
#     def post(self, request):
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         feedback = Feedback(name=name, email=email, message=message)
#         feedback.save()
#         return redirect('confirm_page')
#
#
# class ContactView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         context = self.get_data()
#         context['goods'] = goods
#         return render(request, 'contact.html', context=context)
#
#
# class LoginView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         context = self.get_data()
#         context['goods'] = goods
#         return render(request, 'login.html', context=context)
#
#
# class BasketView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         selected_product_ids = request.session.get('selected_product_ids', [])
#         selected_products = Product.objects.filter(id__in=selected_product_ids)
#         total_sum = sum(product.price for product in selected_products)
#         context = {
#             'menu': menu,
#             'goods': goods,
#             'selected_products': selected_products,
#             'total_sum': total_sum
#         }
#         return render(request, 'basket.html', context=context)
#
#     def post(self, request):
#         if 'product_id' in request.POST:
#             product_id = request.POST.get('product_id')
#             session_selected_product_ids = request.session.get('selected_product_ids', [])
#             session_selected_product_ids.append(product_id)
#             request.session['selected_product_ids'] = session_selected_product_ids
#
#         if 'remove_product_id' in request.POST:
#             remove_product_id = request.POST.get('remove_product_id')
#             session_selected_product_ids = request.session.get('selected_product_ids', [])
#             session_selected_product_ids.remove(remove_product_id)
#             request.session['selected_product_ids'] = session_selected_product_ids
#         elif 'continue_shopping' in request.POST:
#             return redirect('home')
#
#         return redirect('basket')
#
#
# class ClientPageView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         context = self.get_data()
#         context['goods'] = goods
#         return render(request, 'client_page.html', context=context)
#
#
# class ConfirmPageView(View, DataMixin):
#     def get(self, request):
#         goods = Category.objects.all()
#         request.session.pop('selected_product_ids', None)
#         context = self.get_data()
#         context['goods'] = goods
#         return render(request, 'confirm_page.html', context=context)
#
#     def post(self, request):
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         submit_order = request.POST.get('submit_order')
#
#         if submit_order:
#             selected_product_ids = request.session.get('selected_product_ids')
#             products = Product.objects.filter(id__in=selected_product_ids)
#             total_sum = 0
#             for product in products:
#                 quantity = request.POST.get(f'quantity_{product.id}')
#                 if quantity:
#                     quantity = int(quantity)
#                     total_sum += product.price * quantity
#             products_str = ', '.join([f'{product.name} ({product.price})' for product in products])
#             order = Order.objects.create(
#                 name=name,
#                 phone=phone,
#                 email=email,
#                 products=products_str,
#                 total_sum=total_sum
#             )
#             request.session.pop('selected_product_ids', None)
#             return redirect('confirm_page')


