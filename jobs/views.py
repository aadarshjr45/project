import re
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from jobs.models import Job, Application
from django.utils import timezone
from jobs.forms import JobForms, CategoryForm, TypeForm, LevelForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
    
def ml_recommendation_system(job, top_n=5):
    try:
        # Preprocess and vectorize the text data
        category = job.category
        level = job.level
        type = job.type
        

        # jobs = models.job.objects.exclude(pk=job.pk, category=category)
        jobs = Job.objects.filter(Q(category__contains = category) | Q(level__contains = level) | Q(type__contains = type) ).exclude(pk=job.pk)
        texts = [
            job.title + " " + job.description + " " + job.level
            for job in jobs
        ]
        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(texts)

        # Calculate similarity scores
        job_vector = vectorizer.transform(
            [job.title + " " + job.description + " " + job.level]
        )
        similarity_scores = cosine_similarity(job_vector, feature_vectors).flatten()

        # Get the indices of the top similar jobs
        top_indices = similarity_scores.argsort()[::-1][:top_n]

        # Retrieve the top similar jobs
        similar_jobs = [jobs[idx] for idx in top_indices.tolist()]
        print(similar_jobs)
        return similar_jobs
        
    except ValueError as e:
        print(str(e))
        return []
    

def jobseeker_check(user):
    return not user.is_employer



def homepage(request):
    jobs = Job.objects.order_by("-created_at")[:4]
    return render(request, "index.html", {"jobs": jobs})


@login_required
@user_passes_test(jobseeker_check)
def job_list(request):
    category = CategoryForm(request.POST or None)
    type = TypeForm(request.POST or None)
    level = LevelForm(request.POST or None)
    date = timezone.now().date()
    jobs = Job.objects.all().order_by("-created_at")
    paginator = Paginator(jobs,per_page = 3)
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
        request, "job_list.html", {"jobs": page_obj, "date": date, "category": category, "type": type, "level": level}
    )
    

@login_required(login_url="login")
@user_passes_test(jobseeker_check)
def job_detail(request, job_id):
    jobs = Job.objects.get(id=job_id)
    all = Job.objects.order_by("-created_at")[:6]
    date = timezone.now().date()
    user = request.user
    applications = Application.objects.filter(submitted_by=user, submitted_for=jobs)
    similar_jobs = ml_recommendation_system(jobs, top_n=5)

    return render(
        request, "details.html", {"jobs": jobs, "applications": applications, "all": all, "date": date, "similar_jobs": similar_jobs}
    )




@login_required(login_url="login")
@user_passes_test(jobseeker_check)
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
    categoryform = CategoryForm(request.POST)
    typeform = TypeForm(request.POST)
    levelform = LevelForm(request.POST)
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
            request, "search.html", {"searchtext": searchtext, "jobs": page_obj, "category": categoryform, "type": typeform, "level": levelform}
        )
    return render(request, "search.html")


def filter_view(request):
    print("hello")
    categoryform = CategoryForm(request.POST)
    typeform = TypeForm(request.POST)
    levelform = LevelForm(request.POST)
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
