from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from sqlalchemy import all_

from django.http import HttpResponse
from .forms import *
from django.urls import reverse

from .models import *
import operator
import json

def home(request):
    objekt = student.objects.order_by('rno')
    n = objekt.count()
    stud1 = []
    stud2 = []
    nonDBrNos = {}

    i=0
    for x in objekt:
        i+=1
        temp = {}
        temp["sno"]=i
        temp["rno"]=x.rno
        temp["name"]=x.name

        #remove
        if(i%2==0):
            temp["attendance"]="yes"
        else:
            temp["attendance"]="no"

        temp["db"]=x.db
        if(not x.db):
            nonDBrNos[x.rno] = x.name

        if(i<n/2+1):
            stud1.append(temp)
        else:
            stud2.append(temp)

    context = {
        "stud1" : stud1,
        "stud2" : stud2,
        "nonDBrNos" : json.dumps(nonDBrNos),
        "form" : ImageForm()
    }

    if request.method == "POST":
        rno=request.POST['browser']
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("photo")
            obj = Image.objects.create(photo = img)
            obj.save()

            person = student.objects.get(rno=rno)
            print(person.name)
            person.img = obj
            person.save()

            form = ImageForm()
            context["form"] = form
            return HttpResponseRedirect(reverse("home"))
    
    return render(request, "app/index.html", context)


def test(request):
    return render(request, "app/test.html")