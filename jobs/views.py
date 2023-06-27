import re
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from jobs.models import Job, Application
from django.utils import timezone
from jobs.forms import JobForms, CategoryForm, TypeForm, LevelForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def homepage(request):
    jobs = Job.objects.order_by("-created_at")[:6]
    return render(request, "index.html", {"jobs": jobs})


def job_list(request):
    category = CategoryForm(request.POST or None)
    type = TypeForm(request.POST or None)
    level = LevelForm(request.POST or None)
    date = timezone.now().date()
    jobs = Job.objects.all().order_by("-created_at")
    return render(
        request, "job_list.html", {"jobs": jobs, "date": date, "category": category, "type": type, "level": level}
    )


def job_detail(request, job_id):
    jobs = Job.objects.get(id=job_id)
    all = Job.objects.order_by("-created_at")[:6]
    date = timezone.now().date()
    user = request.user
    applications = Application.objects.filter(submitted_by=user, submitted_for=jobs)
    print(applications)

    return render(
        request, "details.html", {"jobs": jobs, "applications": applications, "all": all, "date": date}
    )


@login_required(login_url="login")
def job_edit(request, id):
    job = get_object_or_404(Job, id=id)
    form = JobForms(request.POST or None, request.FILES or None, instance=job)
    if form.is_valid():
        form.save()
        # return redirect(to='users:profile')
        return HttpResponseRedirect(
            reverse(
                "jobs:job_detail",
                args=(job.id,),
            )
        )
    return render(request, "editjob.html", {"form": form, "job": job})


@login_required(login_url="login")
def job_delete(request):
    jobid = request.POST.get("jobid")
    job = get_object_or_404(Job, id=jobid)
    job.delete()
    return HttpResponseRedirect(reverse("jobs:job_list"))


@login_required(login_url="login")
def apply_job(request, job_id):
    jobs = Job.objects.get(id=job_id)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        resume = request.FILES.get("resume")
        submitted_for_id = request.POST.get("submitted_for_id")
        submitted_by_id = request.POST.get("submitted_by_id")
        applicant = Application(
            name=name,
            email=email,
            resume=resume,
            submitted_for_id=submitted_for_id,
            submitted_by_id=submitted_by_id,
            posted_by=jobs.posted_by,
        )
        applicant.save()
        return HttpResponseRedirect(reverse("users:application_view"))
    return render(request, "job_apply.html", {"job": jobs})


def search_view(request):
    if request.method == "POST":
        searchtext = request.POST["searchtext"]
        print(searchtext)
        searchresult = Job.objects.filter(
            Q(title__contains=searchtext)
            | Q(company_name__contains=searchtext)
            | Q(location__contains=searchtext)
        )
        paginator = Paginator(searchresult, per_page=4)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(
                page_number
            )  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)
        return render(
            request, "search.html", {"searchtext": searchtext, "jobs": page_obj}
        )
    return render(request, "search.html")


def filter_view(request):
    print("hello")
    categoryform = CategoryForm(request.POST or None)
    typeform = TypeForm(request.POST or None)
    levelform = LevelForm(request.POST or None)
    if request.method == "POST":
        category = request.POST["category"]
        type = request.POST["type"]
        level = request.POST["level"]
        filterjob = Job.objects.filter(
            Q(category__contains=category)
            | Q(type__contains=type)
            | Q(level__contains=level)
        )

        print(filterjob)
        paginator = Paginator(filterjob, per_page=4)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(
                page_number
            )  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "filter.html", {"jobs": page_obj, "category": categoryform, "type": typeform, "level": levelform})
    return render(request, "filter.html")
