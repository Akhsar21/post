from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    base_url = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()

    def save(self):
        """
        Re-order all items at from 10 upwards, at intervals of 10.
        This makes it easy to insert new items in the middle of
        existing items without having to manually shuffle
        them all around.
        """
        super(Menu, self).save()

        current = 10
        for item in MenuItem.objects.filter(menu=self).order_by('order'):
            item.order = current
            item.save()
            current += 10


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.IntegerField()
    link_url = models.CharField(max_length=100, help_text=_(u'URL or URI to the content, eg /about/ or http://foo.com/'))
    title = models.CharField(max_length=100)
    login_required = models.BooleanField(blank=True, null=True, help_text=_(u'Should this item only be shown to authenticated users?'))
    anonymous_only = models.BooleanField(blank=True, default=False, help_text=_(u'Should this item only be shown to non-logged-in users?'))

    def __unicode__(self):
        return "%s %s. %s" % (self.menu.slug, self.order, self.title)

    # def __init__(self):
    #     return self.__unicode__()
