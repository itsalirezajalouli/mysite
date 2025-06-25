from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25)                                         # a <input type="text"> 
    email = forms.EmailField()                                                      # person sending recommendation
    to = forms.EmailField()                                                         # recipient
    comment = forms.CharField(
            required = False,
            widget = forms.Textarea                                                 # override <input> -> <textarea>
            )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()
