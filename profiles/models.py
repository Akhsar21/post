from django.db.models import Q
from django.core.files.base import ContentFile
from .utils import get_filtered_image, get_random_code
from django.db.models import Value
from django.db.models.functions import Concat
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
import numpy as np
from io import BytesIO

ACTION_CHOICES = (
    ('NO_FILTER', 'no filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert'),
)


def user_directory_path(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.user.username, filename)


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)

        accepted = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        print(accepted)
        print('#########')

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=300)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to=user_directory_path)
    # action = models.CharField(max_length=50, choices=ACTION_CHOICES, default='NO_FILTER')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

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

        # # open image
        # pil_img = Image.open(self.avatar)

        # # convert the image to array and do some processing
        # cv_img = np.array(pil_img)
        # img = get_filtered_image(cv_img, self.action)

        # # convert back to pil image
        # im_pil = Image.fromarray(img)

        # # save
        # buffer = BytesIO()
        # im_pil.save(buffer, format='png')
        # image_png = buffer.getvalue()

        # self.avatar.save(str(self.avatar), ContentFile(image_png), save=False)
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


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile,
                               on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile,
                                 on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
