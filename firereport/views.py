import datetime

from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def index(request):
    return render(request, 'index.html')

def reporting(request):
    error = ""
    if request.method == "POST":
        FullName = request.POST['FullName']
        MobileNumber = request.POST['MobileNumber']
        Location = request.POST['Location']
        Message = request.POST['Message']
        try:
            Firereport.objects.create(FullName=FullName, MobileNumber=MobileNumber, Location=Location, Message=Message)
            error = "no"
        except:
            error = "yes"
    return render(request, 'reporting.html', locals())

def viewStatus(request):
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            firereport = Firereport.objects.filter(Q(FullName__icontains=sd) | Q(MobileNumber=sd) | Q(Location__icontains=sd))
        except:
            firereport = ""
    return render(request, 'viewStatus.html', locals())

def viewStatusDetails(request,pid):
    firereport = Firereport.objects.get(id=pid)
    report1 = Firetequesthistory.objects.filter(firereport=firereport)
    reportcount = Firetequesthistory.objects.filter(firereport=firereport).count()
    return render(request, 'viewStatusDetails.html', locals())

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    totalnewequest = Firereport.objects.filter(Status__isnull=True).count()
    totalAssign = Firereport.objects.filter(Status='Assigned').count()
    totalontheway = Firereport.objects.filter(Status='Team On the Way').count()
    totalworkprocess = Firereport.objects.filter(Status='Fire Relief Work in Progress').count()
    totalreqcomplete = Firereport.objects.filter(Status='Request Completed').count()
    totalfire = Firereport.objects.all().count()
    return render(request, 'admin/dashboard.html', locals())

def addTeam(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamLeaderName = request.POST['teamLeaderName']
        teamLeadMobno = request.POST['teamLeadMobno']
        teamMembers = request.POST['teamMembers']

        try:
            Teams.objects.create(teamName=teamName, teamLeaderName=teamLeaderName, teamLeadMobno=teamLeadMobno, teamMembers=teamMembers)
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/addTeam.html', locals())

def manageTeam(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Teams.objects.all()
    return render(request, 'admin/manageTeam.html', locals())

def editTeam(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Teams.objects.get(id=pid)
    error =""
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamLeaderName = request.POST['teamLeaderName']
        teamLeadMobno = request.POST['teamLeadMobno']
        teamMembers = request.POST['teamMembers']

        teams.teamName = teamName
        teams.teamLeaderName = teamLeaderName
        teams.teamLeadMobno = teamLeadMobno
        teams.teamMembers = teamMembers

        try:
            teams.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editTeam.html', locals())

def deleteTeam(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Teams.objects.get(id=pid)
    teams.delete()
    return redirect('manageTeam')

def newRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.filter(Status__isnull=True)
    return render(request, 'admin/newRequest.html', locals())

def assignRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.filter(Status='Assigned')
    return render(request, 'admin/assignRequest.html', locals())

def teamontheway(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.filter(Status='Team On the Way')
    return render(request, 'admin/teamontheway.html', locals())

def workinprogress(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.filter(Status='Fire Relief Work in Progress')
    return render(request, 'admin/workinprogress.html', locals())

def completeRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.filter(Status='Request Completed')
    return render(request, 'admin/completeRequest.html', locals())

def allRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.all()
    return render(request, 'admin/allRequest.html', locals())

def deleteRequest(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.get(id=pid)
    firereport.delete()
    return redirect('allRequest')

def viewRequestDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    firereport = Firereport.objects.get(id=pid)
    report1 = Firetequesthistory.objects.filter(firereport=firereport)
    firereportid = firereport.id
    team = Teams.objects.all()
    reportcount = Firetequesthistory.objects.filter(firereport=firereport).count()
    try:
        if request.method == "POST":
            teamid = request.POST['AssignTo']
            Status="Assigned"
            team1 = Teams.objects.get(id=teamid)
            try:
                firereport.AssignTo = team1
                firereport.Status = Status
                now = datetime.now()
                firereport.AssignedTime = now.strftime("%m/%d/%Y %H:%M:%S")
                firereport.save()
                error = "no"
            except:
                error = "yes"
    except:
        if request.method == "POST":
            status = request.POST['status']
            remark = request.POST['remark']

            try:
                requesttracking = Firetequesthistory.objects.create(firereport=firereport,status=status, remark=remark)
                firereport.Status = status
                firereport.save()
                firereport.UpdationDate = date.today()
                error1 = "no"
            except:
                error1 = "yes"
    return render(request, 'admin/viewRequestDetails.html', locals())

def dateReport(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        fd = request.POST['fromDate']
        td = request.POST['toDate']
        firereport = Firereport.objects.filter(Q(Postingdate__gte=fd) & Q(Postingdate__lte=td))
        return render(request, 'admin/betweendateReportDtls.html', locals())
    return render(request, 'admin/dateReport.html', locals())

def search(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            firereport = Firereport.objects.filter(Q(FullName__icontains=sd) | Q(MobileNumber=sd) | Q(Location__icontains=sd))
        except:
            firereport = ""
    return render(request, 'admin/search.html', locals())

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/changePassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')
