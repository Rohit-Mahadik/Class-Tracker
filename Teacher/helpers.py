
#helpers.py
from django.core.mail import send_mail
import uuid
from django.conf import settings



def send_forget_password_mail(email, token):
	subject = 'Your Forget Password Link'
	message = f'Hi Click On The link to reset your password http://{settings.DOMAIN}/teacher/forgetchangepassword/{token}/'
	email_from =  settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject,message,email_from,recipient_list,fail_silently=False,)
	return True


def send_mail_user(email,student_login_name):
	subject = 'Class Tracker Login Link'
	message = f'Welcome, {student_login_name} 🎉 \n Your registration was successful,and we are thrilled to welcome you to Class Tracker \n Username: {student_login_name}\n Password: Aptech@123 \n click here to log in http://{settings.DOMAIN}/ '
	email_from =  settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject,message,email_from,recipient_list,fail_silently=False,)
	return True




