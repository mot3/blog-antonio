from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # This type of field is rendered as an <input type="text">
    name = forms.CharField(max_length=25)

    email = forms.EmailField()
    to = forms.EmailField()

    # with widget attribute we can change the input type of form
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    # Created from a model
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body',)
