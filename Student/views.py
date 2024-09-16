from django.shortcuts import render,redirect
from Teacher.models import Attendence,AddStudent,Batch_message,Announcement,LeavePlannerModel
from .forms import Edit_profile_form,Edit_username_form,LeavePlannerForm,PasswordChangingForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date,timedelta
from django.db.models import Q
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import login_required
# Create your views here.



def dashboard(request):
	if request.user.is_authenticated:
		if not request.user.is_superuser:
			stud_data = AddStudent.objects.get(user=request.user)
			naam = AddStudent.objects.get(student_name = stud_data)
			jan =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=1) & Q(name = naam)).count()
			feb =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=2) & Q(name = naam)).count()
			mar =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=3) & Q(name = naam)).count()
			apr =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=4) & Q(name = naam)).count()
			may =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=5) & Q(name = naam)).count()
			jun =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=6) & Q(name = naam)).count()
			jul =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=7) & Q(name = naam)).count()
			aug =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=8) & Q(name = naam)).count()
			sep =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=9) & Q(name = naam)).count()
			oct =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=10) & Q(name = naam)).count()
			nov =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=11) & Q(name = naam)).count()
			dec =Attendence.objects.annotate(month=ExtractMonth('date')).filter(Q(month=12) & Q(name = naam)).count()

			months = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December']

			months_counts = [jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec]

			announcement=Announcement.objects.all()

			user_batch = AddStudent.objects.get(user__username=request.user).student_batch

			assignment = Batch_message.objects.filter(batch=user_batch).order_by('-created_at')[:2]

			email=User.objects.get(username=request.user)

			batch=str(stud_data.student_batch).split('-')

			return render(request,'Student/student_dashboard.html',{'name':request.user,'stud_data':stud_data,'announcement':announcement,'months':months,'months_counts':months_counts,'assignment':assignment,'email':email,'batch':batch[0]})
		else:
			return redirect('login')
	else:
		return redirect('login')



def view_attendance(request):
	if request.user.is_authenticated:
		if not request.user.is_superuser:
			stud_data = AddStudent.objects.get(user=request.user)
			user_name = AddStudent.objects.get(user__username=request.user).student_name
			year = request.POST.get('year')
			month = request.POST.get('month')
			attendance = Attendence.objects.filter(name=user_name, date__year=year, date__month=month)
			attendance_count_present = Attendence.objects.filter(name=user_name, date__year=year, date__month=month,status="Present").count()
			attendance_count_absent = Attendence.objects.filter(name=user_name, date__year=year, date__month=month,status="Absent").count()
			return render(request,"Student/student_view_attendance.html",{'user_name':user_name,'attendance':attendance,'attendance_count_present':attendance_count_present,'attendance_count_absent':attendance_count_absent, 'name':request.user,'stud_data':stud_data})
		else:
			return redirect('login')
	else:
		return redirect('login')




def view_assignments(request):
	if request.user.is_authenticated:
		if not request.user.is_superuser:
			stud_data = AddStudent.objects.get(user=request.user)
			user_batch = AddStudent.objects.get(user__username=request.user).student_batch
			ass = Batch_message.objects.filter(batch=user_batch).order_by('-created_at')
			if len(ass)>0:
				first=ass = Batch_message.objects.filter(batch=user_batch).order_by('-created_at')[0]
				all=ass = Batch_message.objects.filter(batch=user_batch).order_by('-created_at')[1::]
			else:
				first=False
				all=False

			return render(request,"Student/viewassignments.html",{'userbatch':user_batch,'recent_assgn':first,'ass':all, 'name':request.user,'stud_data':stud_data})
		else:
			return redirect('login')
	else:
		return redirect('login')





def view_announcements(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            stud_data = AddStudent.objects.get(user=request.user)
            announcement = Announcement.objects.all().order_by('-created_at')
            if len(announcement):
                latest_announcement = Announcement.objects.all().order_by('-created_at')[0]
                announcement = Announcement.objects.all().order_by('-created_at')[1:]
            else:
                latest_announcement = False
                announcement= False

            return render(request,"Student/viewannouncement.html",{'latest_announcement':latest_announcement,'announcement':announcement,'name':request.user,'stud_data':stud_data})
        else:
            return redirect('login')
    else:
        return redirect('login')



def edit_profile(request):
	if request.user.is_authenticated:
		if not request.user.is_superuser:
			stud_data = AddStudent.objects.get(user=request.user)
			if request.method == "POST":
				pi=AddStudent.objects.get(user=request.user)
				
				form1 = Edit_profile_form(request.POST,request.FILES,instance=pi)
				
				form2=Edit_username_form(request.POST, instance=request.user)

				if form1.is_valid() and form2.is_valid():
					form1.save()
					form2.save()
					messages.success(request,"Profile Update Successfully")
					return redirect('editprofile')
				
			else:
				pi=AddStudent.objects.get(user=request.user)
				form1 = Edit_profile_form(instance=pi)
				form2=Edit_username_form(instance=request.user)
			return render(request,'Student/edit_profile.html',{'fm':form1,'fm1':form2, 'name':request.user,'stud_data':stud_data})
		else:
			# messages.error("Please Login")
			return redirect('login')
	else:
		return redirect('login')




# Student change password

def PasswordChange(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            stud_data = AddStudent.objects.get(user=request.user)
            if request.method == "POST":
                form = PasswordChangingForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  
                    messages.success(request, 'Your password was successfully updated!')    
            else:
                form = PasswordChangingForm(request.user)
            return render(request,'Student/password_change.html',{'form':form, 'name':request.user,'stud_data':stud_data})
        else:
            return redirect('login')
    else:   
        return redirect('login')
	



#Leave Planner Views from student_views

def leave_planner(request):
	if request.user.is_authenticated:
		if not request.user.is_superuser:
			stud_data = AddStudent.objects.get(user=request.user)
			if request.method == "POST":
				form=LeavePlannerForm(request.POST)
				if form.is_valid():
					Leave_Application=form.save(commit=False)
					Leave_Application.student=AddStudent.objects.get(user=request.user)
					Leave_Application.student_name=Leave_Application.student
					Leave_Application.save()
					messages.success(request,"Your Leave Application Submitted Successfully")
					form=LeavePlannerForm()
					Leave__stud_name=AddStudent.objects.get(user=request.user)
					Leave_data=LeavePlannerModel.objects.filter(student_name=Leave__stud_name)

			else:
				form=LeavePlannerForm()
				Leave__stud_name=AddStudent.objects.get(user=request.user)
				Leave_data=LeavePlannerModel.objects.filter(student_name=Leave__stud_name)
			return render(request,'Student/leave_planner.html',{'fm':form,'application':Leave_data, 'name':request.user,'stud_data':stud_data})
		else:
			return redirect('login')
	else:
		return redirect('login')