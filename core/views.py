from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View

from blogs.models import Post
from contacts.forms import EmailSignupForm
from contacts.models import Signup


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)[0:2]
        latest = Post.objects.order_by('-published')[0:3]
        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")
