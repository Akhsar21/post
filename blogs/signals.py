from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from .models import Post


def create_redirect(sender, instance, **kwargs):
    if sender == Post:
        try:
            o = sender.objects.get(id=instance.id)
            if o.slug != instance.slug:
                old_path = o.get_absolute_url()
                new_path = instance.get_absolute_url()

                for redirect in Redirect.objects.filter(new_path=old_path):
                    redirect.new_path = new_path

                    if redirect.new_path == redirect.old_path:
                        redirect.delete()
                    else:
                        redirect.save()
        except sender.DoesNotExist:
            pass
