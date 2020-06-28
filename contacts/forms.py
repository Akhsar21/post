from django import forms
from .models import Signup, Contact


class EmailSignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('email', )
        labels = {'email': '', }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Type your email address', })
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        # labels = {'name': '', 'email': '', 'subject': '', 'message': '', }
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': '', }),
            "email": forms.TextInput(attrs={'placeholder': '', }),
            "subject": forms.TextInput(attrs={'placeholder': '', }),
            "message": forms.Textarea(attrs={'cols': '30', 'rows': '7', 'placeholder': '', }),
        }
        fields_required = ('name', 'email', 'subject', 'message')
