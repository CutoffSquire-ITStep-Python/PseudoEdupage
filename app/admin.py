from django.contrib import admin
from .models import Teacher, Student, SchoolClass, Subject, Grade

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Grade)