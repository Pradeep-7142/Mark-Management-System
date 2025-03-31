from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserLoginForm
from .models import Marks
from .forms import MarksForm

# urer registration
def register(request):
    if request.method=='POST':
        form=UserRegistration(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        form=form=UserRegistration()
    return render(request,"register.html",{'form':form})


# user login
def user_login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        form=UserLoginForm()
    return render(request,"login.html",{'form':form})

#user logout
def user_logout(request):
    logout(request)
    return redirect('login')


# dashboard
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.role=='admin':
            return render(request,"admin_dashboard.html")
        elif request.user.role=='teacher':
            return render(request,"teacher_dashboard.html")
        elif request.user.role=='student':
            return render(request,"student_dashboard.html")
    
    return redirect('login')
    
# Defining the view for different types of users
@login_required
def marks_list(request):
    if request.user.is_staff:  # Teachers/Admins can view all marks 
        marks = Marks.objects.all()
    else:  # Students can view only their marks
        marks = Marks.objects.filter(student=request.user)
    return render(request, 'marks_list.html', {'marks': marks})


@login_required
def marks_create(request):
    if request.user.is_staff:  # Only teachers/admins can add marks
        if request.method == "POST":
            form = MarksForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('marks_list')
        else:
            form = MarksForm()
        return render(request, 'marks_form.html', {'form': form})
    return redirect('marks_list')

@login_required
def marks_update(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    if request.user.is_staff:  # Only teachers/admins can edit
        if request.method == "POST":
            form = MarksForm(request.POST, instance=mark)
            if form.is_valid():
                form.save()
                return redirect('marks_list')
        else:
            form = MarksForm(instance=mark)
        return render(request, 'marks_form.html', {'form': form})
    return redirect('marks_list')

@login_required
def marks_delete(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    if request.user.is_staff:  # Only teachers/admins can delete
        if request.method == "POST":
            mark.delete()
            return redirect('marks_list')
        return render(request, 'marks_confirm_delete.html', {'mark': mark})
    return redirect('marks_list')