from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                attrs={'placeholder':'Your full name'}))
    email = forms.EmailField(widget=forms.TextInput(
                attrs={'placeholder':'Your email (for replies)'}))
    message = forms.CharField(widget=forms.Textarea(
                attrs={'placeholder':'Whatever you like, dislike or love about this app!'}))

