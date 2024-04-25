from django.contrib import admin
from .models import *

class Image_admin(admin.ModelAdmin):
    list_display = ("name", "Image_category", "Image_id")

class user_admin(admin.ModelAdmin):
    list_display = ("name", "email")

admin.site.register(Image, Image_admin)
admin.site.register(user, user_admin)

# Register your models here.
