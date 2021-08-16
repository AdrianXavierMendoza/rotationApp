# Generated by Django 3.1.7 on 2021-08-03 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musical_chairs', '0004_auto_20210803_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='crew',
            name='present',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='AttendanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendanceSheets', to='musical_chairs.captain')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crewStatus', models.BooleanField(default=True)),
                ('attendanceSheet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='musical_chairs.attendancesheet')),
                ('crew', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendaceItem', to='musical_chairs.crew')),
            ],
        ),
    ]
