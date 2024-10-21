from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Feedback(models.Model):

    users = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='feedback'
    )

    rating = models.IntegerField(null=True, blank=False)
    feedback_comment = models.TextField(null=True, blank=True, max_length=250)
