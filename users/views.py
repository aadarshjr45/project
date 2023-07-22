from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Contact
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from users.forms import  SignUpForm,ProfileForm, LoginForm, ContactForm
from .models import User
from jobs.models import Application, Message


User = get_user_model()

def jobseeker_check(user):
    return not user.is_employer

# class UserLoginView(LoginView):
#     template_name = "login.html"
   
def login_view(request):
    form = LoginForm(request.POST or None)
    next_url = request.POST.get('next')
    if request.POST and form.is_valid():
        user = form.login(request)
        if not user:
            raise ValueError("Invalid credentials")
        if user:
            login(request,user)
            if next_url:
                return HttpResponseRedirect(next_url)
            if user.is_employer:
                return HttpResponseRedirect(reverse ('employer:dashboard'))
            else:
                return HttpResponseRedirect(reverse ('jobs:index'))
            
    else:
        return render(request,"login.html", {"form":form})



def signup_view(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if 'resume' in request.FILES:
                resume = request.FILES['resume']
            else:
                resume = None
            insert = form.save(commit=False)
            insert.resume = resume
            insert.save()
            messages.success(request, 'Your account is created successfully')
            return HttpResponseRedirect(reverse ('login'))

        else:
            msg = "form invalid"
    else:
        form = SignUpForm
    return render(request,'register.html', {'form':form, 'msg':msg})

        
@login_required(login_url = 'login')
@user_passes_test(jobseeker_check)
def profile_view(request,id):
    user = get_object_or_404(User,id=id)
    return render(
        request,
        "myprofile.html",
        {"user":user},
    )



@login_required(login_url='login')
@user_passes_test(jobseeker_check)
def profile_edit(request,id):
    user = get_object_or_404(User,id=id)
    form = ProfileForm(request.POST or None,request.FILES or None, instance = request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your profile is updated successfully')
        Application.objects.filter(submitted_by=user).update(resume = user.resume)
        return HttpResponseRedirect(
            reverse(
                "users:profile",
                args=(
                    user.id,
                ),
            )
        )
    
    return render(request,"myprofileedit.html",{"form":form})

@login_required(login_url='login')
@user_passes_test(jobseeker_check)
def application_view(request):
    applications = Application.objects.all()
    return render(
        request,
        "myapplications.html",
        {"applications":applications}
       
    )
@login_required(login_url='login')
@user_passes_test(jobseeker_check)
def application_delete(request):
    applicationid = request.POST.get("applicationid")
    application = get_object_or_404(Application, id=applicationid)
    application.delete()
    return HttpResponseRedirect(reverse("users:application_view"))

@login_required(login_url='login')
@user_passes_test(jobseeker_check)
def view_message(request, id):
    application = Application.objects.get(id = id)
    print(application)
    message = Message.objects.get(application_id = application)
    print(message)
    return render(request, "message.html", {
        "applicaiton":application,
        "message":message,
    })

def contactus(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message= request.POST.get('message')
        add = Contact(name=name, email=email, subject=subject, message=message)
        add.save()
        if add:
            messages.success(request, 'Your message is sent successfully')
        return HttpResponseRedirect(reverse ('jobs:index'))
    else:
        form = ContactForm
    return render(request,'contact.html', {'form':form})