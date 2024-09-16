from django.db import models
from django.contrib.auth.models import User


#This is subject model

class AddSubject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.subject_name

#This is Add Batch model

class AddBatch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=100)
    batch_faculty = models.CharField(max_length=100)
    batch_startdate = models.DateField()
    batch_starttime = models.TimeField()
    batch_endtime = models.TimeField()
    batch_subjects = models.ManyToManyField(AddSubject)
    
    
    def __str__(self):
        return f"{self.batch_name} - ({self.batch_starttime} - {self.batch_endtime})"
    
    
    def get_subjects(self):
        return "".join([str(s) for s in self.batch_subjects.all()])



#Add Student Model which is connect to the user model abd Add Batch model



class AddStudent(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT,primary_key=True)
    student_id = models.CharField(max_length=100,unique=True)
    student_batch = models.ForeignKey(AddBatch,on_delete=models.SET_NULL,null=True,blank=True)
    student_name = models.CharField(max_length=100)
    student_number = models.PositiveIntegerField()
    student_gender = models.CharField(max_length=100)
    student_dob = models.DateField()
    student_address = models.CharField(max_length=300)
    student_image = models.ImageField(upload_to='profile_image',blank=True)
    student_status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student_batch.batch_name} - ({self.student_batch.batch_starttime} - {self.student_batch.batch_endtime})"


    def __str__(self):
        return self.student_name
    

    @property
    def username(self):
        return self.user.username if self.user else 'No User'
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_tokan = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    





class Attendence(models.Model):
    name = models.CharField(max_length=100)
    I = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100,default=True)
    subject = models.CharField(max_length=100)

    


class Batch_message(models.Model):
    batch = models.ForeignKey(AddBatch, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='batch_files/', blank=True, null=True)

    def __str__(self):
        return self.batch.batch_name
    

class Announcement(models.Model):
    announcement_image = models.ImageField(upload_to='Evenet_Img',blank=True)
    announcement = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)



# //Leave Planner
class LeavePlannerModel(models.Model):
    student = models.ForeignKey(AddStudent, on_delete=models.CASCADE, null=True, blank=True)
    student_name = models.CharField(max_length=250)
    leave_type = models.CharField(max_length=100)
    leave_startdate = models.DateField()
    leave_enddate = models.DateField()
    leave_reason = models.CharField(max_length=100)
    leave_status = models.CharField(max_length=100,default='Pending')

    def __str__(self):
        return f"{self.student_name} - {self.leave_type} from {self.leave_startdate} to {self.leave_enddate}"
    
TASK_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
)

class Task(models.Model):
    date = models.DateField()
    description = models.TextField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    task_status = models.CharField(max_length=100,default='Pending',choices=TASK_STATUS_CHOICES,)
    
    def __str__(self):
        return f"{self.date}: {self.description}"
    
    def __str__(self):
        return f"{self.task_status}"