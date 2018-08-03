from django.contrib import admin
from .models import Brand, Car, Image


# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'car_type', 'year', 'registration_indicator', 'number_of_seats', 'colour',
                    'description', 'stock_count', 'price', 'brand']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'image']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Image, ImageAdmin)
