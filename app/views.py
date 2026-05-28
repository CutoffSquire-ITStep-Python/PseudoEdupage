from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpRequest
from .models import Teacher, Student, SchoolClass, Subject, Grade
from .forms import TeacherForm, StudentForm, SchoolClassForm, SubjectForm, GradeForm

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':timezone.now().year,
        }
    )


def teachers(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            teacher = get_object_or_404(Teacher, pk=request.POST.get('teacher_id'))
            teacher.delete()
            return redirect('teachers')

        if action == 'create':
            form = TeacherForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('teachers')
        else:
            form = TeacherForm()
    else:
        form = TeacherForm()

    return render(request, 'app/teachers.html', {
        'title': 'Teachers',
        'form': form,
        'teachers': Teacher.objects.all(),
    })


def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'app/teacher_edit.html', {
        'title': 'Teacher Edit',
        'form': form,
        'teacher': teacher,
    })



def students(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            student = get_object_or_404(Student, pk=request.POST.get('student_id'))
            student.delete()
            return redirect('students')

        if action == 'create':
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('students')
        else:
            form = StudentForm()
    else:
        form = StudentForm()

    return render(request, 'app/students.html', {
        'title': 'Students',
        'form': form,
        'students': Student.objects.all(),
    })


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm(instance=student)

    return render(request, 'app/student_edit.html', {
        'title': 'Student Edit',
        'form': form,
        'student': student,
    })



def schoolclasses(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            school_class = get_object_or_404(SchoolClass, pk=request.POST.get('class_id'))
            school_class.delete()
            return redirect('schoolclasses')

        if action == 'create':
            form = SchoolClassForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('schoolclasses')
        else:
            form = SchoolClassForm()
    else:
        form = SchoolClassForm()

    return render(request, 'app/schoolclasses.html', {
        'title': 'Classes',
        'form': form,
        'classes': SchoolClass.objects.all(),
    })


def schoolclass_edit(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)

    if request.method == 'POST':
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            return redirect('schoolclasses')
    else:
        form = SchoolClassForm(instance=school_class)

    return render(request, 'app/schoolclass_edit.html', {
        'title': 'Class Edit',
        'form': form,
        'schoolclass': school_class,
    })



def subjects(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            subject = get_object_or_404(Subject, pk=request.POST.get('subject_id'))
            subject.delete()
            return redirect('subjects')

        if action == 'create':
            form = SubjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('subjects')
        else:
            form = SubjectForm()
    else:
        form = SubjectForm()

    return render(request, 'app/subjects.html', {
        'title': 'Subjects',
        'form': form,
        'subjects': Subject.objects.all(),
    })


def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subjects')
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'app/subject_edit.html', {
        'title': 'Subject Edit',
        'form': form,
        'subject': subject,
    })



def grades(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            grade = get_object_or_404(Grade, pk=request.POST.get('grade_id'))
            grade.delete()
            return redirect('grades')

        if action == 'create':
            form = GradeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('grades')
        else:
            form = GradeForm()
    else:
        form = GradeForm()

    return render(request, 'app/grades.html', {
        'title': 'Grades',
        'form': form,
        'grades': Grade.objects.all(),
    })


def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm(instance=grade)

    return render(request, 'app/grade_edit.html', {
        'title': 'Grade Edit',
        'form': form,
        'grade': grade,
    })