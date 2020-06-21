from django.shortcuts import render
from first.models import Register
from first.models import Active
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json
import datetime
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your views here.
def reg(request):
    if request.method == 'POST':
        mail=request.POST.get('email')
        user=Register.objects.filter(email=mail)
        print(user)
        if(len(user)>0):
            s='Email is Already Registered'
            return render(request,'newlogin.html',{'s':s})
        else:
            pas=request.POST.get('pass')
            pas1=request.POST.get('pass1')
            if pas==pas1:
                reg=Register()
                reg.name= request.POST.get('name')
                reg.email= request.POST.get('email')
                reg.password= request.POST.get('pass')
                reg.gender= request.POST.get('gender')
                reg.coun= request.POST.get('country')
                reg.img= request.POST.get('avatar')
                reg.save()
                return redirect(login)
            else:
                p='Passwords Do not Match'
                return render(request,'newlogin.html',{'s':p})
    else:
        return render(request,'newlogin.html')

def forgot(request):
	c = False
	if request.method=='POST':
		mail=request.POST.get('email')
		user=Register.objects.filter(email=mail)
		if(len(user)>0):
			c = True
			s='Your Password has been mailed. Please check your Inbox.'
		else:
			s='No user with given email found!!'
			c = True
		return render(request,'forgot.html',{'s':s, 'c':c})
	else:
		return render(request, 'forgot.html',{'c':c})


def logout(request):
	uname=request.session['s_name']
	# print(uname)
	act = Active.objects.filter(email=uname)
	now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
	act.update(date=now)
	act.update(status='Offline')
	del request.session['s_name']
	return redirect(login)

def login(request):
	if request.method =='POST':
		formpost=True
		username=request.POST.get('email')
		password=request.POST.get('password')
		errormsg=""
		cred=Register.objects.filter(email=username,password=password)
		k=len(cred)
		# print(cred)
		if k>0:
			# print("Valid")
			request.session['s_name']=username
			user=Active.objects.filter(email=username)
			n = cred[0].name
			# print(n)
			if(len(user)>0):
				act = Active.objects.filter(email=username)
				act.email = username
				now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
				act.update(date=now)
				act.update(status='Online')
			else:
				act=Active()
				act.email=username
				now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
				# time=now.time
				act.date=now
				act.name = n
				act.status='Online'
				act.save()
			return redirect(dashboard)
		else:
			print("Invalid Credentials")
			errormsg="Invalid Credentials"
			return render(request,"newlogin.html",{'formpost':formpost})
	else:
		formpost=False
		return render(request,"newlogin.html",{'formpost':formpost})


def dashboard(request):
	if not request.session.has_key('s_name'):
		return redirect(error)
	else:
		cp=Register.objects.get(email=request.session['s_name'])
		u=cp.name
		all_entries = Active.objects.filter(status='Online')
		allon = Active.objects.values('name','email','status' ).filter(status='Online')
		allof = Active.objects.values('name','email', 'date', 'status').filter(status='Offline')
		return render(request,'dashboard.html',{'user':all_entries,'n':u,'alln':allon, 'allf':allof})
def error(request):
	return render(request,'error.html')

