# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bcrypt
import re

from django.db import models


LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
class UserManager(models.Manager):
    def register_val(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name']= "Blog name should be more than 2 characters"
        elif not LETTER_REGEX.match(postData["first_name"]):
            errors["first_name_valid"] = "First name must be letters only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Blog name should be more than 2 characters"
        elif not LETTER_REGEX.match(postData["last_name"]):
            errors["last_name_valid"] = "Last name must be letters only"

        if not EMAIL_REGEX.match(postData["email"]):
            errors["email_valid"] = "Email entered is invalid"
        
        if len(postData["password"]) < 8:
            errors["password"] = "Must be 8 characters long"
        elif postData["password"]!= postData["confirm_password"]:
            errors['password'] = "Passwords do not match"

        if not errors and User.objects.filter(email=postData["email"]):
            errors["email_valid"] = "Email is already registered"
        
        return errors
    
    def login_val(self, postData):
        errors = {}
        users = User.objects.filter(email= postData['email'])
        if not users:
            errors['login'] = "Email not found"
        else:
            user = users[0]
            if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
                errors["login"] = "Incorrect password"
        
        if not errors:
            return user

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()

    def __repr__(self):
        return "<User object:{} {} {} {}>".format(self.first_name, self.last_name, self.email, self.password)
    
