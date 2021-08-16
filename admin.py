from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Captain)
admin.site.register(Crew)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(AttendanceSheet)
admin.site.register(AttendanceItem)
