from django import forms

class DownloadForms(forms.Form):
    link = forms.CharField(label = "", required = True, widget = forms.TextInput(
        attrs = {
            "class" : "form_input",
            "placeholder" : "Cole o link aqui"
        }
    ))