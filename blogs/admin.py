from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Author, Category, Post, PostView, Tag


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ["author_avatar", ]

    def author_avatar(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.avatar.url,
            width='300px',
            height='300px',
        )
        )


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'featured', 'restrict_comment')
    list_filter = ('title', 'created')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    view_on_site = True
    list_editable = ('featured', 'restrict_comment')
    autocomplete_fields = ['tags']

    # def view_on_site(self, obj):
    #     url = obj.get_absolute_url()
    #     return 'http://127.0.0.1:8000' + url

    readonly_fields = ["created", "updated", "post_image", ]

    def post_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.thumbnail.url,
            width='500px',
            height='300px',
        )
        )


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostView)
admin.site.register(Tag, TagAdmin)
