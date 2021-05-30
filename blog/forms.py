from django import forms

class EmailPostForm(forms.Form):
    # This type of field is rendered as an <input type="text">
    name = forms.CharField(max_length=25)

    email = forms.EmailField()
    to = forms.EmailField()

    # with widget attribute we can change the input type of form
    comments = forms.CharField(required=False, widget=forms.Textarea)
