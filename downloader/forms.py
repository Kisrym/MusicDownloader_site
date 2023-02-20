from django import forms

class DownloadForms(forms.Form):
    link = forms.CharField(label = "", required = True, widget = forms.TextInput(
        attrs = {
            "class" : "form_input",
            "placeholder" : "Cole o link aqui"
        }
    ))

    offset = forms.IntegerField(label = "", required = False, min_value = 1, widget = forms.NumberInput(
        attrs = {
        "class" : "offset_input",
        "value" : 1
        }
    ))
    
    def clean_link(self):
        nome = self.cleaned_data.get("link")

        if nome:
            if "playlist" in nome or "track" in nome:
                return nome
            else:
                raise forms.ValidationError("Link inválido")