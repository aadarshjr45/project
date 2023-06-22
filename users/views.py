from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from users.forms import  SignUpForm,ProfileForm
from .models import User
from jobs.models import Application, Message
from jobs.forms import ApplicationForm


User = get_user_model()

class UserLoginView(LoginView):
    template_name = "login.html"
    





def signup_view(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            msg = "user registered"
            form.save()
            return HttpResponseRedirect(reverse ('login'))

        else:
            msg = "form invalid"
    else:
        form = SignUpForm
    return render(request,'register.html', {'form':form, 'msg':msg})

        
@login_required(login_url = 'login')
def profile_view(request,id):
    user = get_object_or_404(User,id=id)
    return render(
        request,
        "myprofile.html",
        {"user":user},
    )

@login_required(login_url='login')
def profile_edit(request,id):
    user = get_object_or_404(User,id=id)
    form = ProfileForm(request.POST or None,request.FILES or None, instance = request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your profile is updated successfully')
        # return redirect(to='users:profile')
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
def application_view(request):
    applications = Application.objects.all()
    return render(
        request,
        "myapplications.html",
        {"applications":applications}
       
    )
@login_required(login_url='login')
def application_delete(request):
    applicationid = request.POST.get("applicationid")
    application = get_object_or_404(Application, id=applicationid)
    application.delete()
    return HttpResponseRedirect(reverse("users:application_view"))

@login_required(login_url='login')
def view_message(request, id):
    application = Application.objects.get(id = id)
    print(application)
    message = Message.objects.get(application_id = application)
    print(message)
    return render(request, "message.html", {
        "applicaiton":application,
        "message":message,
    })