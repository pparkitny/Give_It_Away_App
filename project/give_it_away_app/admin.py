from django.contrib import admin

from .models import Donation, Institution, Category

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
