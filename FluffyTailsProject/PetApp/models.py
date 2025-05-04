from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Species(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  


class Breeds(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey(Species, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  


class Pet(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    breeds = models.ManyToManyField(Breeds)  
    age = models.IntegerField(default=0) 
    image = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    adopted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pets = models.ManyToManyField(Pet)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ], default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username} Profile"
