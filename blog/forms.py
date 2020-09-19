from django import forms
from .models import Blog 

class create_blog(forms.ModelForm):
   select_category = forms.ChoiceField(choices=(("programming","programming"), ("news","news"), ("finance","finance"), ("sport","sport"), ("politics","politics"), ("technology","technology"), ("celebrities","celebrities"), ("education","education"),("health","health"), ("lifestyle","lifestyle"),  ("science", "science"), ("arts", "arts")))
   tags = forms.CharField(max_length=400, widget=(forms.TextInput(attrs={"placeholder": "space seperate your tags..."}))) 
   
   class Meta:
      model = Blog
      fields = ['title', 'details',  'select_category', 'tags', 'image']
   