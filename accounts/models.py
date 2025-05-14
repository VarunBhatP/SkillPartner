from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    USER_TYPES = [
        ('learner', 'Learner'),
        ('mentor', 'Mentor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.learner.username} -> {self.mentor.username} ({self.skill.name})"
