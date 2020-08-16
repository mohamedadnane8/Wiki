from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label="")


class CreateForm(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "Txt"}),
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "Txt", "id": "contentTxt"},),
    )
