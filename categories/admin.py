from django.contrib import admin
from .models import CategoriesModel
# Register your models here.

class CategorySlug(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']
    


admin.site.register(CategoriesModel,CategorySlug)
