from django.contrib import admin

from app.models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(MaritalStatus)
admin.site.register(Gender)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Trainer)
admin.site.register(Unit)
admin.site.register(TeachingAttendance)
admin.site.register(TrainerUnit)
admin.site.register(Staff)
admin.site.register(Appointment)
admin.site.register(AppointmentReply)
admin.site.register(VitalSign)
admin.site.register(PatientComplain)
admin.site.register(HistoryOfPresentingIllness)
admin.site.register(PastMedicalHistory)
admin.site.register(FamilyMedicalHistory)
admin.site.register(Examination)
admin.site.register(Diagnosis)
admin.site.register(Finding)
admin.site.register(Treatment)
