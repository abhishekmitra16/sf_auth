from django.db import models

# Create your models here.

class Accounts(models.Model):

    acc_name = models.CharField(name='acc_name', max_length=50)
    acc_phone = models.CharField(name='acc_phone', max_length=20)
    acc_type = models.CharField(name="acc_type", max_length=80)
    acc_strength = models.IntegerField(name="acc_strength")

class User(models.Model):

    user_name = models.CharField(name="user_name", max_length=50)
    user_username = models.EmailField(name="user_username", max_length=50)
    user_email = models.EmailField(name="user_email", max_length=50)

class Contacts(models.Model):

    ct_id = models.CharField(name="ct_id", max_length=50, primary_key=True)
    ct_name = models.CharField(name="ct_name", max_length=50)
    ct_email = models.EmailField(name="ct_email")
    ct_dept = models.CharField(name="ct_dept", max_length=80)