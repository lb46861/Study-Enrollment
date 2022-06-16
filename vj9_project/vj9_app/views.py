from multiprocessing.sharedctypes import Value
import string
from xml.etree.ElementTree import tostring
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .forms import MyUserForm, PredmetiForm
from .models import Predmeti, Korisnik, Uloge
# Create your views here.



def adduser(request):
    if request.method == 'GET':
        form = MyUserForm()
        return render(request, 'add_user.html', {'form':form})

    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('User successffuly created!')
        else:
            return HttpResponse('Something went wrong!')


@login_required
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def addpredmet(request):
    if request.method == 'GET':
        form = PredmetiForm()
        return render(request, 'add_predmet.html', {'form':form})

    if request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjectlist')
        else:
            return HttpResponse('Not able to save!')

@login_required(login_url='login')
def addnositelj(request, id):
    predmet = get_object_or_404(Predmeti, id = id)
    roles = Uloge.objects.get(role='profesor')
    profesori = Korisnik.objects.filter(role=roles)
    if request.method == 'GET':
        data = {
            'predmet': predmet,
            'profesori': profesori
        }
        return render(request, 'add_nositelj.html', data)

    elif request.method == 'POST':
        nositelj = request.POST['profesor']
        noisteljKorisnik = Korisnik.objects.filter(username=nositelj)[0]
        predmet.nositelj = noisteljKorisnik
        predmet.save()  
        return redirect('subjectlist')
    
    else:
        return HttpResponse("Something went wrong!")




@login_required(login_url='login')
def subjectlist(request):
    predmeti = Predmeti.objects.all()
    return render(request, 'subject_list.html', {'predmeti': predmeti})


@login_required(login_url='login')
def studentlist(request):
    users = Korisnik.objects.all()
    students = []
    for user in users:
        if str(user.role) == 'student':
            students.append(user)
    return render(request, "student_list.html", {'users':students})


@login_required(login_url='login')
def profesorlist(request):
    users = Korisnik.objects.all()
    profesors = []
    for user in users:
        if str(user.role) == 'profesor':
            profesors.append(user)
    return render(request, "profesor_list.html", {'users':profesors})  




@login_required(login_url='login')
def subjectdetails(request, id):
    predmet = Predmeti.objects.get(id = id)
    return render(request, "subject_details.html", {'predmet': predmet})


@login_required(login_url='login')
def editsubject(request, id):
    predmet = Predmeti.objects.get(id = id)
    form = PredmetiForm(instance=predmet)

    if request.method=='POST':
        form = PredmetiForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            return HttpResponse('Successfully edited!')

    return render(request, "edit_subject.html", {'form': form})


@login_required(login_url='login')
def edituser(request, id):
    user = Korisnik.objects.get(id = id)
    form = MyUserForm(instance=user)

    if request.method=='POST':
        form = MyUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse('Successfully edited!')

    return render(request, "edit_user.html", {'form': form})


@login_required(login_url='login')
def deletesubject(request, id):
    predmet = Predmeti.objects.get(id=id)
    if request.method=='POST':
        if 'yes' in request.POST:
            predmet.delete()
            return HttpResponse('Successfully deleted!')
        else:
            return redirect('subjectlist')
    return render(request, "delete_object.html")


@login_required(login_url='login')
def deleteuser(request, id):
    user = Korisnik.objects.get(id=id)
    if request.method=='POST':
        if 'yes' in request.POST:
            user.delete()
            return HttpResponse('Successfully deleted!')
        else:
            return redirect('subjectlist')

    return render(request, "delete_object.html")

