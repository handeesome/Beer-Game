#import the django render library
from django.shortcuts import render

#import the django messages library
from django.contrib import messages

#import the class created in the models.py file
from SE.models import Instructor_Registration


'''
instructor_registration function uses the POST method to acquire the data
inputed in the registration form for the instructor.
'''
def instructor_registration(request):
	if request.method == 'POST':
		if (request.POST.get('FirstName') and request.POST.get('LastName') and
		    request.POST.get('Email') and request.POST.get('Password')):
				saverecord = Instructor_Registration()
				saverecord.FirstName = request.POST.get('FirstName')
				saverecord.LastName = request.POST.get('LastName')
				saverecord.Email = request.POST.get('Email')
				saverecord.Password = request.POST.get('Password')
				saverecord.save()
				messages.success(request, "Succesfully registered")
				return render(request, 'signup_instructor.html')
	else:
		return render(request, 'signup_instructor.html')

'''
These functions are used to render html pages as done by the href = '.html'
in HTML forms.
'''

#render the index.html page // used for the database 
def index(request):
	return render(request, 'index.html')

#render the index.html page // used for the home button
def goindex(request):
	return render(request, 'index.html')

#render the signup_instructor.html page
def ins_reg(request):
	return render(request, 'signup_instructor.html')

#render the instructor_login.html page
def ins_log(request):
	return render(request, 'instructor_login.html') 

#render the student_login.html page
def stu_log(request):
	return render(request, 'student_login.html') 

#render the signup_custom.html page
def cus_reg(request):
	return render(request, 'signup_custom.html')

#render the custom_login.html page
def cus_log(request):
	return render(request, 'custom_login.html') 
   

