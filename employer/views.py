from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from jobs.models import Job, Application, Message, Company
from jobs.forms import JobForms
from employer.forms import CompanyForm
from users.models import User


def user_check(user):
    return user.is_employer


@login_required(login_url='login')
@user_passes_test(user_check)
def post_job(request, id):
    id = request.user
    company = Company.objects.get(added_by = id)
    print (company)
    form = JobForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        add = form.save(commit=False)
        add.company_name = company.company_name
        add.company_website = company.company_website
        add.location = company.company_location
        add.logo = company.logo
        add.posted_by = request.user
        # plus = Job(company_name = add.company_name, location = add.company_location, company_website = add.company_website, posted_by_id = request.user)
        add.save()
        return HttpResponseRedirect(reverse ('jobs:job_list'))
    return render(request, 'post_job.html', {"form":form, "company":company,})

@login_required(login_url='login')
@user_passes_test(user_check)
def add_company(request):
    company = Company.objects.filter(added_by = request.user)
    if company:
        return HttpResponseRedirect(reverse ('employer:dashboard'))
    form = CompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        add = form.save(commit=False)
        add.added_by = request.user
        add.save()
        return HttpResponseRedirect(reverse ('employer:dashboard'))
    return render(request, 'addcompany.html', {"form":form})

@login_required(login_url='login')
@user_passes_test(user_check)
def edit_company(request, id):
    company = Company.objects.get(added_by = request.user, id = id)
    form = CompanyForm(request.POST or None, request.FILES or None, instance = company)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse ('employer:dashboard'))
    return render(request, 'editcompany.html', {"form":form})

@login_required(login_url='login')
@user_passes_test(user_check)
def view_company(request):
    company = Company.objects.get(added_by = request.user)
    return render(request, 'viewcompany.html', {"company":company})
    



@login_required(login_url='login')
@user_passes_test(user_check)
def application(request):

    jobs = request.user
    applications = Application.objects.filter(posted_by = jobs)
    messages = Message.objects.all()
    print(messages)

    
    print(applications)
    return render(
        request,
        "applications.html",
        {"applications":applications,
         
         },
         
    
        )



@login_required(login_url='login')
@user_passes_test(user_check)
def dashboard(request):
    company = Company.objects.filter(added_by = request.user)
    jobs = Job.objects.filter(posted_by = request.user).count()

    return render(
            request,
            "employer_dashboard.html",
            {
                "company":company,
                "jobs":jobs,
            }
    )
   

@login_required(login_url='login')
@user_passes_test(user_check)
def jobs(request):
    jobs = Job.objects.filter(posted_by = request.user)
    return render(
        request,
        "jobs.html",
        {"jobs":jobs,
         }

    )

@login_required(login_url='login')
@user_passes_test(user_check)
def accept_application(request, id):
    applications = Application.objects.get(id = id)
    if request.method == "POST":
        message = request.POST.get("message")
        application_id = request.POST.get("application_id")
        status = "accepted"
        accept = Message( message=message, status = status, application_id=application_id)
        accept.save()
        Application.objects.filter(id = application_id).update(status = status)
        return HttpResponseRedirect(reverse("employer:applications"))
    return render (request, "accept.html", {"applications": applications})

@login_required(login_url='login')
@user_passes_test(user_check)
def reject_application(request, id):
    applications = Application.objects.get(id = id)
    if request.method == "POST":
        message = request.POST.get("message")
        application_id = request.POST.get("application_id")
        status = "rejected"
        reject = Message( message=message, status = status, application_id=application_id)
        reject.save()
        Application.objects.filter(id = application_id).update(status = status)
        return HttpResponseRedirect(reverse("employer:applications"))
    return render (request, "reject.html", {"applications": applications})


@login_required(login_url = 'login')
def profile_view(request,id):
    user = User.objects.get(id=id)
    return render(
        request,
        "profileview.html",
        {"user":user},
    )