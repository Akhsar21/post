from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# from django_comments_xtd.moderation import moderator, SpamModerator
from .badwords import badwords


User = get_user_model()

STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', 'Published'),
)


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Post View"
        verbose_name_plural = "Post Views"


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar')

    def __str__(self):
        return self.user.username

    def delete(self):
        self.avatar.delete()
        super().delete()


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    # def save(self):
    #     if not self.slug and self.name:
    #         self.slug = slugify(self.name)
    #     super().save()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ('name', 'slug')

    def get_category_url(self):
        return reverse('post-by-category', kwargs={
            'slug': self.slug
        })

    @property
    def get_posts(self):
        return Post.objects.filter(category__name=self.name)


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    # def save(self):
    #     if not self.slug and self.name:
    #         self.slug = slugify(self.name)
    #     super().save()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        unique_together = ('name', 'slug')

    def get_tag_url(self):
        return reverse('post-by-tag', kwargs={
            'slug': self.slug
        })


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', related_name='comments',
#                              on_delete=models.CASCADE)
#     content = models.TextField()
#     reply = models.ForeignKey('Comment', null=True, blank=True, related_name='replies',
#                               on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-timestamp']

#     def __str__(self):
#         return self.user.username


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='P')


class Post(models.Model):
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE, blank=True, null=True, editable=False)
    content = RichTextUploadingField()
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES, default='D')
    thumbnail = models.ImageField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL, null=True)
    featured = models.BooleanField()
    restrict_comment = models.BooleanField(default=False)
    # previous_post = models.ForeignKey('self', related_name='previous',
    #                                   on_delete=models.SET_NULL, blank=True, null=True)
    # next_post = models.ForeignKey('self', related_name='next',
    #                               on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    # def save(self):
    #     if not self.slug and self.title:
    #         self.slug = slugify(self.title)
    #     super().save()

    class Meta:
        ordering = ['-created']
        unique_together = ('title', 'slug')

    def delete(self):
        self.thumbnail.delete()
        super().delete()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'slug': self.slug
        })

    # @property
    # def get_comments(self):
    #     return self.comments.all().order_by('-timestamp').filter(reply=None)

    # @property
    # def comment_count(self):
    #     return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()


# class PostCommentModerator(SpamModerator):
#     email_notification = True

#     def moderate(self, comment, content_object, request):
#         def clean(word):
#             ret = word
#             if word.startswith('.') or word.startswith(','):
#                 ret = word[1:]
#             if word.endswith('.') or word.endswith(','):
#                 ret = word[:-1]
#             return ret

#         lowcase_comment = comment.comment.lower()
#         msg = dict([(clean(w), i)
#                     for i, w in enumerate(lowcase_comment.split())])
#         for badword in badwords:
#             if isinstance(badword, str):
#                 if lowcase_comment.find(badword) > -1:
#                     return True
#             else:
#                 lastindex = -1
#                 for subword in badword:
#                     if subword in msg:
#                         if lastindex > -1:
#                             if msg[subword] == (lastindex + 1):
#                                 lastindex = msg[subword]
#                         else:
#                             lastindex = msg[subword]
#                     else:
#                         break
#                 if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
#                     return True
#         return super().moderate(comment,
#                                 content_object,
#                                 request)


# moderator.register(Post, PostCommentModerator)
