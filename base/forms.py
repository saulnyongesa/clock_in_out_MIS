from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from app.models import *


# for admissions signup
class PWDChangeView(PasswordChangeView):
    form = PasswordChangeForm
    success_url = reverse_lazy('home-url')


class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class StaffSignupForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class TrainerSignupForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'pf_number', 'phone', 'email', 'photo']


class FaceAuthenticationForm(forms.Form):
    face_image = forms.ImageField()


class TrainerAssignToUnitForm(forms.ModelForm):
    class Meta:
        model = TrainerUnit
        fields = '__all__'


class TrainerLoginForm(forms.Form):
    pf_number = forms.CharField(max_length=50)
    photo = forms.ImageField(required=True)


class UnitSignupForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['teaching_hrs_per_class']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'last_name', 'pf_number', 'username', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'last_name', 'pf_number', 'username', 'phone', 'email']


# =========For medical===============
class StudentDataForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['photo', 'is_active']

    def __init__(self, *args, **kwargs):
        super(StudentDataForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class StaffDataForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['photo', 'is_active']

    def __init__(self, *args, **kwargs):
        super(StaffDataForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True