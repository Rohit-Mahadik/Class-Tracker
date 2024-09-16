from django import forms
from Teacher.models import AddSubject,AddBatch,AddStudent,Batch_message,Announcement,LeavePlannerModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,UserChangeForm,PasswordChangeForm


GENDER_CHOICES = [
	('Male','Male'),
	('Female','Female'),
	('Other','Other'),
]



# Edit_profile_form
class Edit_profile_form(forms.ModelForm):
	student_gender = forms.ChoiceField(label='Gender',choices=GENDER_CHOICES,widget=forms.RadioSelect())
	class Meta:
		model = AddStudent
		fields = ['student_name','student_id','student_number','student_dob','student_address','student_image','student_gender']
		widgets = {
			 'student_name':forms.TextInput(attrs={'class':'form-control'}),
			 'student_id':forms.TextInput(attrs={'class':'form-control'}),
			 'student_number':forms.NumberInput(attrs={'class':'form-control'}),
			 'student_dob':forms.DateInput(attrs={'class':'form-control','type':'date'}),
			 'student_address':forms.Textarea(attrs={'class':'form-control','rows':4}),
			}
		labels={
			'student_name':'Name',
			'student_id':'ID',
			'student_number':'Contact No',
			'student_dob':'DOB',
			'student_address':'Address',
			'student_image':'Image',
			}
		




# Edit Username
class Edit_username_form(UserChangeForm):
	class Meta:
		model = User 
		fields = ['username','email']
		widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
			 		'email':forms.EmailInput(attrs={'class':'form-control'}),
			 }
		



LEAVE_TYPE_CHOICES = (
    ('AN', 'Annual Leave'),
    ('SL', 'Sick Leave'),
    ('PL', 'Personal Leave'),
)


LEAVE_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)


#Leave_PLANNER_FORM

class LeavePlannerForm(forms.ModelForm):
    leave_type = forms.ChoiceField(choices=LEAVE_TYPE_CHOICES,widget=forms.RadioSelect())
    # leave_status = forms.ChoiceField(choices=LEAVE_STATUS_CHOICES,widget=forms.RadioSelect())
    class Meta:
        model = LeavePlannerModel
        fields = ['leave_type','leave_startdate','leave_enddate','leave_reason']
        widgets = {
            'leave_startdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'leave_enddate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'leave_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))

    class Meta:
        models = User
        fields = ['old_password', 'new_password1', 'new_password2']