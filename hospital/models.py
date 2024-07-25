from django.db import models


# # Create your models here.
# class MaritalStatus(models.Model):
#     status_name = models.CharField(max_length=20, null=True, unique=True)

#     def __str__(self):
#         return self.status_name


# class Gender(models.Model):
#     gender_name = models.CharField(max_length=20, null=True, unique=True)

#     def __str__(self):
#         return self.gender_name


# class Student(models.Model):
#     name = models.CharField(max_length=100, null=True)
#     age = models.PositiveIntegerField(null=True)
#     gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE)
#     marital_status = models.ForeignKey(MaritalStatus, null=True, on_delete=models.CASCADE)
#     citizenship = models.CharField(max_length=50, null=True)
#     phone = models.IntegerField(unique=True, null=True)
#     email = models.EmailField(max_length=50, unique=True, null=True)
#     parent_or_guardian_name = models.CharField(max_length=50, null=True)
#     parent_or_guardian_phone = models.PositiveIntegerField(null=True, blank=True)
#     course_taking = models.CharField(max_length=200, null=True)
#     registration_number = models.CharField(max_length=200, unique=True, null=True)
#     photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     created = models.DateTimeField(auto_now_add=True, null=True)
#     is_active = models.BooleanField(default=True, null=True)

#     def __str__(self):
#         return self.name + " " + self.registration_number

#     def save(self, *args, **kwargs):
#         self.pf_number = self.registration_number.upper()
#         self.name = self.name.upper()
#         super().save(*args, **kwargs)


# class Staff(models.Model):
#     name = models.CharField(max_length=100, null=True)
#     age = models.PositiveIntegerField(null=True)
#     gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE)
#     marital_status = models.ForeignKey(MaritalStatus, null=True, on_delete=models.CASCADE)
#     phone = models.IntegerField(unique=True, null=True)
#     email = models.EmailField(max_length=50, unique=True, null=True)
#     id_number = models.CharField(max_length=200, unique=True, null=True)
#     photo = models.ImageField(upload_to='hospital_photos/', blank=True, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     created = models.DateTimeField(auto_now_add=True, null=True)
#     is_active = models.BooleanField(default=True, null=True)

#     def __str__(self):
#         return self.name + " " + self.id_number

#     def save(self, *args, **kwargs):
#         self.pf_number = self.id_number.upper()
#         self.name = self.name.upper()
#         super().save(*args, **kwargs)


# class Appointment(models.Model):
#     sender = models.CharField(max_length=100, null=True)
#     message = models.CharField(max_length=200, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     created = models.DateTimeField(auto_now_add=True, null=True)
#     is_read = models.BooleanField(default=False, null=True)

#     def __str__(self):
#         return self.sender


# class AppointmentReply(models.Model):
#     appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)
#     message = models.CharField(max_length=200, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     created = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.appointment.sender
