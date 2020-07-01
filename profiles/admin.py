from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile, Relationship

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

    # list_display = ('full_name', 'email', 'country')
    list_filter = ('created',)
    # raw_id_fields = ('',)
    readonly_fields = ('slug', 'avatar_profile')
    search_fields = ('user', )
    autocomplete_fields = ['friends']
    date_hierarchy = 'created'
    ordering = ('-created',)

    def avatar_profile(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.avatar.url,
                width='300px',
                height='300px',
            )
        )

admin.site.register(Relationship)