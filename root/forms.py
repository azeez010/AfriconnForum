from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=(("male", "male"), ("female", "female")))
    class Meta:
        model = Profile
        fields = ["about", "gender", "job_tags", "are_you_currently_unemployed", "profile_pic" ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['job_tags'].required = False
 
 
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        

