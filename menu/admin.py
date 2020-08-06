from django.contrib import admin
from .models import Menu, MenuItem

# Register your models here.


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    ordering = ('order',)


class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    inlines = [MenuItemInline, ]
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Menu, MenuAdmin)
