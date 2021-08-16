from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .forms import BuildForm
import bcrypt
import json
import datetime

# Registration codes


def index(request):
    if 'id' not in request.session:
        return render(request, 'index.html')
    else:
        captain = Captain.objects.get(id=request.session['id'])
        context = {
            "captain": captain
        }
        return render(request, 'index.html', context)


def register(request):
    return render(request, 'register.html')


def registration(request):
    errors = Captain.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['pw'].encode('utf-8')
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

        new_captain = Captain.objects.create(
            fname=request.POST['fname'],
            sname=request.POST['sname'],
            code=request.POST['code'],
            pw=pw_hash)
        request.session['id'] = new_captain.id
        return redirect("/")


def login(request):
    return render(request, 'login.html')


def login_captain(request):
    login_errors = Captain.objects.gatekeeper(request.POST)
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        logged_captain = Captain.objects.get(code=request.POST['code'])
        request.session['id'] = logged_captain.id
        return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")


def command(request):
    if 'id' in request.session:
        captain = Captain.objects.get(id=request.session['id'])
        form = BuildForm()
        CREW_STATUS = Status.CREW_STATUS
        context = {
            "captain": captain,
            "all_crew": Crew.objects.filter(captain=captain).order_by('name'),
            "all_tasks": Task.objects.filter(captain=captain),
            "status_options": CREW_STATUS,


        }
        return render(request, 'command.html', context)
    else:
        return render(request, 'login.html')


def addCrew(request):
    if 'id' in request.session and len(request.POST['fname']) > 1:
        captain = Captain.objects.get(id=request.session['id'])
        newCrew = Crew.objects.create(
            name=request.POST['fname'], captain=captain)
        for i in Task.objects.filter(captain=captain).all():
            Status.objects.create(crew=newCrew,
                                  captain=captain, task=i)
        return redirect('/command')
    else:
        return redirect('/login')


def removeCrew(request, crew_id):
    c = Crew.objects.get(id=crew_id)
    c.delete()
    return redirect('/command')


def addTask(request):
    if 'id' in request.session and len(request.POST['task']) > 2:
        captain = Captain.objects.get(id=request.session['id'])
        last = Task.objects.create(
            task=request.POST['task'], captain=captain)
        for i in Crew.objects.filter(captain=captain).all():
            Status.objects.create(crew=i,
                                  captain=captain, task=last)
        return redirect('/command')
    else:
        return redirect('/login')


def removeTask(request, task_id):
    c = Task.objects.get(id=task_id)
    c.delete()
    return redirect('/command')


# REMOVED FEATURE DUE TO STATUS BEING ADDED ON CREATION OF CREW/TASK

# def add_Status(request, crew_id, task_id):
#     if 'id' in request.session:
#         captain = Captain.objects.get(id=request.session['id'])
#         crew = Crew.objects.get(id=crew_id)
#         Status.objects.create(
#             status=request.POST['status'], captain=captain, crew=crew)
#         return redirect('/command')
#     else:
#         return redirect('/login')


def updateStatus(request, stat_id):
    newStatus = request.POST['status']
    Update = Status.objects.get(id=stat_id)
    Update.status = newStatus
    print('Request: ', Update.crew.skills)
    print('New Status: ', newStatus)
    if newStatus != '...' or 'Restricted':
        Update.crew.skills += 1
    else:
        Update.crew.skills -= 1

    Update.crew.save()

    print('Request: ', Update.crew.skills)

    Update.save()
    return redirect('/command')


def updateAttendance(request):
    data = json.loads(request.body)
    crewId = data['crewId']
    presence = data['presence']

    if presence == 'checked':
        crew = Crew.objects.get(id=crewId)
        crew.present = False
    if presence == 'unchecked':
        crew = Crew.objects.get(id=crewId)
        crew.present = True

    print('CrewId:', crewId)
    print('Presence:', presence)
    print('Data:', data)

    crew.save()

    return JsonResponse('Item was added', safe=False)


# def attendance(request):
#     if 'id' in request.session:
#         captain = Captain.objects.get(id=request.session['id'])
#         form = BuildForm()
#         CREW_STATUS = Status.CREW_STATUS
#         context = {
#             "captain": captain,
#             "all_crew": Crew.objects.filter(captain=captain).order_by('name'),
#             "all_tasks": Task.objects.filter(captain=captain),
#             "status_options": CREW_STATUS,


#         }
#         return render(request, 'attendance.html', context)
#     else:
#         return render(request, 'login.html')

def attendance(request):
    if 'id' in request.session:
        captain = Captain.objects.get(id=request.session['id'])
        form = BuildForm()
        CREW_STATUS = Status.CREW_STATUS
        context = {
            "captain": captain,
            "all_crew": Crew.objects.filter(captain=captain).order_by('present', 'name'),
            "all_tasks": Task.objects.filter(captain=captain),
            "status_options": CREW_STATUS,


        }
        return render(request, 'attendance.html', context)
    else:
        return render(request, 'login.html')
