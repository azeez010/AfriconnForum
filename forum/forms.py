from django import forms
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Thread, Comment, Category

class Register_user(UserCreationForm):
    accept_terms = forms.BooleanField(label="accept terms")
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "accept_terms"]
        
    def __init__(self, *args, **kwargs):
        super(Register_user, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class create_thread_category(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title", "description", "image"]
        
        def __init__(self, *args, **kwargs):
            super(create_thread_category, self).__init__(*args, **kwargs)
            # self.fields['title'].widget = forms.TextInput(attrs={"placeholder": "category title..."})
       
        
class create_thread(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "details", "image"]
    def __init__(self, *args, **kwargs):
        super(create_thread, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        
class create_comment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment", "image"]
    
    def __init__(self, *args, **kwargs):
        super(create_comment, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
    
class report(forms.Form):
    report = forms.CharField(max_length=1024, widget=(forms.Textarea(attrs={"placeholder": "report..."})))
    report_type = forms.ChoiceField(choices=(("offensive", "offensive"), ("sexual", "sexual")))