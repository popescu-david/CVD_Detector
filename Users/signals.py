from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def request_admin_activation(sender, instance, **kwargs):
    if instance.pk is None:
        instance.is_active = False
        subject = "Account activation request"
        message = "User " + instance.username + " has requested account activation!"
        send_mail(subject, message,"cvddetector@noreply.com",["superuser@email.com"],fail_silently=False,)

@receiver(pre_save, sender=User)
def send_activation_notification(sender, instance, **kwargs):
    if instance.is_active and User.objects.filter(pk=instance.pk, is_active=False).exists():
        subject = "Account activated"
        message = instance.username + " your account is now active!"
        send_mail(subject, message,"cvddetector@noreply.com",[instance.email],fail_silently=False,)
