from django.db import models

class Login(models.Model):        
    id	= models.IntegerField(primary_key=True)
    username	= models.CharField(max_length=100)
    password	= models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True
        db_table = 'login'

class Logisticslogin(models.Model):        
    id	= models.IntegerField(primary_key=True)
    username	= models.CharField(max_length=100)
    password	= models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True
        db_table = 'logisticlogin'        
