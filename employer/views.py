from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from jobs.models import Job, Application, Message
from employer.models import Company
from jobs.forms import JobForms
from employer.forms import EmployerForm
from employer.forms import CompanyForm
from users.models import User
from django.utils import timezone



def employer_check(user):
    return user.is_employer
    
def jobseeker_check(user):
    return not user.is_employer
    


@login_required(login_url='login')
@user_passes_test(employer_check, redirect_field_name='jobs:index')
def post_job(request, id):
    id = request.user
    comp = Company.objects.filter(added_by = id)
    if comp:
        company = Company.objects.get(added_by = id)
        form = JobForms(request.POST or None, request.FILES or None)
        if form.is_valid():
            add = form.save(commit=False)
            add.company_name = company.company_name
            add.company_website = company.company_website
            add.location = company.company_location
            add.logo = company.logo
            add.posted_by = request.user
            add.company = company
            # plus = Job(company_name = add.company_name, location = add.company_location, company_website = add.company_website, posted_by_id = request.user)
            add.save()
            messages.success(request, "Job posted successfully")
            return HttpResponseRedirect(reverse ('employer:jobs'))
    else:
        messages.warning(request, "You need to register a company first")
        return HttpResponseRedirect(reverse ('employer:add_company'))
    return render(request, 'post_job.html', {"form":form, "company":company,})

@login_required(login_url="login")
def job_edit(request, id):
    company = Company.objects.filter(added_by = request.user)
    job = get_object_or_404(Job, id=id)
    form = JobForms(request.POST or None, request.FILES or None, instance=job)
    if form.is_valid():
        save = form.save()
        if save:
            messages.success(request, "Job updated successfully")
        else:
            messages.error(request, "Error updating job")
        # return redirect(to='users:profile')
        return HttpResponseRedirect(
            reverse(
                "employer:job_detail",
                args=(job.id,),
            )
        )
    return render(request, "edit_job.html", {"form": form, "job": job, "company":company,})


@login_required(login_url="login")
def job_delete(request):
    jobid = request.POST.get("jobid")
    job = get_object_or_404(Job, id=jobid)
    save = job.delete()
    if save:
        messages.success(request, "Job deleted successfully")
    else:
        messages.error(request, "Error deleting job")
    return HttpResponseRedirect(reverse("employer:jobs"))

@login_required(login_url='login')
@user_passes_test(employer_check)
def add_company(request):
    company = Company.objects.filter(added_by = request.user)
    if company:
        return HttpResponseRedirect(reverse ('employer:dashboard'))
    form = CompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        add = form.save(commit=False)
        add.added_by = request.user
        added = add.save()
        if added:
            messages.success(request, "Company added successfully")
        return HttpResponseRedirect(reverse ('employer:view_company'))
    return render(request, 'addcompany.html', {"form":form})

@login_required(login_url='login')
@user_passes_test(employer_check)
def edit_company(request, id):
    company = Company.objects.get(added_by = request.user, id = id)
    jobs = Job.objects.filter(posted_by = request.user)
    print (jobs)
    form = CompanyForm(request.POST or None, request.FILES or None, instance = company)
    if form.is_valid():
        save = form.save()
        jobs.update(logo=save.logo)
        if save:
            messages.success(request, "Company updated successfully")
        else:
            messages.error(request, "Error updating company")
        return HttpResponseRedirect(reverse ('employer:view_company'))
    return render(request, 'editcompany.html', {"form":form})

@login_required(login_url='login')
@user_passes_test(employer_check)
def view_company(request):
    company = Company.objects.get(added_by = request.user)
    return render(request, 'viewcompany.html', {"company":company})
    

@login_required(login_url="login")
@user_passes_test(employer_check)
def delete_company(request):
    companyid = request.POST.get("companyid")
    company = get_object_or_404(Company, id=companyid)
    company.delete()
    return HttpResponseRedirect(reverse("employer:dashboard"))


@login_required(login_url='login')
@user_passes_test(employer_check)
def application(request):

    jobs = Job.objects.filter(posted_by = request.user)
    company = Company.objects.filter(added_by = request.user)
    print(jobs)
    applications = Application.objects.filter(posted_by = request.user)
    messages = Message.objects.all()
    print(messages)

    
    print(applications)
    return render(
        request,
        "applications.html",
        {"applications":applications,
            "jobs":jobs,
            "company":company,
         
         },
         
    
        )

@login_required(login_url='login')
@user_passes_test(employer_check)
def job_detail(request, job_id):
    company = Company.objects.filter(added_by = request.user)
    jobs = Job.objects.get(id=job_id)
    date = timezone.now().date()
    user = request.user

    return render(
        request, "jobdetails.html", {"jobs": jobs, "date": date, "user":user, "company":company,}
    )


@login_required(login_url='login')
@user_passes_test(employer_check)
def dashboard(request):
    company = Company.objects.filter(added_by = request.user)
    jobs = Job.objects.filter(posted_by = request.user).count()
    applications = Application.objects.filter(posted_by = request.user).count()

    return render(
            request,
            "employer_dashboard.html",
            {
                "company":company,
                "jobs":jobs,
                "applications":applications,
            }
    )
   

@login_required(login_url='login')
@user_passes_test(employer_check)
def jobs(request):
    company = Company.objects.filter(added_by = request.user)
    
    jobs = Job.objects.filter(posted_by = request.user).order_by('-created_at')
    return render(
        request,
        "jobs.html",
        {"jobs":jobs,
        "company":company,
         }

    )

@login_required(login_url='login')
@user_passes_test(employer_check)
def accept_application(request, id):
    applications = Application.objects.get(id = id)
    company = Company.objects.get(added_by = request.user)
    if request.method == "POST":
        message = request.POST.get("message")
        application_id = request.POST.get("application_id")
        company_name = request.POST.get("company_name")
        employer_name = request.POST.get("employer_name")
        applicant_name = request.POST.get("applicant_name")
        status = "Accepted"
        accept = Message( message=message, status = status, application_id=application_id, company_name = company_name, applicant_name = applicant_name, employer_name = employer_name)
        accept.save()
        Application.objects.filter(id = application_id).update(status = status)
        return HttpResponseRedirect(reverse("employer:applications"))
    return render (request, "accept.html", {"applications": applications, "company":company} )

@login_required(login_url='login')
@user_passes_test(employer_check)
def reject_application(request, id):
    applications = Application.objects.get(id = id)
    company = Company.objects.get(added_by = request.user)
    if request.method == "POST":
        message = request.POST.get("message")
        application_id = request.POST.get("application_id")
        company_name = request.POST.get("company_name")
        employer_name = request.POST.get("employer_name")
        applicant_name = request.POST.get("applicant_name")
        status = "Rejected"
        reject = Message( message=message, status = status, application_id=application_id, company_name = company_name, applicant_name = applicant_name, employer_name = employer_name)
        reject.save()
        Application.objects.filter(id = application_id).update(status = status)
        return HttpResponseRedirect(reverse("employer:applications"))
    return render (request, "reject.html", {"applications": applications, "company":company} )


@login_required(login_url = 'login')
def profile_view(request,id):
    company = Company.objects.filter(added_by = request.user)
    user = User.objects.get(id=id)
    return render(
        request,
        "profileview.html",
        {"user":user,
         "company":company,},
    )

@login_required(login_url='login')
def profile_edit(request,id):
    user = get_object_or_404(User,id=id)
    company = Company.objects.filter(added_by = request.user)
    form = EmployerForm(request.POST or None,request.FILES or None, instance = request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully")
        return HttpResponseRedirect(
            reverse(
                "employer:profile",
                args=(
                    user.id,
                ),
            )
        )
    return render(request,"profileedit.html",{"form":form, "user":user, "company":company,})