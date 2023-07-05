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
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
import random
import warnings
warnings.filterwarnings('ignore')
    
# def get_job_recommendations(user, job_similarity, jobs, num_recommendations):
#     user_jobs = jobs.filter(user=user)
#     if user_jobs.exists():
#         user_job_categories = user_jobs.values_list('category', flat=True).distinct()
#         user_similar_jobs = []

#         for category in user_job_categories:
#             similar_scores = job_similarity[category].sort_values(ascending=False)
#             similar_jobs = similar_scores.iloc[1:num_recommendations+1].index.tolist()
#             user_similar_jobs.extend(similar_jobs)

#         recommended_jobs = jobs.filter(category__in=user_similar_jobs)
#         recommended_jobs = recommended_jobs.exclude(user=user)
#         return recommended_jobs.order_by('?')[:num_recommendations]

#     else:
#         return jobs.order_by('?')[:num_recommendations]

# def main(request):
#     jobs = Job.objects.get_queryset()

#     # numeric_job_fields = pd.DataFrame(jobs.values_list('salary', flat=True))

#     categorical_job_fields = pd.DataFrame(jobs.values_list('category', flat=True))
#     # print(numeric_job_fields)
  
#     numeric_transformer = StandardScaler()
#     categorical_transformer = OneHotEncoder()

#     preprocessor = ColumnTransformer(
#         transformers=[
#             # ('numeric', numeric_transformer, numeric_job_fields),
#             ('categorical', categorical_transformer, categorical_job_fields)
#         ] ,
#         remainder='drop',
#                     n_jobs=-1)

#     job_values = []
#     for job in jobs:
#         print(categorical_job_fields)
#         # numeric_values = [getattr(job, field) for field in numeric_job_fields]
#         categorical_values = [getattr(job, field) for field in categorical_job_fields]
#         job_values.append(categorical_values)
        
    
#     jobs_reshaped =preprocessor.fit_transform(job_values)
#     print(jobs_reshaped)
#     job_similarity = cosine_similarity(jobs_reshaped)
#     job_similarity_df = pd.DataFrame(job_similarity, index=jobs.values_list('category', flat=True), columns=jobs.values_list('category', flat=True))

#     num_recommendations = 5
#     num = random.randint(1, 38)
#     user =request.user   
#     print(f"User: {user}")

#     recommended_jobs = get_job_recommendations(user, job_similarity_df, jobs, num_recommendations)

#     print("Recommended Jobs:")
#     print(recommended_jobs)

# if __name__ == "__main__":
#     main()


# def calculate_job_similarities(user_jobs):
#     """
#     Calculates the similarity between the user's previous jobs.

#     Args:
#         user_jobs: A list of jobs.

#     Returns:
#         A Pandas DataFrame of job similarities.
#     """

#     # Create a list of the job features.
#     job_features = ['category', 'type', 'salary']

#     # Create a Pandas DataFrame of the user's previous jobs.
#     user_jobs_df = pd.DataFrame(user_jobs.values_list(*job_features), columns=job_features)

#     # Calculate the cosine similarity between the user's previous jobs.
#     job_similarities = cosine_similarity(user_jobs_df)

#     return job_similarities

# def get_job_recommendations(user, jobs, num_recommendations):
#     """
#     Recommends jobs to the user based on their previous jobs selections.

#     Args:
#         user: The user ID.
#         jobs: A list of jobs.
#         num_recommendations: The number of recommendations to return.

#     Returns:
#         A list of recommended jobs.
#     """

#     # Create a list of the user's previous jobs.
#     user_jobs = jobs.filter(user=user)

#     # Calculate the similarity between the user's previous jobs.
#     job_similarities = calculate_job_similarities(user_jobs)

#     # Identify the most similar jobs to the user's previous jobs.
#     most_similar_jobs = job_similarities.sort_values(ascending=False)[:num_recommendations]

#     # Return the top `n` most similar jobs to the user.
#     return most_similar_jobs

def homepage(request):
    jobs = Job.objects.order_by("-created_at")[:6]
    return render(request, "index.html", {"jobs": jobs})

def jobseeker_check(user):
    return not user.is_employer

def job_list(request):
    category = CategoryForm(request.POST or None)
    type = TypeForm(request.POST or None)
    level = LevelForm(request.POST or None)
    date = timezone.now().date()
    jobs = Job.objects.all().order_by("-created_at")
    paginator = Paginator(jobs,12)
    page_number = request.GET.get("page")
    jobsfinal = paginator.get_page(page_number)
    return render(
        request, "job_list.html", {"jobs": jobs, "date": date, "category": category, "type": type, "level": level, "jobsfinal": jobsfinal}
    )

@login_required(login_url="login")
@user_passes_test(jobseeker_check)
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
