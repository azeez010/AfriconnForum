from django import forms
from .models import Applicant, Job
from tinymce.widgets import TinyMCE

class create_job(forms.ModelForm):
   position = forms.ChoiceField(choices=(("full-time", "full-time"),("part-time", "part-time"), ("intern-ship", "intern-ship"), ("remote", "remote")))
   category = forms.ChoiceField(choices=(("select category",""), ("programming","programming"), ("office jobs","office jobs"), ("finance","finance"), ("gigs","gigs"), ("graphic designers", "graphic designers"), ("artisans", "artisans"), ("others","others")))
   class Meta:
      model = Job
      fields = ["title", "name_of_company", "details", "address", "jobImage", "pay" ]
   def __init__(self, *args, **kwargs):
      super(create_job, self).__init__(*args, **kwargs)
      self.fields['jobImage'].required = False
      self.fields['address'].required = False
      self.fields['category'].required = True
      self.fields['pay'].required = False
      self.fields['address'].widget = forms.TextInput(attrs={"placeholder": "company's address..."})
      self.fields['pay'].widget = forms.NumberInput(attrs={"placeholder": "e.g 50000 optional"}) 



class ResumeForm(forms.Form):
    first_name = forms.CharField(max_length=500, widget=(forms.TextInput(attrs={"placeholder": "your first name"})))
    last_name = forms.CharField(max_length=500, widget=(forms.TextInput(attrs={"placeholder": "your last name"})))
    skills = forms.CharField(max_length=500, widget=(forms.TextInput(attrs={"placeholder": "your core skills..."})))
    phone = forms. CharField(max_length=18, required=False, widget=(forms.NumberInput(attrs={"placeholder": "your phone optional..."})))
    proposal = forms.CharField(widget=TinyMCE())#forms.CharField(max_length=5000, widget=(forms.Textarea(attrs={"placeholder": "what can you do..."})))
    Education_and_Work_experience = forms.CharField(widget=TinyMCE())#forms.CharField(max_length=10000, required=False, widget=(forms.Textarea(attrs={"placeholder": "your eduction and previous experience optional"})))
