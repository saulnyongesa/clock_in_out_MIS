from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from base.forms import *


# Create your views here.
# ================Main page controls=================================
def home(request):
    return render(request, 'main.html')


@login_required(login_url='sign-in-url')
def dashboard(request):
    if request.user.is_superuser:
        students = Student.objects.all()
        trainers = Trainer.objects.all()
        units = Unit.objects.all()
        admins = User.objects.all()
        context = {
            'students': students,
            'trainers': trainers,
            'units': units,
            'admins': admins,
        }
        return render(request, 'base/index.html', context)
    else:
        return render(request, 'Error.html')


# =====================User Account controls============================
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome")
            return redirect('admin-dashboard-url')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('sign-in-url')

    return render(request, 'base/sign_in.html')


@login_required(login_url='home-url')
def sign_out(request):
    logout(request)
    return redirect('home-url')


def user_details(request):
    if request.user.is_superuser:
        form = UserDetailsForm(instance=request.user)
        return render(request, 'base/user_details.html', {'form': form})
    else:
        return render(request, 'Error.html')


def other_user_details(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id=pk)
        form = UserDetailsForm(instance=user)
        return render(request, 'base/user_other_details.html', {'form': form, 'user': user})
    else:
        return render(request, 'Error.html')


def edit_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'You edited your details successfully')
                return redirect('user-details-url')
            else:
                messages.error(request, 'Please correct the errors')
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'base/edit_user.html', {'form': form})
    else:
        return render(request, 'Error.html')


def edit_other_user(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id=pk)
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request,
                                 'You edited ' + user.first_name + ' ' + user.second_name + ' details successfully')
                return HttpResponseRedirect('/user/details/' + str(user.id))
            else:
                messages.error(request, 'Please correct the errors')
        else:
            form = UserEditForm(instance=user)
        return render(request, 'base/edit_other_user.html', {'form': form, 'user': user})
    else:
        return render(request, 'Error.html')


# ======================Department Admin sign up============================================
@login_required(login_url='clock-face-url')
def admin_signup(request):
    if request.user.is_superuser:
        departments = Department.objects.all()
        if request.method == 'POST':
            department = request.POST.get('department')
            fname = request.POST.get('fname').upper()
            sname = request.POST.get('sname').upper()
            lname = request.POST.get('lname').upper()
            username = request.POST.get('username').upper()
            pf_number = request.POST.get('pf_number').upper()
            email = request.POST.get('email').upper()
            phone = request.POST.get('phone')
            password = request.POST.get('password')

            department = Department.objects.get(id=department)
            try:
                User.objects.get(username=username)
                messages.error(request, 'Username already used')
            except User.DoesNotExist:
                admin = User.objects.create(
                    first_name=fname,
                    second_name=sname,
                    last_name=lname,
                    pf_number=pf_number,
                    username=username,
                    password=make_password(password),
                    email=email,
                    phone=phone,
                    is_admission=True if department.department_name == "ADMISSION" else False,
                    is_hospital=True if department.department_name == "HOSPITAL" else False,
                    is_pharmacy=True if department.department_name == "PHARMACY" else False,
                )

                admin.save()
                messages.success(request, "Admin for " + department.department_name + " added successful")
            return redirect('home-url')
        context = {
            "departments": departments,
        }
        return render(request, 'base/admin_signup.html', context)
    else:
        return render(request, 'Error.html')


@login_required(login_url='clock-face-url')
def admin_status(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id=pk)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, 'Admin status change.')
        return redirect('admin-list-url')
    else:
        return render(request, 'Error.html')


@login_required(login_url='clock-face-url')
def admin_list(request):
    if request.user.is_superuser:
        list_choice = 0
        users = User.objects.all()
        if request.method == 'POST':
            choice = request.POST.get('choice')
            if int(choice) == 0:
                return redirect('admin-list-url')
            elif int(choice) == 1:
                return redirect('admin-list-active-url')
            elif int(choice) == 2:
                return redirect('admin-list-inactive-url')
        return render(request, 'base/admin_list.html',
                      {
                          'users': users,
                          'list_choice': list_choice})
    else:
        return render(request, 'Error.html')


@login_required(login_url='clock-face-url')
def admin_list_active_only(request):
    if request.user.is_superuser:
        list_choice = 1
        users = User.objects.filter(
            is_active=True
        )
        return render(request, 'base/admin_list.html',
                      {
                          'users': users,
                          'list_choice': list_choice})
    else:
        return render(request, 'Error.html')


@login_required(login_url='clock-face-url')
def admin_list_inactive_only(request):
    if request.user.is_superuser:
        list_choice = 2
        users = User.objects.filter(
            is_active=False
        )
        return render(request, 'base/admin_list.html',
                      {
                          'users': users,
                          'list_choice': list_choice})
    else:
        return render(request, 'Error.html')
