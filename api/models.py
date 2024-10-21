from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


YES_NO_CHOICES = [
    ('1', 'Да'),
    ('2', 'Нет'),
]

RATING_VALIDATORS = [
    MaxValueValidator(2),
    MinValueValidator(-1)
]


class Cases(models.Model):
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    priority = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    theme = models.CharField(max_length=250)
    description = models.TextField()
    author = models.CharField(max_length=100)
    executor = models.CharField(max_length=100)
    activity_code = models.CharField(max_length=20)
    activity_name = models.CharField(max_length=255)
    resolution_description = models.TextField()

    users = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='cases',
        null=True
    )

    def __str__(self):
        return f"{self.code} - {self.activity_code} {self.activity_name}"


class Actives_and_project(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    service_manager = models.CharField(max_length=100)

    comment = models.TextField(null=True, blank=True, max_length=250)
    first_question = models.CharField(max_length=1, choices=YES_NO_CHOICES, null=True, blank=False, default=None)
    second_question = models.CharField(max_length=1, choices=YES_NO_CHOICES, null=True, blank=False, default=None)
    third_question = models.CharField(max_length=1, choices=YES_NO_CHOICES, null=True, blank=False, default=None)
    fourth_question = models.CharField(max_length=1, choices=YES_NO_CHOICES, null=True, blank=False, default=None)
    fourth_comment_question = models.TextField(null=True, blank=True, max_length=250)

    rating = models.IntegerField(validators=RATING_VALIDATORS, null=True, blank=False, default=None)
    active = models.ForeignKey(
        Cases,
        on_delete=models.PROTECT,
        related_name='actives_and_project',
        null=True
    )

    def __str__(self):
        return f"{self.name}"
