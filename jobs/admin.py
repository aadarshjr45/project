from django.contrib import admin
from .models import Company, Job, Application, Message


admin.site.register(Job)

admin.site.register(Application)

admin.site.register(Message)

admin.site.register(Company)