from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class NoData(models.Model):
    no_data = models.CharField(max_length=20, null=True)


def get_no_data():
    return NoData.objects.get_or_create(no_data="No Data")[0]


class Department(models.Model):
    department_name = models.CharField(max_length=50, null=True, unique=True)
    is_hospital = models.BooleanField(default=True)

    def __str__(self):
        return self.department_name


class MaritalStatus(models.Model):
    status_name = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.status_name


class Gender(models.Model):
    gender_name = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.gender_name


class User(AbstractUser):
    second_name = models.CharField(max_length=20, null=True)
    pf_number = models.CharField(max_length=20, null=True, unique=True)
    phone = models.PositiveIntegerField(null=True, unique=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    is_admission = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)


class Student(models.Model):
    name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE)
    marital_status = models.ForeignKey(MaritalStatus, null=True, on_delete=models.CASCADE)
    citizenship = models.CharField(max_length=50, null=True)
    phone = models.IntegerField(unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    parent_or_guardian_name = models.CharField(max_length=50, null=True)
    parent_or_guardian_phone = models.PositiveIntegerField(null=True, blank=True)
    course_taking = models.CharField(max_length=200, null=True)
    registration_number = models.CharField(max_length=200, unique=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name + " " + self.registration_number

    def save(self, *args, **kwargs):
        self.pf_number = self.registration_number.upper()
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class Trainer(models.Model):
    name = models.CharField(max_length=50, null=True)
    pf_number = models.CharField(max_length=50, unique=True, null=True)
    phone = models.CharField(max_length=50, null=True, unique=True)
    email = models.EmailField(max_length=50, null=True, unique=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    face_encoding = models.TextField(null=True)
    is_active = models.BooleanField(default=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name + " " + self.pf_number

    def save(self, *args, **kwargs):
        self.pf_number = self.pf_number.upper()
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class Unit(models.Model):
    unit_name = models.CharField(max_length=200, null=True)
    unit_code = models.CharField(max_length=20, null=True)
    teaching_hrs_per_class = models.PositiveIntegerField(null=True)
    teaching_hrs_week = models.PositiveIntegerField(null=True)
    teaching_hrs_term = models.PositiveIntegerField(null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['unit_name']

    def __str__(self):
        return self.unit_name + " (" + self.unit_code + ")"

    def save(self, *args, **kwargs):
        self.name = self.unit_name.upper()
        super().save(*args, **kwargs)


class TrainerUnit(models.Model):
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.trainer.name + " - " + self.unit.unit_name


class TeachingAttendance(models.Model):
    trainer_unit = models.ForeignKey(TrainerUnit, null=True, on_delete=models.CASCADE)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    roll = models.CharField(max_length=20, null=True)
    clock_in_status = models.BooleanField(default=False)
    clock_out_status = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-clock_in', '-clock_out']

    def __str__(self):
        return self.trainer_unit.unit.unit_name + " class " + str(self.clock_in.astimezone())


class Staff(models.Model):
    name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE)
    marital_status = models.ForeignKey(MaritalStatus, null=True, on_delete=models.CASCADE)
    phone = models.IntegerField(unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    id_number = models.CharField(max_length=200, unique=True, null=True)
    photo = models.ImageField(upload_to='hospital_photos/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name + " " + self.id_number

    def save(self, *args, **kwargs):
        self.pf_number = self.id_number.upper()
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class Appointment(models.Model):
    sender = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=200, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.sender


class AppointmentReply(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.appointment.sender


# ==============Patient Data=========================================================
class VitalSign(models.Model):
    patient = models.CharField(max_length=100, null=True)
    sign = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class PatientComplain(models.Model):
    patient = models.CharField(max_length=100, null=True)
    complain = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class HistoryOfPresentingIllness(models.Model):
    patient = models.CharField(max_length=100, null=True)
    history = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class PastMedicalHistory(models.Model):
    patient = models.CharField(max_length=100, null=True)
    pretreatment = models.CharField(max_length=200, null=True)
    allergies = models.CharField(max_length=200, null=True)
    transfusion = models.CharField(max_length=200, null=True)
    surgeries = models.CharField(max_length=200, null=True)
    others = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class FamilyMedicalHistory(models.Model):
    patient = models.CharField(max_length=100, null=True)
    history = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Examination(models.Model):
    patient = models.CharField(max_length=100, null=True)
    examination = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Diagnosis(models.Model):
    patient = models.CharField(max_length=100, null=True)
    diagnosis = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Finding(models.Model):
    patient = models.CharField(max_length=100, null=True)
    finding = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Treatment(models.Model):
    patient = models.CharField(max_length=100, null=True)
    treatment = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
