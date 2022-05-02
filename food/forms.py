from django import forms
from django.contrib.auth.models import User
from . import models

#for admin
# class AdminSigupForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']


#for Donar related form
class DonarUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class DonarExtraForm(forms.ModelForm):
    class Meta:
        model=models.DonarExtra
        fields=['company_name','address','mobile','email']



#for NGO related form
class NGOUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','username','email','password']
class NGOExtraForm(forms.ModelForm):
    class Meta:
        model=models.NGOExtra
        fields=['address','mobile']




#for Attendance related form
# presence_choices=(('Present','Present'),('Absent','Absent'))
# class AttendanceForm(forms.Form):
#     present_status=forms.ChoiceField( choices=presence_choices)
#     date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()




#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
