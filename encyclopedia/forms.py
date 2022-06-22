from django import forms

from encyclopedia import util

class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': "form-control text"})
    )
    entry = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': "form-control text textarea"})
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if util.get_entry(title) != None:
            raise forms.ValidationError("The page \"" + title + "\" already exists")

        return title

class EditEntryForm(forms.Form):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'class': "form-control text textarea"})
    )

class SearchForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': "search form-control form-control-sm",
            'type': "text",
            'name': "q",
            'placeholder': "Search Encyclopedia"
        })
    )