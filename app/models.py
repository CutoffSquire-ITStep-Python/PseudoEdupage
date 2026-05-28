from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint, CheckConstraint, Q


class Teacher(models.Model):
    DEGREE_CHOICES = [
        ('none', 'None'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('doctor', 'Doctor of Science'),
    ]

    full_name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        default='none',
        verbose_name="Academic Degree"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['full_name']),
        ]
        constraints = [
            UniqueConstraint(fields=['email'], name='unique_teacher_email'),
        ]

    def __str__(self):
        return self.full_name


class Student(models.Model):
    full_name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Full Name")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['full_name']),
        ]

    def __str__(self):
        return self.full_name


class SchoolClass(models.Model):

    number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        verbose_name="Class Number"
    )
    abbreviation = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Abbreviation",
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Full Name",
    )

    students = models.ManyToManyField(
        Student,
        related_name='classes',
        blank=True,
        verbose_name="Students"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "School Class"
        verbose_name_plural = "School Classes"
        ordering = ['number', 'abbreviation']
        constraints = [
            UniqueConstraint(fields=['abbreviation'], name='unique_class_abbreviation'),
            CheckConstraint(
                condition=Q(number__gte=1) & Q(number__lte=9),
                name='class_number_range'
            ),
        ]

    def __str__(self):
        return self.abbreviation


class Subject(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True, verbose_name="Subject Name")

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects',
        verbose_name="Teacher"
    )
    students = models.ManyToManyField(
        Student,
        related_name='subjects',
        blank=True,
        verbose_name="Students"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']
        constraints = [
            UniqueConstraint(fields=['name'], name='unique_subject_name'),
        ]

    def __str__(self):
        return self.name


class Grade(models.Model):

    GRADE_TYPE_CHOICES = [
        ('none', 'None'),
        ('classwork', 'Classwork'),
        ('homework', 'Homework'),
        ('test', 'Test'),
        ('project', 'Project'),
    ]

    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Grade",
    )
    grade_type = models.CharField(
        max_length=20,
        choices=GRADE_TYPE_CHOICES,
        default='none',
        verbose_name="Grade Type"
    )

    students = models.ManyToManyField(
        Student,
        related_name='grades',
        blank=True,
        verbose_name="Students"
    )
    subjects = models.ManyToManyField(
        Subject,
        related_name='grades',
        blank=True,
        verbose_name="Subjects"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['value']),
        ]
        constraints = [
            CheckConstraint(
                condition=Q(value__gte=1) & Q(value__lte=5),
                name='grade_value_range'
            ),
        ]

    def __str__(self):
        return f"Grade {self.value} ({self.get_grade_type_display()}) — {self.created_at:%Y-%m-%d}"