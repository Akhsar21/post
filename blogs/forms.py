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
            # 'featured': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.use_custom_control = False
        self.helper.form_method = 'POST'  # get or post
        self.helper.add_input(Submit('submit', 'Submit'))
        # self.fields['my_field'].label = False


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('content', )
#         labels = {'content': '', }
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': '6', 'placeholder': 'Type your comment'})
#         }
