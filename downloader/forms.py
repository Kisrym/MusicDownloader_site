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
        "placeholder" : "Ínicio"
        }
    ))
    
    limit = forms.IntegerField(label = "", required = False, min_value = 1, max_value = 50, widget = forms.NumberInput(
        attrs = {
            "class" : "offset_input",
            "placeholder" : "Fim"
        }
    ))

    def clean_link(self):
        nome = self.cleaned_data.get("link")

        if nome:
            for item in ["track", "playlist", "watch", "youtu.be"]:
                if item in nome:
                    return nome
                
            raise forms.ValidationError("Link inválido")