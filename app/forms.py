from django import forms
from .models import Teacher, Student, SchoolClass, Subject, Grade


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['full_name', 'email', 'phone', 'degree', 'is_active']
        labels = {
            'full_name': "Full Name",
            'email': "Email",
            'phone': "Phone",
            'degree': "Academic Degree",
            'is_active': "Active",
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Teacher's full name",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@school.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1XXXXXXXXXX',
            }),
            'degree': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 7 or len(digits) > 15:
            raise forms.ValidationError(
                "Enter a valid phone number (7 to 15 digits)."
            )
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = Teacher.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "A teacher with this email already exists."
                )
        return email


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'birth_date', 'is_active']
        labels = {
            'full_name': "Full Name",
            'birth_date': "Date of Birth",
            'is_active': "Active",
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Student's full name",
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'birth_date': "Format: YYYY-MM-DD",
        }

    def clean_birth_date(self):
        from datetime import date
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = (today - birth_date).days // 365
            if birth_date > today:
                raise forms.ValidationError(
                    "Date of birth cannot be in the future."
                )
            if age > 25:
                raise forms.ValidationError(
                    "Student's age cannot exceed 25 years."
                )
        return birth_date


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['number', 'abbreviation', 'full_name', 'students']
        labels = {
            'number': "Class Number",
            'abbreviation': "Abbreviation",
            'full_name': "Full Name",
            'students': "Students",
        }
        widgets = {
            'number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 9,
                'placeholder': '1–9',
            }),
            'abbreviation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 5A',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Fifth grade, group A',
            }),
            'students': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '6',
            }),
        }
        help_texts = {
            'number': "Must be between 1 and 9.",
            'students': "Hold Ctrl (or Cmd on Mac) to select multiple students.",
        }

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if number is not None and not (1 <= number <= 9):
            raise forms.ValidationError("Class number must be between 1 and 9.")
        return number

    def clean_abbreviation(self):
        abbreviation = self.cleaned_data.get('abbreviation')
        if abbreviation:
            qs = SchoolClass.objects.filter(abbreviation__iexact=abbreviation)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "A class with this abbreviation already exists."
                )
        return abbreviation


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'students']
        labels = {
            'name': "Subject Name",
            'teacher': "Teacher",
            'students': "Students",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject name',
            }),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '6',
            }),
        }
        help_texts = {
            'students': "Hold Ctrl (or Cmd on Mac) to select multiple students.",
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            qs = Subject.objects.filter(name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "A subject with this name already exists."
                )
        return name


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['value', 'grade_type', 'students', 'subjects']
        labels = {
            'value': "Grade (1–5)",
            'grade_type': "Grade Type",
            'students': "Students",
            'subjects': "Subjects",
        }
        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': '1 to 5',
            }),
            'grade_type': forms.Select(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '6',
            }),
            'subjects': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '4',
            }),
        }
        help_texts = {
            'students': "Hold Ctrl (or Cmd on Mac) to select multiple students.",
            'subjects': "Hold Ctrl (or Cmd on Mac) to select multiple subjects.",
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value is not None and not (1 <= value <= 5):
            raise forms.ValidationError(
                "Grade must be between 1 and 5."
            )
        return value

    def clean(self):
        cleaned_data = super().clean()
        students = cleaned_data.get('students')
        subjects = cleaned_data.get('subjects')

        if not students:
            raise forms.ValidationError(
                "Please select at least one student."
            )
        if not subjects:
            raise forms.ValidationError(
                "Please select at least one subject."
            )

        return cleaned_data