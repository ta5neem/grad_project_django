from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


        
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.FloatField()
    time = models.FloatField()
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    total_eval = models.FloatField()
    video_id = models.OneToOneField(Video, on_delete=models.CASCADE)


class HandEval(models.Model):
    id = models.AutoField(primary_key=True)
    CLOSED_U_HANDS = models.FloatField()
    HAND_CROSSED = models.FloatField()
    HAND_ON_HIP = models.FloatField()
    HAND_ON_HEAD = models.FloatField()
    STRAIGHT_DOWN = models.FloatField()
    CLOSED_D_HANDS = models.FloatField()
    OUT_BOX = models.FloatField()
    evaluation_id =  models.OneToOneField(Evaluation, on_delete=models.CASCADE)


class Voice_Eval () :
    Voice_degree = models.FloatField()
    evaluation_id = models.OneToOneField(Evaluation, on_delete=models.CASCADE)    