from django.db import models

# Create your models here.

class Registration(models.Model):
      Registration_ID = models.IntegerField(auto_created=True, primary_key=True)
      FirstName = models.CharField(max_length = 255)
      LastName= models.CharField(max_length = 255)
      Email = models.CharField(max_length = 255)
      MobileNo = models.IntegerField()
      Profile_Photo = models.ImageField()
      Password = models.CharField(max_length = 255)
      Created_Date = models.DateTimeField(auto_now_add = True)
      Updated_Date = models.DateTimeField(auto_now = True)

      class Meta:
          db_table = 'Registration'

class Registration_OTP(models.Model):
      Registration_OTP_ID = models.IntegerField(auto_created=True, primary_key=True)
      Email = models.CharField(max_length=50)
      otp = models.IntegerField()

      class Meta:
          db_table = 'Registration_OTP'


class Chatting(models.Model):
      Chatting_Id = models.IntegerField(auto_created=True, primary_key=True)
      Registration_Id = models.ForeignKey(Registration, on_delete=models.CASCADE)
      Message = models.TextField(max_length=5000)
      Created_Date = models.DateTimeField()

      class Meta:
          db_table = 'Chatting'