from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                attrs={'placeholder':'Your full name'}))
    email = forms.EmailField(widget=forms.TextInput(
                attrs={'placeholder':'Your email (for replies)'}))
    message = forms.CharField(widget=forms.Textarea(
                attrs={
                    'placeholder':('Suggestions, improvements and corrections'
                                   ' or whatever you like or dislike about this app!')}))

