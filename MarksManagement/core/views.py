from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserLoginForm
from .models import Marks
from .forms import MarksForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse

# Home 
def home(request):
    return render(request, 'home.html')

# urer registration
def register(request):
    if request.method=='POST':
        form=UserRegistration(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        form=UserRegistration()
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


# Teacher View: View all marks with filter options
@login_required
def view_all_marks(request):
    if request.user.role != 'teacher':
        return render(request, 'unauthorized.html')

    marks = Marks.objects.all()

    # Optional filtering by subject or student
    subject = request.GET.get('subject')
    student = request.GET.get('student')
    if subject:
        marks = marks.filter(subject__icontains=subject)
    if student:
        marks = marks.filter(student__username__icontains=student)

    return render(request, 'view_all_marks.html', {'marks': marks})

# Student View: View own marks
@login_required
def view_my_marks(request):
    if request.user.role != 'student':
        return render(request, 'unauthorized.html')

    marks = Marks.objects.filter(student=request.user)
    return render(request, 'view_my_marks.html', {'marks': marks})


def download_result(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        return HttpResponse("Unauthorized", status=401)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 50, "Student Result Report")

    # Student Info
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Student Name: {request.user.get_full_name()}")
    p.drawString(50, height - 100, f"Email: {request.user.email}")

    # Marks Table Headers
    marks = Marks.objects.filter(student=request.user)
    data = [['Subject', 'Score']]
    total = 0

    for mark in marks:
        data.append([mark.subject, str(mark.marks_obtained)])
        total += mark.marks_obtained

    # Table for Subject-wise Scores
    table = Table(data, colWidths=[250, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, height - 280)

    # Summary Table (Total, Percentage, Grade)
    subject_count = len(marks)
    percentage = round((total / (250)) * 100, 2) if subject_count else 0

    # Simple grading logic
    if percentage >= 90:
        grade = 'A+'
    elif percentage >= 80:
        grade = 'A'
    elif percentage >= 70:
        grade = 'B'
    elif percentage >= 60:
        grade = 'C'
    elif percentage >= 50:
        grade = 'D'
    else:
        grade = 'F'

    summary_data = [
        ['Total Marks', str(total)],
        ['Percentage', f"{percentage}%"],
        ['Grade', grade],
    ]

    summary_table = Table(summary_data, colWidths=[250, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    summary_table.wrapOn(p, width, height)
    summary_table.drawOn(p, 50, height - 400)

    # Finalize PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')