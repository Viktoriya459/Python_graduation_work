from django.contrib import admin

# Register your models here.

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'size', 'availability',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('availability',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'total_sum', 'created_at')
    readonly_fields = ('total_sum',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    list_display_links = ('name', 'email', 'message', 'created_at')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)