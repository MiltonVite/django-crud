from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100) #va a ser un texto corto

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField() #va a ser un texto largo
    project = models.ForeignKey(Project, on_delete=models.CASCADE) #relacion de uno a muchos
    done = models.BooleanField(default=False) #va a ser un booleano
    def __str__(self):
        return self.title + ' - ' + self.project.name 