from django.urls import path

from .views import email_list_signup, contact_form, subscribe


urlpatterns = [
    # path('email-signup/', email_list_signup, name='email-list-signup'),
    path('subscribe/', email_list_signup, name='subscribe'),
    path('contact/', contact_form, name='contact')
]
