from django import forms
import django.db
from .models import AddSubject,AddBatch,AddStudent,Batch_message,Announcement,LeavePlannerModel,Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,UserChangeForm,PasswordChangeForm


#This is Add subject form

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = AddSubject
        fields = ['subject_name']
        widgets = {'subject_name':forms.TextInput(attrs={'autofocus':True , 'class': 'form-control'})}


#This is Add Batch form

class AddBatchForm(forms.ModelForm):
    batch_subjects = forms.ModelMultipleChoiceField(
        queryset=AddSubject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = AddBatch
        fields = ['batch_name','batch_faculty' ,'batch_startdate','batch_starttime','batch_endtime','batch_subjects']
        widgets = {'batch_name':forms.TextInput(attrs={'class':'form-control'}),
             'batch_faculty':forms.TextInput(attrs={'class':'form-control','rows':4}),
             'batch_startdate':forms.DateInput(attrs={'class':'form-control','type':'date'}),
             'batch_starttime':forms.TimeInput(attrs={'class':'form-control','type':"time"}),
             'batch_endtime':forms.TimeInput(attrs={'class':'form-control','type':"time"}),
             }
        

        

#This is User Form 

class StudentCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','value':'Aptech@123'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','value':'Aptech@123'}))
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.', widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'password1':'pass'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    

#This is Add Student form

GENDER_CHOICES = [
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
]

STUDENT_STATUS_CHOICES = (
    ('Active','Active'),
    ('Completed','Completed'),
    ('Drop_out','Drop_out'),
)



class StudentDataForm(forms.ModelForm):
    student_gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect())
    student_status = forms.ChoiceField(choices=STUDENT_STATUS_CHOICES,widget=forms.RadioSelect())
    class Meta:
        model = AddStudent
        fields = ['student_id','student_batch','student_name','student_number','student_gender','student_status','student_dob','student_image','student_address']
        widgets = {'student_batch':forms.Select(attrs={'class':'form-control'}),
             'student_address':forms.Textarea(attrs={'class':'form-control','rows':4,'cols':10}),
             'student_dob':forms.DateInput(attrs={'class':'form-control','type':'date'}),
             'student_number':forms.NumberInput(attrs={'class':'form-control'}),
             'student_name':forms.TextInput(attrs={'class':'form-control'}),
             'student_id':forms.TextInput(attrs={'class':'form-control'}),
             'student_status':forms.Select(attrs={'class':'form-control'}),
             }
        labels = {'student_number':'Student Contact Number',}



#This is Login Form

class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True , 'class': 'form-control','placeholder':'Username'}))
    password=forms.CharField(label='password',strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password' , 'class': 'form-control mt-3','placeholder':'Password'}))




# This is Batch message form

class Batch_message_form(forms.ModelForm):
    class Meta:
        model = Batch_message
        fields = ['batch','message','file']
        widgets = {'batch':forms.Select(attrs={'class':'form-control'}),
             'message':forms.Textarea(attrs={'class':'form-control','rows':4})}


class Announcement_form(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['announcement_image','announcement']
        widgets = {'announcement':forms.Textarea(attrs={'class':'form-control'})}


class edit_profile_user_form(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
             'first_name':forms.TextInput(attrs={'class':'form-control','rows':4,'cols':10}),
             'last_name':forms.TextInput(attrs={'class':'form-control'}),
             'email':forms.EmailInput(attrs={'class':'form-control'}),
             'username':forms.TextInput(attrs={'class':'form-control'}),
             }


GENDER_CHOICES = [
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
]

STUDENT_STATUS_CHOICES = (
    ('Active','Active'),
    ('Completed','Completed'),
    ('Drop_out','Drop_out'),
)

class edit_profile_addstudent_form(forms.ModelForm):
    student_gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect())
    student_status = forms.ChoiceField(choices=STUDENT_STATUS_CHOICES,widget=forms.RadioSelect())
    class Meta:
        model = AddStudent
        fields = ['student_id','student_batch','student_name','student_number','student_gender','student_status','student_dob','student_image','student_address']
        widgets = {'student_batch':forms.Select(attrs={'class':'form-control'}),
             'student_address':forms.Textarea(attrs={'class':'form-control','rows':4,'cols':10}),
             'student_dob':forms.DateInput(attrs={'class':'form-control','type':'date'}),
             'student_number':forms.NumberInput(attrs={'class':'form-control'}),
             'student_name':forms.TextInput(attrs={'class':'form-control'}),
             'student_id':forms.TextInput(attrs={'class':'form-control'}),
             'student_status':forms.Select(attrs={'class':'form-control'}),
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


class LeaveApplicationForm(forms.ModelForm):
    leave_type = forms.ChoiceField(choices=LEAVE_TYPE_CHOICES,widget=forms.RadioSelect())
    leave_status = forms.ChoiceField(choices=LEAVE_STATUS_CHOICES,widget=forms.RadioSelect())

    class Meta:
        model = LeavePlannerModel
        fields = ['leave_type','leave_startdate','leave_enddate','leave_reason','leave_status']
        widgets = {
            'leave_startdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'leave_enddate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'leave_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



        
class TaskForm(forms.ModelForm):
    # task_status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Task
        fields = ['date', 'description','starttime','endtime','task_status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date','class': 'form-control',}),
            'description':forms.Textarea(attrs={'class': 'form-control',}),
            'starttime': forms.TimeInput(attrs={'type': 'time','class': 'form-control',}),
            'endtime': forms.TimeInput(attrs={'type': 'time','class': 'form-control',}),
        }



class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))

    class Meta:
        models = User
        fields = ['old_password', 'new_password1', 'new_password2']