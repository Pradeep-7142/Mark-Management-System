from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import createForms
from service.models import Service
from news.models import News
from contact.models import Contact
from django.core.paginator import Paginator
from django.core.mail import send_mail
def homePage(request):
    # send_mail(
    #     'testing-mail',
    #     'here is the first generated email',
    #     'pradeep080805@gmail.com',
    #     ['su-23026@sitare.org'],
    #     fail_silently=False
    # )

    data={
        'title':"Home Page dynamic",
        'slist':['JAVA','PYTHON','DSA'],
        'ins':[{'name':"Pradeep",'Mobile':9090909048},{'name':"Pradeep",'Mobile':9090909048}]
    }
    return render(request, "index.html",data)

def aboutUs(request):
    if request.method=="GET":
        name=request.GET.get('result')
    return render(request, "about.html",{"name":name})

def services(request,method=['GET']):
    serviceData=Service.objects.all().order_by('-service_titie') #to order we have used order_by and dash is for descending 
    newsData=News.objects.all()
    if request.method=='GET':
        searched=request.GET.get('data')
        if searched!=None:
            serviceData=Service.objects.filter(service_titie__icontains=searched) #if any letter will match then it will show only that data 
    
    paginator=Paginator(serviceData,1)
    page_number=request.GET.get('page')
    serviceDataFinal=paginator.get_page(page_number)
    totalpages=serviceDataFinal.paginator.num_pages
    data={
       'serviceData':serviceDataFinal,
       'newsData':newsData,
       'lastpage':totalpages,
       'pagelist':[n+1 for n in range(totalpages)]
    }
    
    return render(request, "services.html",data)

def newsDetails(request,slug):
    newsData=News.objects.get(new_slug=slug)
    data={
        'newsDetails':newsData
    }
    return render(request,"newsDetails.html",data)

def submitForm(request):
    name=""
    email=""
    message=""
    
    try:
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            message=request.POST['message']
            
            result=name +" "+ email +" "+ message
            return HttpResponse(result)
    except:
        pass

def contact(request):
    # name=""
    # email=""
    # message=""
    num1=0
    num2=0
    fn=createForms()
    data={"form":fn}
    try:
        if request.method=='POST':
            # name=request.POST['name']
            # email=request.POST['email']
            # message=request.POST['message']
            num1=int(request.POST.get('num1'))
            num2=int(request.POST.get('num2'))
            result=num1+num2
            data={
               'form':fn,
               'result':result
            }
            # url="/aboutUs/?result={}".format(name)
            # return redirect(url)
    except:
        pass
    return render(request, "contact.html",data)

def courseInfo(request,id):
    return HttpResponse(id)

def submitContact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        toSave=Contact(name=name,email=email,phone=phone,message=message)
        toSave.save()
    return render(request,"index.html")