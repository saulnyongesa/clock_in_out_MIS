from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from collections import defaultdict

from base.forms import *
from app.models import *


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        all_appointments = Appointment.objects.all()
        active_appointments = Appointment.objects.filter(is_read=False)
        students = Student.objects.all()
        staffs = Staff.objects.all()
        patients = students.count() + staffs.count()
        context = {
            'patients': patients,
            'all_appointments': all_appointments,
            'active_appointments': active_appointments,
        }
        return render(request, 'hospital/index.html', context)
    else:
        if request.method == 'POST':
            sender = None
            data = request.POST.get('input').upper()
            try:
                try:
                    student = Student.objects.get(registration_number=data)
                    sender = student
                    return HttpResponseRedirect('/hospital/appointment/send/' + str(sender.id))
                except Student.DoesNotExist:
                    staff = Staff.objects.get(id_number=data)
                    sender = staff
                    return HttpResponseRedirect('/hospital/appointment/send/' + str(sender.id))
            except Student.DoesNotExist and Staff.DoesNotExist:
                messages.error(request, 'You are not register Or You have entered a wrong ID/REG Number.')
                return redirect('sender-type-url')

        return render(request, 'hospital/appointment_b4_send.html')


# Student and Staff information=============================================================================
def sender_type(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        choice = int(choice)
        if choice == 1:
            return redirect('student-self-signup-url')
        else:
            return redirect('staff-self-signup-url')

    return render(request, 'hospital/sender.html')


def student_signup(request):
    form = StudentSignupForm()
    if request.method == "POST":
        form = StudentSignupForm(request.POST, request.FILES)
        registration_number = request.POST.get('registration_number').upper()
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Saved successfully')
            print(registration_number)
            sender = Student.objects.get(registration_number=registration_number)
            return HttpResponseRedirect('/hospital/appointment/send/' + str(sender.id))
            # return redirect('send-appointment-url')
    context = {
        'form': form,
    }
    return render(request, 'hospital/student/student_signup.html', context)


def staff_signup(request):
    form = StaffSignupForm
    if request.method == "POST":
        form = StaffSignupForm(request.POST, request.FILES)
        id_number = request.POST.get('id_number').upper()
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Saved successfully')
            sender = Staff.objects.get(id_number=id_number)
            return HttpResponseRedirect('/hospital/appointment/send/' + str(sender.id))
            # return redirect('send-appointment-url')
    context = {
        'form': form,
    }
    return render(request, 'hospital/student/staff_signup.html', context)


# ===========Appointments===========================================
def all_appointments(request):
    students = Student.objects.all()
    staffs = Staff.objects.all()
    appointments = Appointment.objects.all()
    replies = AppointmentReply.objects.all()
    context = {
        'appointments': appointments,
        'students': students,
        'staffs': staffs,
        'replies': replies,
    }
    return render(request, 'hospital/appointments_all.html', context)


def send_appointment(request, pk):
    sender = None
    patient = None
    try:
        try:
            student = Student.objects.get(id=pk)
            sender = student
            patient = sender.registration_number
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            sender = staff
            patient = sender.id_number
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'An Error Occurred! Try Again')
        return redirect('hospital-dashboard-url')
    if request.method == 'POST':
        message = request.POST.get('message')

        appointment = Appointment.objects.create(
            sender=patient,
            message=message
        )
        appointment.save()
        messages.success(request, "Appointment Sent! You'll get a reply email")
        return redirect('hospital-dashboard-url')
    appointments = Appointment.objects.filter(sender=patient)
    replies = AppointmentReply.objects.all()
    context = {
        'appointments': appointments,
        'replies': replies,
        'patient': patient,
        'sender': sender,
    }
    return render(request, 'hospital/appointment_send.html', context)


def active_appointments(request):
    students = Student.objects.all()
    staffs = Staff.objects.all()
    active_appointments = Appointment.objects.filter(is_read=False)
    context = {
        'active_appointments': active_appointments,
        'students': students,
        'staffs': staffs,
    }
    return render(request, 'hospital/appointments_active.html', context)


def view_appointment(request, pk):
    sender = None
    appointment = Appointment.objects.get(id=pk)
    try:
        try:
            student = Student.objects.get(registration_number=appointment.sender)
            sender = student
        except Student.DoesNotExist:
            staff = Staff.objects.get(id_number=appointment.sender)
            sender = staff
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'An Error Occurred!')
    context = {
        'appointment': appointment,
        'sender': sender
    }
    return render(request, 'hospital/appointment_approve.html', context)


def reply_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == 'POST':
        message = request.POST.get('reply')
        sender = None
        try:
            try:
                student = Student.objects.get(registration_number=appointment.sender)
                sender = student
            except Student.DoesNotExist:
                staff = Staff.objects.get(id_number=appointment.sender)
                sender = staff
        except Student.DoesNotExist and Staff.DoesNotExist:
            messages.error(request, 'An Error Occurred!')

        AppointmentReply.objects.create(
            appointment=appointment,
            message=message
        )
        appointment.is_read = True
        appointment.save()
        send_mail(
            "Appointment Approval",
            message,
            request.user.email,
            [sender.email],
            fail_silently=True,
        )
        messages.success(request, 'Reply Sent Successfully!')
        return redirect('active-appointments-url')
    context = {
        'appointment': appointment,
    }
    return render(request, 'hospital/appointment_approve.html', context)


# =====================User Account controls============================
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome")
            return redirect('hospital-dashboard-url')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('hospital-sign-in-url')

    return render(request, 'hospital/sign_in.html')


@login_required(login_url='hospital-dashboard-url')
def sign_out(request):
    logout(request)
    return redirect('hospital-sign-in-url')


def user_details(request):
    if request.user.is_superuser:
        form = UserDetailsForm(instance=request.user)
        return render(request, 'hospital/user_details.html', {'form': form})
    else:
        return render(request, '')


def edit_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'You edited your details successfully')
                return redirect('user-hospital-details-url')
            else:
                messages.error(request, 'Please correct the errors')
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'hospital/edit_user.html', {'form': form})
    else:
        return render(request, '')
    

# ==============Patient Data=========================================================
def patient_search(request):
    if request.method == 'POST':
        patient = None
        data = request.POST.get('input').upper()
        try:
            try:
                student = Student.objects.get(registration_number=data)
                patient = student
                return HttpResponseRedirect('/hospital/medical-records/bio/' + str(patient.id))
            except Student.DoesNotExist:
                staff = Staff.objects.get(id_number=data)
                patient = staff
                return HttpResponseRedirect('/hospital/medical-records/bio/' + str(patient.id))
        except Student.DoesNotExist and Staff.DoesNotExist:
            messages.error(request, 'Patient Not registered Or You have entered a wrong ID/REG Number.')
            return redirect('patient-type-url')
    return render(request, 'hospital/index.html')


def patient_type(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        choice = int(choice)
        if choice == 1:
            return redirect('student-medical-signup-url')
        else:
            return redirect('staff-medical-signup-url')

    return render(request, 'hospital/medical_record/before_medical_patient_register.html')


def student_medical_signup(request):
    form = StudentSignupForm()
    if request.method == "POST":
        form = StudentSignupForm(request.POST, request.FILES)
        registration_number = request.POST.get('registration_number').upper()
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Saved successfully')
            print(registration_number)
            patient = Student.objects.get(registration_number=registration_number)
            return HttpResponseRedirect('/hospital/medical-records/' + str(patient.id))
    context = {
        'form': form,
    }
    return render(request, 'hospital/medical_record/student_signup.html', context)


def staff_medical_signup(request):
    form = StaffSignupForm
    if request.method == "POST":
        form = StaffSignupForm(request.POST, request.FILES)
        id_number = request.POST.get('id_number').upper()
        if form.is_valid():
            form.save()
            messages.success(request, 'Details Saved successfully')
            patient = Staff.objects.get(id_number=id_number)
            return HttpResponseRedirect('/hospital/medical-records/' + str(patient.id))
    context = {
        'form': form,
    }
    return render(request, 'hospital/medical_record/staff_signup.html', context)


def bio_data(request, pk):
    patient = None
    form = None
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            form = StudentDataForm(instance=student)
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            form = StaffDataForm(instance=staff)
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    context = {
        'patient': patient,
        'form': form,
    }
    return render(request, 'hospital/medical_record/bio_data.html', context)


def vital_signs(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            vital_saved_signs = VitalSign.objects.filter(patient=save_patient).order_by('-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            vital_saved_signs = VitalSign.objects.filter(patient=save_patient).order_by('-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_vital_signs = defaultdict(list)
    for vital_sign in vital_saved_signs:
        date_str = vital_sign.created.strftime('%Y-%m-%d')
        grouped_vital_signs[date_str].append(vital_sign)
    grouped_vital_signs = dict(grouped_vital_signs)
    if request.method == 'POST':
        v_signs = request.POST.getlist('vital_signs')

        for vital_sign in v_signs:
            if vital_sign:
                v = VitalSign.objects.create(
                    patient=save_patient,
                    sign=vital_sign
                )
                v.save()
        messages.success(request, "Patient's Vital Signs Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/vital-signs/' + str(patient.id))
    context = {
        'patient': patient,
        'vital_signs': grouped_vital_signs,
    }
    return render(request, 'hospital/medical_record/vital_signs.html', context)


def complains(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            patient_complains_saved = PatientComplain.objects.filter(patient=save_patient).order_by('-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            patient_complains_saved = PatientComplain.objects.filter(patient=save_patient).order_by('-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_complains = defaultdict(list)
    for complain in patient_complains_saved:
        date_str = complain.created.strftime('%Y-%m-%d')
        grouped_complains[date_str].append(complain)
    grouped_complains = dict(grouped_complains)
    if request.method == 'POST':
        patient_complains = request.POST.getlist('vital_signs')

        for complain in patient_complains:
            if complain:
                v = PatientComplain.objects.create(
                    patient=save_patient,
                    complain=complain
                )
                v.save()
        messages.success(request, "Patient's Complains Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/complains/' + str(patient.id))
    context = {
        'patient': patient,
        'complains': grouped_complains,
    }
    return render(request, 'hospital/medical_record/complains.html', context)


def hpi(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            patient_hpi_saved = HistoryOfPresentingIllness.objects.filter(patient=save_patient).order_by('-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            patient_hpi_saved = HistoryOfPresentingIllness.objects.filter(patient=save_patient).order_by('-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_hpi = defaultdict(list)
    for hpi_ in patient_hpi_saved:
        date_str = hpi_.created.strftime('%Y-%m-%d')
        grouped_hpi[date_str].append(hpi_)
    grouped_hpi = dict(grouped_hpi)
    if request.method == 'POST':
        patient_hpi = request.POST.getlist('vital_signs')

        for hpi_ in patient_hpi:
            if hpi_:
                v = HistoryOfPresentingIllness.objects.create(
                    patient=save_patient,
                    history=hpi_
                )
                v.save()
        messages.success(request, "Patient's HPI Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/hpi/' + str(patient.id))
    context = {
        'patient': patient,
        'hpis': grouped_hpi,
    }
    return render(request, 'hospital/medical_record/HPI.html', context)


def past_medical_history(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            patient_med_history_saved = PastMedicalHistory.objects.filter(patient=save_patient).order_by('-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            patient_med_history_saved = PastMedicalHistory.objects.filter(patient=save_patient).order_by('-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_pmh = defaultdict(list)
    for pmh in patient_med_history_saved:
        date_str = pmh.created.strftime('%Y-%m-%d')
        grouped_pmh[date_str].append(pmh)
    grouped_pmh = dict(grouped_pmh)
    if request.method == 'POST':
        pretreatment = request.POST.getlist('pretreatment')
        allergies = request.POST.getlist('allergies')
        transfusion = request.POST.getlist('transfusion')
        surgeries = request.POST.getlist('surgeries')
        others = request.POST.getlist('others')
        v = PastMedicalHistory.objects.create(
            patient=save_patient,
            pretreatment=pretreatment,
            allergies=allergies,
            transfusion=transfusion,
            surgeries=surgeries,
            others=others
        )
        v.save()
        messages.success(request, "Patient's Past Medical History Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/past-medical-history/' + str(patient.id))
    context = {
        'patient': patient,
        'past_medical_records': grouped_pmh
    }
    return render(request, 'hospital/medical_record/past_medical_record.html', context)


def family_medical_history(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            family_saved_medical_records = FamilyMedicalHistory.objects.filter(patient=save_patient).order_by('-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            family_saved_medical_records = FamilyMedicalHistory.objects.filter(patient=save_patient).order_by('-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_fmhs = defaultdict(list)
    for family_saved_medical_record in family_saved_medical_records:
        date_str = family_saved_medical_record.created.strftime('%Y-%m-%d')
        grouped_fmhs[date_str].append(family_saved_medical_record)
    grouped_fmhs = dict(grouped_fmhs)
    if request.method == 'POST':
        fmhs = request.POST.getlist('vital_signs')

        for fmhs in fmhs:
            if fmhs:
                v = FamilyMedicalHistory.objects.create(
                    patient=save_patient,
                    history=fmhs
                )
                v.save()
        messages.success(request, "Patient's Family Medical History Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/family-medical-history/' + str(patient.id))
    context = {
        'patient': patient,
        'family_medical_records': grouped_fmhs
    }
    return render(request, 'hospital/medical_record/family_medical_record.html', context)


def examination(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            examination_saved_records = Examination.objects.filter(patient=save_patient).order_by(
                '-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            examination_saved_records = Examination.objects.filter(patient=save_patient).order_by(
                '-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_examinations = defaultdict(list)
    for examination_saved_record in examination_saved_records:
        date_str = examination_saved_record.created.strftime('%Y-%m-%d')
        grouped_examinations[date_str].append(examination_saved_record)
    grouped_examinations = dict(grouped_examinations)
    if request.method == 'POST':
        examination_inputs = request.POST.getlist('vital_signs')

        for examination_input in examination_inputs:
            if examination_input:
                v = Examination.objects.create(
                    patient=save_patient,
                    examination=examination_input
                )
                v.save()
        messages.success(request, "Patient's Medical Examination Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/examination/' + str(patient.id))
    context = {
        'patient': patient,
        'medical_examination_records': grouped_examinations
    }
    return render(request, 'hospital/medical_record/examination.html', context)


def diagnosis(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            diagnosis_saved_records = Diagnosis.objects.filter(patient=save_patient).order_by(
                '-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            diagnosis_saved_records = Diagnosis.objects.filter(patient=save_patient).order_by(
                '-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_diagnosis_s = defaultdict(list)
    for diagnosis_saved_record in diagnosis_saved_records:
        date_str = diagnosis_saved_record.created.strftime('%Y-%m-%d')
        grouped_diagnosis_s[date_str].append(diagnosis_saved_record)
    grouped_diagnosis_s = dict(grouped_diagnosis_s)
    if request.method == 'POST':
        diagnosis_inputs = request.POST.getlist('vital_signs')

        for diagnosis_input in diagnosis_inputs:
            if diagnosis_input:
                v = Diagnosis.objects.create(
                    patient=save_patient,
                    diagnosis=diagnosis_input
                )
                v.save()
        messages.success(request, "Patient's Medical diagnosis Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/diagnosis/' + str(patient.id))
    context = {
        'patient': patient,
        'medical_diagnosis_records': grouped_diagnosis_s
    }
    return render(request, 'hospital/medical_record/diagnosis.html', context)


def findings(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            finding_saved_records = Finding.objects.filter(patient=save_patient).order_by(
                '-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            finding_saved_records = Finding.objects.filter(patient=save_patient).order_by(
                '-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_findings = defaultdict(list)
    for finding_saved_record in finding_saved_records:
        date_str = finding_saved_record.created.strftime('%Y-%m-%d')
        grouped_findings[date_str].append(finding_saved_record)
    grouped_findings = dict(grouped_findings)
    if request.method == 'POST':
        finding_inputs = request.POST.getlist('vital_signs')

        for finding_input in finding_inputs:
            if finding_input:
                v = Finding.objects.create(
                    patient=save_patient,
                    finding=finding_input
                )
                v.save()
        messages.success(request, "Patient's Medical Diagnosis Finding Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/findings/' + str(patient.id))
    context = {
        'patient': patient,
        'medical_finding_records': grouped_findings
    }
    return render(request, 'hospital/medical_record/finding.html', context)


def treatment(request, pk):
    try:
        try:
            student = Student.objects.get(id=pk)
            patient = student
            save_patient = patient.registration_number
            treatment_saved_records = Treatment.objects.filter(patient=save_patient).order_by(
                '-created')
        except Student.DoesNotExist:
            staff = Staff.objects.get(id=pk)
            patient = staff
            save_patient = patient.id_number
            treatment_saved_records = Treatment.objects.filter(patient=save_patient).order_by(
                '-created')
    except Student.DoesNotExist and Staff.DoesNotExist:
        messages.error(request, 'Patient Not registered Or You entered wrong ID/REG Number.')
        return redirect('hospital-dashboard-url')
    grouped_treatments = defaultdict(list)
    for treatment_saved_record in treatment_saved_records:
        date_str = treatment_saved_record.created.strftime('%Y-%m-%d')
        grouped_treatments[date_str].append(treatment_saved_record)
    grouped_treatments = dict(grouped_treatments)
    if request.method == 'POST':
        treatment_inputs = request.POST.getlist('vital_signs')

        for treatment_input in treatment_inputs:
            if treatment_input:
                v = Treatment.objects.create(
                    patient=save_patient,
                    treatment=treatment_input
                )
                v.save()
        messages.success(request, "Patient's Medical Treatment Record Saved Successfully")
        return HttpResponseRedirect('/hospital/medical-records/treatment/' + str(patient.id))
    context = {
        'patient': patient,
        'medical_treatment_records': grouped_treatments
    }
    return render(request, 'hospital/medical_record/treatment.html', context)
