from asyncio.windows_events import NULL
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import MyUserForm, PredmetiForm
from .models import Predmeti, Korisnik, Uloge, Upisi
import operator
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


@login_required(login_url='login')
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
        if nositelj == '----':
            return redirect('subjectlist')
        noisteljKorisnik = Korisnik.objects.filter(username=nositelj)[0]
        predmet.nositelj = noisteljKorisnik
        predmet.save()  
        return HttpResponse("Subject holder updated!")
    
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
def mysubjects(request, profesor_id):
    predmeti = Predmeti.objects.filter(nositelj = profesor_id)
    profesor = Korisnik.objects.get(id = profesor_id)
    return render(request, "my_subjects.html", {'predmeti': predmeti, 'profesor': profesor})

    

def createupis(student_id, predmet_id, status):
        student = Korisnik.objects.get(id=student_id)
        predmet = Predmeti.objects.get(id=predmet_id)
        Upisi.objects.create(student=student, subject=predmet, status=status)

def deleteupis(student_id, predmet_id):
        upis = Upisi.objects.filter(student=student_id, subject=predmet_id)
        upis.delete()

@login_required(login_url='login')
def upisni(request, student_id):
    predmeti = Predmeti.objects.all()
    student = Korisnik.objects.get(id = student_id)
    upisni = Upisi.objects.filter(student = student.id)
    upisani = upisni.values_list('subject', flat=True)
    
    if request.method == 'POST':
        status = request.POST['status']
        predmet_id = request.POST['predmet_id']
        if(status == 'upisan'):
            createupis(student_id, predmet_id, status) 
        elif(status == 'ispis'):
            deleteupis(student_id, predmet_id)
        #return redirect('upisni', student_id)  

    data = {
        "predmeti": predmeti,
        "student": student,
        "upisani": upisani,
        "upisni": upisni
    }

    return render(request, "upisni_list.html", data)


def updateupis(student_id, predmet_id, status):
    upis = Upisi.objects.get(student=student_id, subject=predmet_id)
    upis.status = status
    upis.save()
        
@login_required(login_url='login')
def popisstudenata(request, predmet_id):
    predmet = Predmeti.objects.get(id = predmet_id)
    upis = Upisi.objects.filter(subject=predmet)

    if request.method == 'POST':
        status = request.POST['status']
        student_id = request.POST['student_id']
        updateupis(student_id, predmet_id, status)
        #return redirect('popisstudenata', predmet_id)

    return render(request, "popis_studenata.html", {'upisani': upis, "predmet": predmet})



  
@login_required(login_url='login')
def studentspredmet(request, predmet_id):
    predmet = Predmeti.objects.get(id = predmet_id)
    upis = Upisi.objects.filter(subject=predmet)
    return render(request, "students_predmet.html", {'upisani': upis, "predmet": predmet})


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
    return render(request, "delete_object.html", {'object':predmet})


@login_required(login_url='login')
def deleteuser(request, id):
    user = Korisnik.objects.get(id=id)
    if request.method=='POST':
        if 'yes' in request.POST:
            user.delete()
            return HttpResponse('Successfully deleted!')
        else:
            return redirect('studentlist')

    return render(request, "delete_object.html", {'object':user})

