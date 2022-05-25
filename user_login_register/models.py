from django.db import models

# Create your models here.

from app_1.models import User
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
# Create your models here.






class EmailConfirmed(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key=models.CharField(max_length=255)
    email_confirmed=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural='User Email-Confirmed'

@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirmed_instance=EmailConfirmed(user=instance)
        user_encoded=f'{instance.email}-{dt}'.encode()
        activation_key=hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key=activation_key
        email_confirmed_instance.save()
