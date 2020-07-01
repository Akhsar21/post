from django.db.models import Value
from django.db.models.functions import Concat
from django.db import models
from django.contrib.auth.models import User
# from django.template.defaultfilters import slugify
from django.utils.text import slugify
from .utils import get_random_code


class Profile(models.Model):
    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=300)
    # email = models.EmailField(max_length=254, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    full_name.admin_order_field = Concat('first_name', Value(' '), 'last_name')

    def save(self, *args, **kwargs):
        ex = False
        if self.user.first_name and self.user.last_name:
            to_slug = slugify(str(self.user.first_name) + " " + str(self.user.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts_count(self):
        return self.posts.all().count()

    # def get_all_authors_posts(self):
    #     return self.posts.all()

    # def get_likes_given_count(self):
    #     likes = self.like_set.all()
    #     total_liked = 0
    #     for item in likes:
    #         if item.value == 'like':
    #             total_liked += 1
    #     return total_liked

    # def get_likes_received_count(self):
    #     posts = self.posts.all()
    #     total_liked = 0
    #     for item in posts:
    #         total_liked += item.likes.all().count()
    #     return total_liked


STATUS_CHOICES = (
    ('sender', 'Sender'),
    ('accepted', 'Accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile,
                               on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile,
                                 on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
