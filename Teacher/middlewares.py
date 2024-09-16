from .models import AddStudent
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


def my_middleware(get_response):
	def middleware_function(request):
		if request.user.is_authenticated:
			try:
				student = AddStudent.objects.get(user = request.user)
				if student.student_status == "Drop_out":
					logout(request)
					return redirect(reverse('account_locked'))
			except AddStudent.DoesNotExist:
				pass
		response = get_response(request)
		return response
	return middleware_function