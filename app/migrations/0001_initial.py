# Generated by Django 5.0.7 on 2024-07-11 09:48

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=50, null=True, unique=True)),
                ('is_admission', models.BooleanField(default=True)),
                ('is_hospital', models.BooleanField(default=True)),
                ('is_pharmacy', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender_name', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_data', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('pf_number', models.CharField(max_length=50, null=True, unique=True)),
                ('phone', models.CharField(max_length=50, null=True, unique=True)),
                ('email', models.EmailField(max_length=50, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('face_encoding', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=200, null=True)),
                ('unit_code', models.CharField(max_length=20, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['unit_name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('second_name', models.CharField(max_length=20, null=True)),
                ('pf_number', models.CharField(max_length=20, null=True, unique=True)),
                ('phone', models.PositiveIntegerField(null=True, unique=True)),
                ('email', models.CharField(max_length=50, null=True, unique=True)),
                ('is_admission', models.BooleanField(default=False)),
                ('is_hospital', models.BooleanField(default=False)),
                ('is_pharmacy', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('age', models.PositiveIntegerField(null=True)),
                ('citizenship', models.CharField(max_length=50, null=True)),
                ('phone', models.IntegerField(null=True, unique=True)),
                ('email', models.EmailField(max_length=50, null=True, unique=True)),
                ('parent_or_guardian_name', models.CharField(max_length=50, null=True)),
                ('parent_or_guardian_phone', models.PositiveIntegerField(blank=True, null=True)),
                ('course_taking', models.CharField(max_length=200, null=True)),
                ('registration_number', models.CharField(max_length=200, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='studentphotos/')),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.gender')),
                ('marital_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.maritalstatus')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.trainer')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.unit')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in', models.DateTimeField(blank=True, null=True)),
                ('clock_out', models.DateTimeField(blank=True, null=True)),
                ('roll', models.CharField(max_length=20, null=True)),
                ('clock_in_status', models.BooleanField(default=False)),
                ('clock_out_status', models.BooleanField(default=False)),
                ('time_taken', models.PositiveIntegerField(blank=True, null=True)),
                ('trainer_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.trainerunit')),
            ],
            options={
                'ordering': ['-clock_in', '-clock_out'],
            },
        ),
    ]
