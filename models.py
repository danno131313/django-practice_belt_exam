from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if User.objects.filter(email=postData['email']):
            errors['usedEmail'] = "Email address already in use"
        if len(postData['password']) < 8:
            errors['pwlength'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['password_confirm']:
            errors['pw'] = "Password didn't match"
        if (len(postData['first_name']) < 1 or len(postData['last_name']) < 1):
            errors['name'] = "First and last names must not be empty"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must be a valid email address"
        return errors

    def create_user(self, postData):
        first_name = postData['first_name']
        last_name  = postData['last_name']
        email      = postData['email']
        password   = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        
        user = self.create(first_name=first_name, last_name=last_name, email=email, password=password)
        return user

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email      = models.CharField(max_length=255)
    password   = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Comment(models.Model):
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster     = models.ForeignKey(User, related_name="comments")
    recipient  = models.ForeignKey(User, related_name="recieved_comments")

