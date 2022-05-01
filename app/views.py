from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
from sqlalchemy import all_, null

from django.http import HttpResponse

from template.settings import BASE_DIR
from .forms import *
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
import operator
import json

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

import base64
import os
import requests

piServerURL = "http://127.0.0.1:5000/test"
piServerURL2 = "http://127.0.0.1:5000/updateDB"

##########################################################

#                        AJAX

##########################################################

@api_view(('GET',))
def ajax_test(request):
    if(not request.user.is_authenticated or request.user.username=="demo_user"):
        context = {
            "message":"lol",
        }
        return Response(context, status=status.HTTP_200_OK)
    request_data = request.GET.get('notif_id')
    print("got notif_id : ",request_data)

    print(request.user.is_authenticated)
    print(request.user.username)
  
    context = {
        "message":"AJAX success",
    }
    return Response(context, status=status.HTTP_200_OK)

@api_view(('GET',))
def mark_present(request):
    stud_rno = request.GET.get('rno')
    print(stud_rno," -> marking present")
    return Response(status=status.HTTP_200_OK)

    from datetime import date
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    stud = student.objects.get(rno=stud_rno)
    stud_id = stud.s_no
    print(stud.name)

    try:
        f = record.objects.get(datee=d1)
        temp = f.presentStudents
        present_studs=temp.split('.')
        print(present_studs)
        print("class found, appending")

        f.presentStudents = f.presentStudents+'.'+str(stud_id)
        f.save()

    except:
        print("no class found, creating one")
        studentss = str(stud_id)
        f = record.objects.create(datee=d1, presentStudents=studentss)
        f.save()
  
    context = {
        "message":"success",
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(('GET',))
def attendance_for_date(request):
    datee = request.GET.get('datee')
    print("got date",datee)

    try:
        f = record.objects.get(datee=datee)
        temp = f.presentStudents
        present_studs=temp.split('.')
        # print(present_studs)
    except:
        print("invalid date or record not present in db")
        context = {
            "message":"no record found for date "+datee,
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    objekt = student.objects.order_by('rno')
    n = objekt.count()
    stud1 = []
    stud2 = []

    i=0
    for x in objekt:
        i+=1
        temp = {}
        temp["sno"]=i
        temp["rno"]=x.rno
        temp["name"]=x.name

        if str(x.s_no) in present_studs:
            # print(x.name)
            temp["attendance"] = "Present"
        else:
            temp["attendance"] = "Absent"

        temp["db"]=x.db

        if(i<n/2+1):
            stud1.append(temp)
        else:
            stud2.append(temp)

    context = {
        "message":"success",
        "stud1" : stud1,
        "stud2" : stud2,
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(('GET',))
def updateDB(request):
    if(not request.user.is_authenticated or request.user.username=="demo_user"):
        context = {
            "message":"lol",
        }
        return Response(context, status=status.HTTP_200_OK)
        
    f = student.objects.all()
    studs = []
    for x in f:
        if(x.db==False and x.img!=None):  #not in db
            studs.append(x.name)
            stud = student.objects.get(rno = x.rno)
            stud.db=True
            stud.save()
    print(studs)
    if(len(studs)>0):
        #call api to raspberry pi
        url = piServerURL2
        payload={}
        files={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        context = {
            "message":1,
            "names":studs,
        }
        return Response(context, status=status.HTTP_200_OK)

    context = {
        "message":0,
    }
    return Response(context, status=status.HTTP_200_OK)


##########################################################

#                        NOT AJAX

##########################################################

def loginPage(request):
    return render(request, "app/login.html")

def handLoginTeacher(request):
    logout(request)

    if request.method=="POST":
        user=request.POST['TeacherName']
        password=request.POST['teacherPass']
        print(user,password)
        user=authenticate(username= user, password= password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("teacher"))
        else:
            messages.info(request, 'Invalid credentials. Please try again!')
            return render(request,"app/login.html")
    messages.info(request, 'Not POST request!')
    return HttpResponseRedirect(reverse("loginPage"))

def handlogout(request):
    logout(request)
    messages.info(request, 'Logged out!')
    return HttpResponseRedirect(reverse("loginPage"))


def home(request):
    objekt = student.objects.order_by('rno')
    n = objekt.count()
    stud1 = []
    stud2 = []
    nonDBrNos = {}

    from datetime import date
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    # print(d1)
    present_studs = []
    try:
        f = record.objects.get(datee=d1)
        temp = f.presentStudents
        present_studs=temp.split('.')
        # print(present_studs)
    except:
        print("invalid date or record not present in db")
        present_studs = []
    
    i=0
    for x in objekt:
        i+=1
        temp = {}
        temp["sno"]=i
        temp["rno"]=x.rno
        temp["name"]=x.name

        if str(x.s_no) in present_studs:
            # print(x.name)
            temp["attendance"] = "Present"
        else:
            temp["attendance"] = "Absent"

        temp["db"]=x.db
        if(not x.db):
            nonDBrNos[x.rno] = x.name

        if(i<n/2+1):
            stud1.append(temp)
        else:
            stud2.append(temp)
        
    if len(present_studs)<=0:
        stud1 = []
        stud2 = []

    context = {
        "stud1" : json.dumps(stud1),
        "stud2" : json.dumps(stud2),
        "nonDBrNos" : json.dumps(nonDBrNos),
        "form" : ImageForm()
    }

    if request.method == "POST":
        rno=request.POST['browser']
        form = ImageForm(request.POST, request.FILES)
        if(not request.user.is_authenticated or request.user.username=="demo_user"):
            messages.info(request, "Not available for Demo user!")
            return HttpResponseRedirect(reverse("teacher"))
        if form.is_valid():
            img = form.cleaned_data.get("photo")
            obj = images.objects.create(photo = img)
            obj.save()

            person = student.objects.get(rno=rno)
            print(person.name)
            person.img = obj
            person.save()

            form = ImageForm()
            context["form"] = form
            responseFromPI = sendImageToRpi(rno)
            if responseFromPI=="ok":
                messages.info(request, person.name+"'s Photo Received!Please update Database!")
                return HttpResponseRedirect(reverse("teacher"))
            else:
                messages.info(request, "Some error occured!")
                return HttpResponseRedirect(reverse("teacher"))
    
    return render(request, "app/index.html", context)

def sendImageToRpi(rollNo):
    x = student.objects.get(rno=rollNo)
    url = piServerURL
    path = os.path.join(BASE_DIR,'media',str(x.img.photo))
    imgName = rollNo+".png"

    payload={}
    files=[
        ('img',(imgName,open(path,'rb'),'image/png'))
    ]
    headers = {
    'rno': rollNo
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    return response.text




def test(request):
    data =[
  { "date" : "2013-01-01", "close" : 45 },
  { "date" : "2013-02-01", "close" : 50 },
	{ "date" : "2013-03-01", "close" : 55 },
	{ "date" : "2013-04-01", "close" : 50 },
	{ "date" : "2013-05-01", "close" : 45 },
	{ "date" : "2013-06-01", "close" : 50 },
	{ "date" : "2013-07-01", "close" : 50 },
	{ "date" : "2013-08-01", "close" : 55 }
]

    kk=[1,2]
    
    # data.append(kk)
    context = {
        "lol1":data,
        "lol2":json.dumps(data),
    }

    return render(request, "app/test.html",context)