from django.contrib import admin
from .models import Post,Category
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','published_date','is_active','category',)
    readonly_fields = ('slug',)
    list_filter = ('title','category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    list_filter = ('is_active',)