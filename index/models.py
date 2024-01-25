from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    DEPARTMENT_CHOICES = [
        ('accounts', 'Accounts'),
        ('logistics', 'Logistics'),
        ('procurement', 'Procurement'),
        ('management', 'Management'),
        ('masteruser', 'Master User'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    # Add any additional fields you need for the user profile

    def __str__(self):
        return self.user.username
  
    class Meta:
        managed = True
        db_table = 'testcase_userprofile'  

class Radio(models.Model):
  
  id = models.IntegerField(primary_key=True)
  radio = models.CharField(max_length=45)
  
  
    
  def __str__(self):
        return str(self.id)
  class Meta:
        managed = True
        db_table = 'updatelogin'  