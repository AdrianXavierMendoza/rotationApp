from __future__ import unicode_literals
from django.db import models
import re
import bcrypt


class CaptainManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData['sname']) < 2:
            errors["sname"] = "Last name should be at least 2 characters"

# # Email validations
#         EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#         captain = Captain.objects.filter(email=postData['email'])
#         if len(captain) > 0:
#             errors["email"] = "Email already exist"
#         if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
#             errors['email'] = ("Invalid email address!")

# Validating a password
        PW_REGEX = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})")
        if len(postData['pw']) < 8:
            errors["pw"] = "Show description should be at least 10 characters"
        # test whether a field matches the pattern
        if not PW_REGEX.match(postData['pw']):
            errors['pw'] = ("Password did not meet requirements!")
        if postData['confirm_pw'] != postData['pw']:
            errors['confirm_pw'] = "Passwords do not match"

# Cross checking referal code
        # if postData['code'] != 1234:
        #     errors['code'] = "Referal code incorrect"

# ...
        return errors

    def gatekeeper(self, postData):
        errors = {}
        captain = Captain.objects.filter(code=postData['code'])
        if len(captain) < 1:
            errors['code'] = "Captain does not exist"
        else:
            if not bcrypt.checkpw(postData['pw'].encode('utf-8'), captain[0].pw.encode('utf-8')):
                errors['invalidpw'] = 'Invalid Password'
        return errors


class Captain(models.Model):
    fname = models.CharField(max_length=20)
    sname = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    pw = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CaptainManager()

    def __str__(self):
        return str(self.code + ' ' + self.fname + ' ' + self.sname)


class Crew(models.Model):
    captain = models.ForeignKey(
        Captain, related_name='captains', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    skills = models.IntegerField(default=0)
    present = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Task(models.Model):
    task = models.CharField(max_length=20)
    captain = models.ForeignKey(
        Captain, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.task)


class Status(models.Model):

    NONE = '...'
    TRAINING = 'Training'
    NOVICE = 'Novice'
    MASTER = 'Master'
    RESTRICTED = 'Restricted'

    CREW_STATUS = [
        (NONE, '...'),
        (TRAINING, 'Training'),
        (NOVICE, 'Novice'),
        (MASTER, 'Master'),
        (RESTRICTED, 'Restricted')
    ]
    status = models.CharField(
        choices=CREW_STATUS, max_length=100, default=NONE)
    task = models.ForeignKey(
        Task, related_name='tasker', on_delete=models.CASCADE)
    crew = models.ForeignKey(
        Crew, related_name='crewStatus', on_delete=models.CASCADE)
    captain = models.ForeignKey(
        Captain, related_name='captain', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.crew.name + ' is ' + self.status + ' at ' + self.task.task)

class AttendanceSheet(models.Model):
    date = models.DateTimeField()
    captain = models.ForeignKey(
        Captain, related_name='attendanceSheets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date)

    # @property
    # def get_total(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.get_total for item in orderitems])
    #     return total


class AttendanceItem(models.Model):
    attendanceSheet = models.ForeignKey(AttendanceSheet, on_delete=models.SET_NULL, null=True)
    crew = models.ForeignKey(
        Crew, related_name='attendaceItem', on_delete=models.SET_NULL, null=True)
    crewStatus = models.BooleanField(default=True)

    def __str__(self):
        return str(self.crew.name + ' is ' + self.crewStatus + ' with  ' + self.attendanceSheet.captain.name)