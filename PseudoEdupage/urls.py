
from django.urls import path
from django.contrib import admin
from app import views


urlpatterns = [
    path('', views.home, name='home'),

    path('teachers/',
         views.teachers,
         name='teachers'),
 
    path('teachers/<int:pk>/',
         views.teacher_edit,
         name='teacher_edit'),
 

    path('students/',
         views.students,
         name='students'),
 
    path('students/<int:pk>/',
         views.student_edit,
         name='student_edit'),


    path('classes/',
         views.schoolclasses,
         name='schoolclasses'),
 
    path('classes/<int:pk>/',
         views.schoolclass_edit,
         name='schoolclass_edit'),
 

    path('subjects/',
         views.subjects,
         name='subjects'),
 
    path('subjects/<int:pk>/',
         views.subject_edit,
         name='subject_edit'),


    path('grades/',
         views.grades,
         name='grades'),
 
    path('grades/<int:pk>/',
         views.grade_edit,
         name='grade_edit'),
    path('admin/', admin.site.urls),
]
