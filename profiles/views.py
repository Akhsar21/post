from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.translation import gettext as _
from django.conf import settings

from .models import Profile
from .forms import ProfileForm, UserForm


@login_required
@transaction.atomic
def my_profiles_view(request):
    profile = Profile.objects.get(user=request.user)
    confirm = False

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST or None,
                                   request.FILES or None, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _(
                'Your profile was successfully updated!'))
            # return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(request.POST or None,
                                   request.FILES or None, instance=profile)

    context = {
        'profile': profile,
        'confirm': confirm,
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profiles/myprofile.html', context)
