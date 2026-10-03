from django.db import models

# Create your models here.

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name} Team'

class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "A", "Admin"
        EMPLOYEE = "E", "Employer"
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.firstname} { self.lastname}'

class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "N", "New"
        COMPLETED = "C", "Completed"
        IN_PROCESS = "I", "In process"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    destination_date = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.NEW,
    )
    responsible = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title