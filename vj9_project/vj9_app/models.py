from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Uloge(models.Model):
    role = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.role


class Korisnik(AbstractUser):
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    status = models.CharField(max_length=50, choices=STATUS)
    role = models.ForeignKey(Uloge, on_delete=models.CASCADE, null=True)
    
class Predmeti(models.Model):
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    izborni = models.CharField(max_length=50, choices=IZBORNI)

    def __str__(self):
        return self.name

class Upisi(models.Model):
  student = models.ForeignKey(Korisnik, on_delete=models.CASCADE, null=True)
  subject = models.ForeignKey(Predmeti, on_delete=models.CASCADE, null=True)
  status = models.CharField(max_length=64)

