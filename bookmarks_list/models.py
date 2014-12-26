
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save



class Link(models.Model):
  name = models.CharField(max_length=50)
  link_url = models.URLField()
  date_created = models.DateTimeField()
  date_modified = models.DateTimeField()
  tag = models.TextField(null=True, blank=True)
  def __str__(self):             
    return self.name

class List(models.Model):
  name = models.CharField(max_length=50)
  date_created = models.DateTimeField()
  date_modified = models.DateTimeField()
  link = models.ManyToManyField(Link)
  def __str__(self):             
      return self.name

class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True)
  internal_id = models.CharField(max_length=25,null=True, blank=True)
  verified = models.BooleanField(default=False)
  approval_date = models.DateTimeField(null=True, blank=True)
  def __str__(self):             
      return self.user.username
  
 
class ListForm(forms.Form):
  name = forms.CharField(label='Name', max_length=50)

class LinkForm(forms.Form):
   name = forms.CharField(label='Name', max_length=50)
   url = forms.URLField(label='URL')
   tag = forms.CharField(label='Tag', required=False)

class LoginForm(forms.Form):
  username = forms.CharField(label="Username")
  password = forms.CharField(label="Password", widget=forms.PasswordInput())

class RegisterForm(forms.Form):
  username = forms.CharField(label="Username")
  password = forms.CharField(label="Password", widget=forms.PasswordInput())





