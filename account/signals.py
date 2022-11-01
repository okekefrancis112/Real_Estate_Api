# from django.db.models.signals import post_save,pre_save
# # from django.core.signals import request_started
# from django.dispatch import receiver

# from goldapi.models import Realtor

# from .models import User



# @receiver(post_save, sender=User)
# def create_related_realtor(sender, instance, created, *args, **kwargs):
#     # Notice that we're checking for `created` here. We only want to do this
#     # the first time the `User` instance is created. If the save that caused
#     # this signal to be run was an update action, we know the user already
#     # has a profile.
#     print("Post save",instance)
#     if instance and created:
#         instance.realtor = Realtor.objects.create(realtor=instance)