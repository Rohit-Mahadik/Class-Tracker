import django.db.models
from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from .forms import AddSubjectForm,AddBatchForm,StudentCreationForm,StudentDataForm,LoginForm,Batch_message_form,Announcement_form,edit_profile_user_form,TaskForm,edit_profile_addstudent_form,LeaveApplicationForm,PasswordChangingForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from .models import AddBatch, AddStudent, AddSubject, Announcement, Attendence,Batch_message,LeavePlannerModel,Task,Profile
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from datetime import date
from .helpers import send_forget_password_mail,send_mail_user
import uuid
# Create your views here.


def account_locked(request):
    return render(request,"Teacher/account_locked.html")



def access_denied(request):
    return render(request,"Teacher/access_denied.html")



def navbar(request):
    if request.user.is_authenticated:
        return render(request,'Teacher/navbar.html',)




def add_subject(request):

    if request.user.is_authenticated and request.user.is_superuser == True:

        stud_data = AddStudent.objects.get(user=request.user)

        allsub=None

        if request.method == "POST":

            form = form = AddSubjectForm(request.POST)

            if form.is_valid():

                sub=form.save(commit=False)

                mydata = AddSubject.objects.filter(subject_name__iexact=sub.subject_name)

                if(mydata):

                    messages.error(request,"Subject already exists")

                else:

                    messages.success(request,"Subject Added Successfully")

                    sub.save()

                    form = AddSubjectForm() 

                allsub=AddSubject.objects.all()

            else:

                allsub=AddSubject.objects.all()

        else:

            form = AddSubjectForm()

            allsub=AddSubject.objects.all()

    else:

        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")

        return redirect('access_denied')

    return render(request,"Teacher/addsubject.html",{'form':form, 'sub':allsub, 'stud_data':stud_data, 'name':request.user})













def updatesubject(request,id):

    if request.user.is_authenticated and request.user.is_superuser == True:

        stud_data = AddStudent.objects.get(user=request.user)

        if request.method == 'POST':

            subject = AddSubject.objects.get(subject_id=id)

            form = AddSubjectForm(request.POST,instance=subject)

            if form.is_valid():

                sub=form.save(commit=False)

                mydata = AddSubject.objects.filter(subject_name__iexact=sub.subject_name)

                if(mydata):

                    allsub = AddSubject.objects.all()

                    messages.error(request,"Subject already exists")

                else:

                    sub.save()

                    messages.success(request,"Subject Updated Successfully")

                    allsub = AddSubject.objects.all()

                    return redirect('addsubject')

            else:

                messages.error(request,"Invalid Form")

        else:

            subject = AddSubject.objects.get(subject_id=id)

            form = AddSubjectForm(instance=subject)

            allsub = AddSubject.objects.all()

    else:

        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")

        return redirect('access_denied')

    return render(request,"Teacher/addsubject.html",{'form':form, 'sub':allsub, 'stud_data':stud_data, 'name':request.user,})
    
    



def delete_subject(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method=="POST":
            pi=AddSubject.objects.get(subject_id=id)
            pi.delete()
            messages.success(request,"Subject Deleted Successfully")
            return redirect('addsubject')
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect('access_denied')






def add_batch(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        if request.method == "POST":
            form = form = AddBatchForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Batch Added successfully")
                return redirect('addbatch')
        else:
            form = AddBatchForm()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect('access_denied')
    return render(request,"Teacher/addbatch.html",{'form':form, 'stud_data':stud_data, 'name':request.user,})




def update_batch(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        if request.method == 'POST':
            batch = AddBatch.objects.get(batch_id=id)
            form = AddBatchForm(request.POST,instance=batch)
            if form.is_valid():
                form.save()
                messages.success(request,"Batch Updated Successfully")
                return redirect('showbatch')
        else:
            batch = AddBatch.objects.get(batch_id=id)
            form = AddBatchForm(instance=batch)
            allbatch = AddBatch.objects.all()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect('access_denied')
    return render(request,"Teacher/addbatch.html",{'form':form,'batch':allbatch, 'stud_data':stud_data, 'name':request.user,})




def delete_batch(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method=="POST":
            pi=AddBatch.objects.get(batch_id=id)
            pi.delete()
            messages.success(request,"Batch Deleted Successfully")
            return redirect('showbatch')
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect('access_denied')



def add_student(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        if request.method == 'POST':
            form1 = StudentCreationForm(request.POST)
            form2 = StudentDataForm(request.POST, request.FILES)
            email = request.POST.get("email")
            student_login_name = request.POST.get("username")
            
            if form1.is_valid() and form2.is_valid():
                user = form1.save()
                student = form2.save(commit=False)
                student.user = user
                student.save()
                send_mail_user(email,student_login_name)
                messages.success(request,"Student Add Successfully")
                form1 = StudentCreationForm()
                form2 = StudentDataForm()

        else:
            form1 = StudentCreationForm()
            form2 = StudentDataForm()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect('access_denied')
    return render(request,"Teacher/addstudent.html",{'form1':form1,'form2':form2, 'stud_data':stud_data, 'name':request.user,})




def view_all_student(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        StudentInfo=AddStudent.objects.all()[1::]
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/view_all_student.html",{"studInfo":StudentInfo, 'stud_data':stud_data, 'name':request.user,})



def update_stud(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        if request.method=="POST":
            pi=AddStudent.objects.get(student_id=id)
            form=StudentDataForm(request.POST,instance=pi)

            if form.is_valid():
                form.save()
                messages.success(request,"Student Updated Successfully")
                return redirect('viewallstudent')
        else:
            pi=AddStudent.objects.get(student_id=id)
            form=StudentDataForm(instance=pi)
            return render(request,"Teacher/updatestudent.html",{'fm':form,'stud_data':stud_data, 'name':request.user,})
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")


def delete_student(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method=="POST":
            pi=AddStudent.objects.get(student_id=id)
            pi.delete()
            messages.success(request,"Subject Deleted Successfully")
        return redirect('viewallstudent')
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")




def user_log(request):
    if request.method == 'POST':
        fm = LoginForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request, user)
                if request.user.is_superuser == True:
                    return HttpResponseRedirect("teacher/dashboardteacher")
                else:
                    return HttpResponseRedirect("student/dashboardstudent")
    else:
        fm = LoginForm()
    return render(request,"Teacher/loginpage.html",{'form':fm})
    



def user_logout(request):
    logout(request)
    return redirect('login')





def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        sum_stud = AddStudent.objects.all().count()-1
        sum_batch = AddBatch.objects.all().count()
        date = datetime.datetime.now().date()
        tasks = Task.objects.filter(date=date)
        batches = AddBatch.objects.all()
        announcement=Announcement.objects.all()
        return render(request,'Teacher/admin_dashboard.html',{'name':request.user,'stud_data':stud_data,'sum_stud':sum_stud,'sum_batch':sum_batch,'tasks': tasks,'batches':batches,'announcement':announcement})
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")




def show_batch(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        if request.user.is_authenticated and request.user.is_superuser == True:
            batches = AddBatch.objects.all()
            return render(request,'Teacher/showbatch.html',{'batches':batches, 'name':request.user,'stud_data':stud_data})
        else:
            return render(request,"Teacher/loginpage.html")
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")


def show_batch_students(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        batch = get_object_or_404(AddBatch,batch_id=id)
        students = AddStudent.objects.filter(student_batch=batch)
        batchid = AddBatch.objects.filter(batch_id=id)
        xyz = []
        for i in students:
            if i.student_status =='Active':
                xyz.append(i)
            else:
                print("Inactive")

        return render(request,'Teacher/showbatch_student.html',{'students':xyz , 'batchid':batchid, 'name':request.user,'stud_data':stud_data})
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")




def take_attendance(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        if request.method == "POST":
            batch_sub = AddSubject.objects.filter(addbatch__batch_id=id)
            students = AddStudent.objects.filter(student_batch=id)
            
            
            for i in students:
                selected_subject = request.POST.get('subjects')
                attendance_data = request.POST.get(i.student_id)
                
                if selected_subject == "Select Ongoing Subject":
                    messages.success(request,"Please Select Subject")
                    return redirect("takeattendance",id=id)
                elif attendance_data:
                    Attendence.objects.update_or_create(name=i.student_name, I=i.student_id,date=date.today(),defaults={'status':attendance_data},subject=selected_subject)
            return redirect('showbatch') 

        else:
        
            batch_sub = AddSubject.objects.filter(addbatch__batch_id=id)
            students = AddStudent.objects.filter(student_batch=id)
            return render(request, "Teacher/takeattendance.html", {'batch_sub': batch_sub, 'students': students, 'name':request.user,'stud_data':stud_data})
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")





def view_attendance_teacher(request):
    if request.user.is_authenticated and request.user.is_superuser == True:
        stud_data = AddStudent.objects.get(user=request.user)
        subjects = AddSubject.objects.all()
        stud_attendance = None
        stud_attendance_id = None
        stud_attendance_id_count_present = 0
        stud_attendance_count_present = 0
        stud_attendance_id_count_absent = 0
        stud_attendance_count_absent = 0

        student=request.POST.get('student-name')
        subject = request.POST.get('subject')

        # print(student)
        if request.method == 'POST':
            stud_name = AddStudent.objects.filter(student_name__iexact = student).count()
            if stud_name > 1:
                messages.warning(request,"There are multiple student with this name kindly search with student id")
            else:
                if subject == "select subject":
                    stud_attendance_id= Attendence.objects.filter(I__iexact=student)
                    stud_attendance = Attendence.objects.filter(name__iexact=student)

                    stud_attendance_id_count_present= Attendence.objects.filter(I__iexact=student, status="Present").count()
                    stud_attendance_count_present = Attendence.objects.filter(name__iexact=student, status="Present").count()

                    stud_attendance_id_count_absent= Attendence.objects.filter(I__iexact=student, status="Absent").count()
                    stud_attendance_count_absent = Attendence.objects.filter(name__iexact=student, status="Absent").count()
                    
                    
                else:
                    stud_attendance_id= Attendence.objects.filter(I__iexact=student,subject=subject)
                    stud_attendance = Attendence.objects.filter(name__iexact=student,subject=subject)

                    stud_attendance_id_count_present= Attendence.objects.filter(I__iexact=student, subject=subject, status="Present").count()
                    stud_attendance_count_present = Attendence.objects.filter(name__iexact=student, subject=subject, status="Present").count()

                    stud_attendance_id_count_absent= Attendence.objects.filter(I__iexact=student, subject=subject, status="Absent").count()
                    stud_attendance_count_absent = Attendence.objects.filter(name__iexact=student, subject=subject, status="Absent").count()
                    
                    
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/view_attendance_teacher.html",{'stud_attendance':stud_attendance,'stud_attendance_id':stud_attendance_id,'subjects':subjects, 'name':request.user,'stud_data':stud_data,'stud_attendance_id_count_present':stud_attendance_id_count_present , 'stud_attendance_count_present':stud_attendance_count_present, 'stud_attendance_id_count_absent':stud_attendance_id_count_absent, 'stud_attendance_count_absent':stud_attendance_count_absent})




def batch_message(request):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        d = None
        if request.method == "POST":
            form = Batch_message_form(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                form=Batch_message_form()
                batches = AddBatch.objects.all()
                messages.success(request,"Assignment Submit Successfully")          
        else:
            form=Batch_message_form()
            batches = AddBatch.objects.all()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/assignment.html",{'form':form, 'batches':batches, 'name':request.user,'stud_data':stud_data})




# view perticular assignment
def ViewAPerticularAssignment(request,id):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        batches = AddBatch.objects.get(batch_id=id)
        form = Batch_message.objects.filter(batch_id = id)
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request, 'Teacher/assignmentData.html',{'batches':batches, 'form':form, 'name':request.user,'stud_data':stud_data})



# update Assignment
def UpdateAssignment(request, id):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method=="POST":
            pi=Batch_message.objects.get(id=id)
            form=Batch_message_form(request.POST,request.FILES,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"Assignment Update Successfully")
                batches = AddBatch.objects.all()
                return redirect('sendmessage')
            else:
                messages.error(request,"Error")
        else:
            pi=Batch_message.objects.get(id=id)
            form=Batch_message_form(instance=pi)
            batches = AddBatch.objects.all()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/assignment.html",{"form":form,'batches':batches, 'name':request.user,'stud_data':stud_data})



# delete Assignment
def DeleteAssignment(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            pi=Batch_message.objects.get(id=id)
            pi.delete()
            messages.success(request,"Assignment Deleted Successfully")
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return redirect('sendmessage')



# Announcement part
def make_announcement(request):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        d=None
        if request.method == "POST":
            form = Announcement_form(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                form=Announcement_form()
                d = Announcement.objects.all()
                messages.success(request,"Announcement Send Successfully")
        else:
            form=Announcement_form()
            d = Announcement.objects.all()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/makeannouncement.html",{'form':form,'d':d, 'name':request.user,'stud_data':stud_data})




# update Announcement
def UpdateMessage(request, id):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method=="POST":
            pi=Announcement.objects.get(id=id)
            form=Announcement_form(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"Announcement Update Successfully")
                allanno = Announcement.objects.all()
                return redirect('makeannouncement')
            else:
                messages.error(request,"Error")
        else:
            pi=Announcement.objects.get(id=id)
            form=Announcement_form(instance=pi)
            allanno = Announcement.objects.all()
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/makeannouncement.html",{"form":form, 'd':allanno, 'name':request.user,'stud_data':stud_data})



# delete Announcement
def DeleteMessage(request, id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            pi=Announcement.objects.get(id=id)
            pi.delete()
            messages.success(request,"Announcement Deleted Successfully")
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return redirect('makeannouncement')



def edit_user_profile(request):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            pi=AddStudent.objects.get(user=request.user)
            fm = edit_profile_user_form(request.POST,instance=request.user)
            fm1 = edit_profile_addstudent_form(request.POST,request.FILES,instance=pi)
            if fm.is_valid() and fm1.is_valid():
                fm.save()
                fm1.save()
                messages.success(request,"Profile Updated Successfully")
                return redirect('editadminprofile')
        else:
            pi=AddStudent.objects.get(user=request.user)
            fm = edit_profile_user_form(instance=request.user)
            fm1 = edit_profile_addstudent_form(instance=pi)
    else:
        return redirect("access_denied")
    return render(request,"Teacher/editadminprofile.html",{'form1':fm,'form2':fm1, 'name':request.user,'stud_data':stud_data})




# admin change password

def adminPasswordChange(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            stud_data = AddStudent.objects.get(user=request.user)
            if request.method == "POST":
                form = PasswordChangingForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  
                    messages.success(request, 'Your password was successfully updated!')    
            else:
                form = PasswordChangingForm(request.user)
            return render(request,'Teacher/password_change.html',{'form':form, 'name':request.user,'stud_data':stud_data})
        else:
            return redirect('login')
    else:   
        return redirect('login')
        



def search_student(request):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
            if request.method == "POST":
                search = request.POST.get('search')
                if search == "":
                    student = AddStudent.objects.all()[1::]
                    messages.info(request,"Please Enter Student Name")
                else:
                    student = AddStudent.objects.filter(student_name__icontains=search)
            else:
                student=AddStudent.objects.all()[1::]
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    return render(request,"Teacher/view_all_student.html",{'student':student, 'name':request.user,'stud_data':stud_data})




# Leave Application From Admin Views
def all_leave_application(request):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        Leave_data = LeavePlannerModel.objects.all()

        return render(request,'Teacher/all_leave_application.html',{'application':Leave_data, 'name':request.user,'stud_data':stud_data})
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")
    



# //Leave Application form
def leave_application_form(request,id):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        pi=LeavePlannerModel.objects.get(id=id)
        if request.method=='POST':
            form=LeaveApplicationForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                return redirect('leaveapplication') 

        else:
            form=LeaveApplicationForm(instance=pi)

        return render(request,'Teacher/leave_application_form.html',{'fm':form, 'name':request.user,'stud_data':stud_data})
    else:
        messages.success(request,"YOU DON'T HAVE AN ACCESS TO MANAGE THIS AUTHERITY")
        return redirect("access_denied")





def delete_levae(request,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            pi=LeavePlannerModel.objects.get(id=id)
            pi.delete()
    else:
        return redirect("access_denied")
    return redirect('leaveapplication')




def announcement_detail(request,id):
    announcement= Announcement.objects.get(id=id)
    print(announcement)
    return render(request,'Teacher/announcement_detail.html',{'announcement':announcement})





def task_for_date(request, date):
    try:
        tasks = Task.objects.filter(date=date)  # Adjust this query as needed
        tasks_list = [
            {
                'id': task.id,
                'description': task.description,
                'starttime': task.starttime,
                'endtime': task.endtime,
                'task_status': task.task_status,
            } for task in tasks
        ]
        return JsonResponse({'tasks': tasks_list,})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)





def add_task(request):
    stud_data = AddStudent.objects.get(user=request.user)
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboardteacher')
        else:
            form = TaskForm()
        return render(request, 'Teacher/add_task.html', {'form': form, 'name':request.user,'stud_data':stud_data})
    else:
        return redirect("access_denied")




def update_task(request,id):
    stud_data = AddStudent.objects.get(user=request.user)
    task = Task.objects.get(id=id)
    print(task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboardteacher')
    else:
        form = TaskForm(instance=task)
    return render(request, 'Teacher/add_task.html', {'form': form, 'name':request.user,'stud_data':stud_data})






def forget_change_password(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_tokan = token).first()
        context = {'user_id':profile_obj.user.id}
        if request.method == 'POST':
            new_password = request.POST.get("new-password")
            confirm_password = request.POST.get("confirm-password")
            user_id = request.POST.get("user_id")
            
            if user_id is None:
                messages.success(request,"No user id found")
                return redirect(f'forgetchangepassword/<token>/')
            
            if new_password != confirm_password:
                messages.success(request,"Password not match")
                return redirect(f'forgetchangepassword/<token>/')
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect("/") 

        

    except Exception as e:
        print(e)
    return render(request,"Teacher/forgot_change_pass.html",context=context)




def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request,"User Not Found")
                return redirect('/login/')
            
            user_obj = User.objects.get(username=username)
            # print(user_obj)
            token = str(uuid.uuid4())
            profile_obj,created_at = Profile.objects.get_or_create(user=user_obj)

            profile_obj.forget_password_tokan = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request,"An email is send")
            return redirect('user_log')

    except Exception as e:
        print(e)
    return render(request,"Teacher/forgot_pass_email.html")




from django.views.decorators.http import require_POST
@require_POST
def delete_task(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        task = get_object_or_404(Task, id=id)
        task.delete()
        return JsonResponse({'success': True})  # Return a JSON response indicating success
    else:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)




def today_task_delete(request ,id):
    if request.user.is_authenticated and request.user.is_superuser == True:
        if request.method == "POST":
            pi=Task.objects.get(id=id)
            pi.delete()
        return redirect('dashboardteacher')
    else:
        return redirect("access_denied")