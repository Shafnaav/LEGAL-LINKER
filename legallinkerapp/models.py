from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)  # Assuming a 6-digit PIN code

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

class Advocate(models.Model):
    advocate = models.OneToOneField(User, on_delete=models.CASCADE)
    id_card = models.CharField(max_length=100)
    practice_area = models.TextField()
    experience = models.IntegerField()  # Years of experience
    achievements = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=255)  # Languages spoken
    courts = models.TextField()  # Courts the advocate practices in
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=6)
    mobile = models.CharField(max_length=15)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Case(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    advocate = models.ForeignKey(Advocate, related_name='cases', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Open')  # Example statuses: Open, Closed, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)  # Assuming phone number as a string
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)  # To track if the message has been read

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.created_at}"