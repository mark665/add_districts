from django import forms
    
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label = 'Select a file',
        help_text = 'max. 42 megabytes'
    )
    
    
# def clean( self ): 
    # cleaned_data = self.cleaned_data
    # file = cleaned_data.get( "docfile" )
    # file_exts = ('.csv', ) 

    # if file is None:

        # raise forms.ValidationError( 'Please select file first ' ) 

    # if not file.content_type in settings.UPLOAD_AUDIO_TYPE: #UPLOAD_AUDIO_TYPE contains mime types of required file

        # raise forms.ValidationError( 'Audio accepted only in: %s' % ' '.join( file_exts ) ) 


    # return cleaned_data

