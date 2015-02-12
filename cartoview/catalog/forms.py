from django import forms
from models import UpdateFrequency, CoordSystem, UrlType, DataType,Resource,Url,UrlImage,Settings

'''class SubmissionForm(forms.Form):
    dataset_name = forms.CharField(max_length=255, label="Data set, API or App name")
    organization = forms.CharField(max_length=255)
    copyright_holder = forms.CharField(max_length=255)
    contact_email = forms.CharField(max_length=255)
    contact_phone = forms.CharField(max_length=255)
    url = forms.CharField(max_length=255, label="Data/API/App url")
    time_period = forms.CharField(required=False, max_length=255, label="Valid time period")
    release_date = forms.DateField(required=False)
    area_of_interest = forms.CharField(max_length=255, label="Geographic area")
    
    update_frequency = forms.ModelChoiceField(required=False, queryset=UpdateFrequency.objects.all())
    coord_system = forms.ModelMultipleChoiceField(required=False, queryset=CoordSystem.objects.all(), label="Coordinate system")
    wkt_geometry = forms.CharField(widget=forms.Textarea, label="Well known Text (WKT) geometry of the dataset")
    types = forms.ModelMultipleChoiceField(required=False, queryset=UrlType.objects.all(), label="Data types")
    formats = forms.ModelMultipleChoiceField(required=False, queryset=DataType.objects.all(), label="Data formats")
    
    description = forms.CharField(max_length=1000, widget=forms.Textarea, label="Describe this dataset")
    usage_limitations = forms.CharField(max_length=1000, widget=forms.Textarea, label="Are there usage limitations?")
    collection_process = forms.CharField(max_length=1000, widget=forms.Textarea, label="How was the data collected?")
    data_purpose = forms.CharField(max_length=1000, widget=forms.Textarea, label="Why was the data collected?")
    intended_audience = forms.CharField(max_length=1000, widget=forms.Textarea, label="Who is the intended audience?")
    why = forms.CharField(max_length=1000, widget=forms.Textarea, label="Why should the data be included in this site?")
    certified = forms.BooleanField(required=False, label="", help_text="I am the copyright holder or have permission to release this data")
    terms = forms.BooleanField(label="", help_text="I have read and agree with the site's <a href='/terms/' target='_blank'>terms of use</a>")'''

Provider_Choices = [('arcgis', 'ArcGIS',)]
DataType_Choices = [('file', 'File',),
                        ('database','Database')]

Service_Choices = [('map_server', 'Map Server',),
    ('map_server_layer', 'Map server layer.',),
    ('feature_server', 'Feature server',),
                   ('feature_server_layer','Feature server layer',)]
class ResourceForm(forms.ModelForm):
    name = forms.CharField( label="Title")
    class Meta:
        model = Resource
        fields = ['name', 'short_description','description','categories' ,'location_extent']
        exclude = ['location_extent']
    
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'short_description', 'description','categories','organization','usage',]
        exclude = ['location_extent']

class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['url', 'url_label', 'url_type' ]
        widgets = {
            'provider':  forms.Select(),
            'service_type': forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs)
        self.fields['url_type'].label = "Type"
        self.fields['url_type'].queryset  = UrlType.objects.all()

class APIform(forms.ModelForm):
    class Meta:
        model = Url
        fields = [ 'provider' , 'service_type']
        widgets = {
            'provider':  forms.Select(),
            'service_type': forms.Select(),}


    def __init__(self, *args, **kwargs):
        super(APIform, self).__init__(*args, **kwargs)
        self.fields['provider'].required = True
        self.fields['service_type'].required  = True

class UrlImageForm (forms.ModelForm):
    class Meta:
        model = UrlImage
        fields = ['image']

class SettingsForm (forms.ModelForm):
    class Meta:
        model = Settings
        exclude = ['site']
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        if self.fields['default_view'].choices[0][0] == '':
            default_view_choices = self.fields['default_view'].choices
            del default_view_choices[0]
            self.fields['default_view'].choices = default_view_choices

class DataTypeForm (forms.ModelForm) :
    class Meta:
        model = Resource
        fields = ['data_types']

    def __init__(self, *args, **kwargs):
        super(DataTypeForm, self).__init__(*args, **kwargs)
        self.fields['data_types'].required = True
