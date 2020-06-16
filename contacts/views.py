from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template

from .forms import EmailSignupForm, ContactForm
from .models import Signup, Contact

import json
import requests
from django.core.mail import send_mail

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(dc=MAILCHIMP_DATA_CENTER)
members_endpoint = '{api_url}/lists/{list_id}/members'.format(
    api_url=api_url,
    list_id=MAILCHIMP_EMAIL_LIST_ID
)


def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()


def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed")
            else:
                subscribe(form.instance.email)
                form.save()
                messages.success(request, "You email has been submitted!")

                # subject="Thank You For Joining Our Newsletter"
                # from_email=settings.DEFAULT_FROM_EMAIL
                # to_email=[form.instance.email]
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def contact_form(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            contactdata = Contact()
            contactdata.name = form.cleaned_data['name']
            contactdata.email = form.cleaned_data['email']
            contactdata.subject = form.cleaned_data['subject']
            contactdata.message = form.cleaned_data['message']

            # Email ourselves the submitted contact message

            subject = contactdata.subject
            from_email = contactdata.email
            to_email = [settings.DEFAULT_FROM_EMAIL]

            context = {
                'user': contactdata.name,
                'email': contactdata.email,
                'message': contactdata.message
            }

            contact_message = get_template(
                'email/contact_message.txt').render(context)
            send_mail(subject, contact_message, from_email,
                      to_email, fail_silently=True)

            contactdata.save()
            messages.success(
                request, "Your message has been sent. Thank You for your interest")
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
