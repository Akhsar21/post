from django.contrib import admin
from django.contrib.auth.admin import Group

# Register your models here.
admin.site.site_header = 'Akhsar admin'
admin.site.site_title = 'Akhsar admin'
admin.site.index_title = 'Akhsar administration'

admin.site.unregister(Group)
