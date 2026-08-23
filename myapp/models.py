from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Expert(models.Model):
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phonenumber=models.BigIntegerField()
    photo=models.CharField(max_length=300)
    qualification=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    proof=models.CharField(max_length=300)

class Patient(models.Model):
    AUTHUSER = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phonenumber=models.BigIntegerField()

class Schedule(models.Model):
    EXPERT = models.ForeignKey(Expert, on_delete=models.CASCADE)
    scheduledate=models.CharField(max_length=100)
    fromtime=models.CharField(max_length=100, default="6:00")
    totime=models.CharField(max_length=100, default="7:00")

class Complaint(models.Model):
    Date=models.DateField()
    complaint=models.CharField(max_length=100)
    EXPERT=models.ForeignKey(Expert,on_delete=models.CASCADE)
    PATIENT=models.ForeignKey(Patient,on_delete=models.CASCADE)
    reply=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class Review (models.Model):
    EXPERT=models.ForeignKey(Expert,on_delete=models.CASCADE)
    PATIENT=models.ForeignKey(Patient,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    Date=models.DateField()

class Appointment (models.Model):
    SCHEDULE=models.ForeignKey(Schedule,on_delete=models.CASCADE, default=1)
    PATIENT=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Status=models.CharField(max_length=100)
    Time=models.CharField(max_length=100)
    Date=models.DateField()


class Prediction (models.Model):
    APPOINTMENT=models.ForeignKey(Appointment,on_delete=models.CASCADE, default=1)
    Prediction=models.CharField(max_length=100)
    Filepath1=models.CharField(max_length=100)
    Filepath2=models.CharField(max_length=100)
    Date=models.DateField()

class Chat(models.Model):
    EXPERT= models.ForeignKey(Expert,on_delete=models.CASCADE,related_name="Fromid")
    USER= models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="Toid")
    message=models.CharField(max_length=100)
    Type=models.CharField(max_length=100)
    date=models.DateField()

class Education_content(models.Model):
    fpath=models.CharField(max_length=5000)
    title=models.CharField(max_length=500)
    date=models.CharField(max_length=100)