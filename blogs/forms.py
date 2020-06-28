from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'thumbnail',
                  'category', 'tags', 'status', 'restrict_comment', 'featured')
        widgets = {
            'content': CKEditorUploadingWidget(attrs={'required': False, 'cols': 30, 'rows': 10}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
