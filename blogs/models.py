from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

from profiles.models import Profile


STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', 'Published'),
)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
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
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

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

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        unique_together = ('name', 'slug')

    def get_tag_url(self):
        return reverse('post-by-tag', kwargs={
            'slug': self.slug
        })


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='P')


class Post(models.Model):
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    content = RichTextUploadingField()
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D')
    thumbnail = models.ImageField(upload_to='posts/%Y/%m/%d', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=None)
    updated = models.DateTimeField(auto_now=True, editable=None)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    featured = models.BooleanField(default=False)
    restrict_comment = models.BooleanField(default=False)
    # previous_post = models.ForeignKey('self', related_name='previous',
    #                                   on_delete=models.SET_NULL, blank=True, null=True)
    # next_post = models.ForeignKey('self', related_name='next',
    #                               on_delete=models.SET_NULL, blank=True, null=True)
# , through="Like"

    class Meta:
        ordering = ['-created']
        unique_together = ('title', 'slug')

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save()

    def delete(self):
        self.thumbnail.delete()
        super().delete()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post-update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'slug': self.slug})

    def get_like_url(self):
        return reverse("like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("like-api-toggle", kwargs={"slug": self.slug})

    # @property
    # def total_likes(self):
    #     return self.likes.all().count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     value = models.CharField(max_length=10, default='Like', choices=LIKE_CHOICES)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created']

    # def __str__(self):
    #     return self.user.username
