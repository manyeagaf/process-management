# Generated by Django 4.0.5 on 2022-07-12 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='middle name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('branch', models.PositiveBigIntegerField(choices=[(2, 'Ebankese Branch'), (3, 'Accra Central Branch'), (4, 'Republic Court Branch'), (5, 'Kumasi Branch'), (6, 'Tema Branch'), (7, 'Legon Branch'), (8, 'Abossey Okai Branch'), (9, 'Tudu Branch'), (10, 'Techiman Branch'), (11, 'KNUST Brach'), (12, 'Tamale Branch'), (13, 'Koforidua Branch'), (14, 'Baatsona Branch'), (15, 'Private Panking'), (16, 'Ashaiman Branch'), (17, 'Takoradi Branch'), (18, 'Kasoa Branch'), (19, 'Post Office Square Branch'), (20, 'Adabraka Branch'), (21, 'Agona Swedru Branch'), (22, 'Cape Coast Branch'), (23, 'Winneba Branch'), (24, 'Asamankese Branch'), (25, 'Dansoman Branch'), (26, 'Accra Newtown Branch'), (27, 'Sefwi Wiawso'), (28, 'Essam Branch'), (29, 'Asankragua Branch'), (30, 'Sefwi Bekwai Branch '), (31, 'Akontombra Branch'), (32, 'Juaboso'), (33, 'Asempaneye Branch'), (34, 'Madina Branch'), (35, 'Goaso Branch'), (36, 'Achimota Branch'), (37, 'Asokwa Branch'), (38, 'Tema Community 25 Branch'), (39, 'Bolgatanga Branch'), (40, 'Adjiringanor Branch')], default=2)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_branch_user', models.BooleanField(default=False)),
                ('is_head_office_user', models.BooleanField(default=False)),
                ('staff_id', models.CharField(max_length=50)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'branch'), (2, 'officer'), (3, 'admin')], default=1)),
                ('date_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPrivilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.privilege')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=250)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
