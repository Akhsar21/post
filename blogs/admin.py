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

    list_display = ('title', 'created', 'featured', 'restrict_comment')
    list_filter = ('title', 'created')
    search_fields = ['title']
    # prepopulated_fields = {'slug': ('title',)}
    view_on_site = True
    list_editable = ('featured', 'restrict_comment')
    autocomplete_fields = ['tags']
    # exclude = ('author',)

    # def save_model(self, request, obj, form, change):
    #     obj.author = request.user
    #     obj.save()

    # def view_on_site(self, obj):
    #     url = obj.get_absolute_url()
    #     return 'http://127.0.0.1:8000' + url

    readonly_fields = ["post_image", "slug"]

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
# admin.site.register(Like)
