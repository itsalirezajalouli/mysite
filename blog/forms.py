from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25)                                         # a <input type="text"> 
    email = forms.EmailField()                                                      # person sending recommendation
    to = forms.EmailField()                                                         # recipient
    comments = forms.CharField(
            required = False,
            widget = forms.Textarea                                                 # override <input> -> <textarea>
            )

