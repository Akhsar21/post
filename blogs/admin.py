from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Author, Category, Post, PostView, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    '''Admin View for Author'''

    readonly_fields = ["author_avatar", ]

    def author_avatar(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.avatar.url,
                width='300px',
                height='300px',
            )
        )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'content', 'thumbnail', 'tags', 'category', 'status')
        }),
        ('Short descriptions', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('description', 'likes'),
        }),
    )
    list_display = ('title', 'created', 'featured', 'restrict_comment')
    list_filter = ('title', 'created')
    search_fields = ['title']
    # view_on_site = True
    list_editable = ('featured', 'restrict_comment')
    readonly_fields = ['post_image', 'slug', ]
    autocomplete_fields = ['tags', ]
    date_hierarchy = 'created'

    def view_on_site(self, obj):
        url = obj.get_absolute_url()
        return url

    def post_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.thumbnail.url,
                width='500px',
                height='300px',
            )
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin View for Tag'''

    search_fields = ['name']
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    search_fields = ['name']
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(PostView)
