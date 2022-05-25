from django.forms import ModelForm
from app_1.models import campaign_table



class add_campaign(ModelForm):
    class Meta:
        model = campaign_table
        fields = ['campaign_name', 'campaign_slug', 'start_time', 'end_time', 'campaign_logo', 'campaign_benner', 'free_delivery'] 
        
        
class edit_campaign(ModelForm):
    class Meta:
        model = campaign_table
        fields = '__all__'
        