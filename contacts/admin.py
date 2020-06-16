from django.contrib import admin

from .models import Signup, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')
    list_filter = ('status',)


admin.site.register(Signup)
admin.site.register(Contact, ContactAdmin)
