from django.db import models
from datetime import datetime

import re

# Create your models here.
print("PRINTING TIME: ", datetime.now())
# Create your models here.

now = str(datetime.now())


class UserManager(models.Manager):
    def basic_validator(self, postData):

        print("POSTDATA is", postData)

        errors = {}
        #Username Validation
        if len(postData["username"]) < 3:
            errors["username"] = "username is required!"
        elif User.objects.filter(username = postData["username"]):
            errors["username"] = "Great one, but it's already taken!"

        #Name Validation
        if len(postData["name"]) < 3:
            errors["name"] = "name is required"
        else: User.objects.filter(name = postData["name"])
            
        #Date of Birth Validation
        if not postData["dob"]:
            errors["dob"] = "date of birth is required"
        elif postData['dob'] > now:
            errors["dob"] = "You're living in the future!"

        #Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "password is required"
        if len(postData['password']) < 3:
            errors['password'] = "password needs to be atleast 3 characters long!"
        if postData['confirm_password'] != postData['password']:
            errors['password'] = "Hey, these passwords don't match!!"
        return errors

    def login_validator(self, postData):

        print("POSTDATA is", postData)

        errors = {}
        #Email Validation
        if len(postData["username"]) < 3:
            errors["username"] = "username is required"
        elif not User.objects.filter(username = postData["username"]):
            errors["username"] = "Uhm, this username was not found, please register!"

        #Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "password is required"
        return errors

class TripManager(models.Manager):

    def trip_validator(self, postData):
        errors = {}

        #Destination Validator
        print(type(postData['destination']))
        if len(postData['destination']) < 2:
            print("Empty")
            errors['destination'] = "Don't know if that's a real place?"

        #Trip Name Validator
        if len(postData['tripname']) < 1:
            errors['title'] = "Please enter longer Trip Name!"

        #Start Date Validator
        if not postData["startdate"]:
            errors["startdate"] = "When are we starting?"
        elif postData["startdate"] < now:
            errors ['startdate'] = "Uhh that date has already passed!"

        #End Date Validation
        if not postData['enddate']:
            errors["enddate"] = "I wish we could travel forever but we need to come back!"
        elif postData["enddate"] < postData["startdate"]:
            errors["enddate"] = "We can't end the trip before we started!"


        return errors


class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    #represent method
    def __repr__(self):
        return f"User: {self.id} {self.username}"



class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    tripname = models.CharField(max_length = 255)

    #ONE TO MANY RELATIONSHIP
    added_by = models.ForeignKey(User, related_name = "trips", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()

class Mytrip(models.Model):
    user = models.ForeignKey(User, related_name="user_mytrips", on_delete = models.CASCADE)
    trip = models.ForeignKey(Trip, related_name="trip_mytrips", on_delete = models.CASCADE)

# Create your models here.
