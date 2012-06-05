from django import forms

CHOICES = (
(0, 'a'),
(1, 'b'),
(2, 'c'),
)
  
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label = 'Select a File',
        help_text = 'max. 42 megabytes',
        
    )
    letters = forms.MultipleChoiceField(
            choices=CHOICES, 
            label="...", 
            required=False)

    

