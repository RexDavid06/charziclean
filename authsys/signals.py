from django.dispatch import receiver 
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from authsys.models import UserProfile

@receiver(post_save, sender=User)
def profile_build(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def profile_save(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
        