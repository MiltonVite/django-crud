from django import forms

class CreateNewTask(forms.Form):
    title = forms.CharField(label="Titulo: ", max_length=200)
    description = forms.CharField(widget=forms.Textarea, label="Descripcion: ")
    
class createNewProjetc(forms.Form):
    
    name = forms.CharField(label="Nombre del proyecto: ", max_length=200)