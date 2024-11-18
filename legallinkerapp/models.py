from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
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
    
class ChatRoom(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chat_rooms")
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user_profile.user.username} and {self.advocate.advocate.username}"

    class Meta:
        unique_together = ('user_profile', 'advocate') 
    
class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} in {self.chat_room} at {self.created_at}"
