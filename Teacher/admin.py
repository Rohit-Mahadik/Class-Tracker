from django.contrib import admin
from .models import AddSubject,AddBatch,AddStudent,Attendence,Batch_message,Announcement,Task,Profile

# Register your models here.

@admin.register(AddSubject)
class AddSubjectAdmin(admin.ModelAdmin):
	list_display = ['subject_id','subject_name']



@admin.register(AddBatch)
class AddBatchAdmin(admin.ModelAdmin):
	list_display = ['batch_id','batch_name','batch_faculty' ,'batch_startdate','batch_starttime','batch_endtime','get_subjects']



@admin.register(AddStudent)
class AddStudentAdmin(admin.ModelAdmin):
	list_display = ['student_id','student_batch','student_name','student_number','student_address','student_dob','student_image']



@admin.register(Attendence)
class AttendenceAdmin(admin.ModelAdmin):
	list_display = ['name','I','date','status','subject']


@admin.register(Batch_message)
class Batch_messageAdmin(admin.ModelAdmin):
	list_display = ['batch','file','message','created_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ['announcement_image','announcement','created_at']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ['date','starttime','endtime','task_status']


admin.site.register(Profile)