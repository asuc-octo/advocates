from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Case)
admin.site.register(Comment)
admin.site.register(CaseWorker)