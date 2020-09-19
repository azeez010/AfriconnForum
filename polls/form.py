from django import forms

class PollForm(forms.Form):
    poll = forms.CharField(max_length=400, widget=(forms.TextInput(attrs={"placeholder": "Poll Title"})))
    image = forms.ImageField(required=False)
    expiryDate = forms.ChoiceField(required=True, choices=(("", "--select timespan --"), (86400, "one day"), (259200, "three days"), (604800, "a week")))
    

    
# class PollChoiceForm(forms.Form):
#     PollChoice = forms.CharField(max_length=500, widget=(forms.TextInput(attrs={"placeholder": "Input choices"})))