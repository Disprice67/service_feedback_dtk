from rest_framework import serializers
from .models import Actives_and_project, Cases
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name']


class ActivesSerializer(serializers.ModelSerializer):

    active = serializers.PrimaryKeyRelatedField(
        queryset=Cases.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = Actives_and_project
        fields = ['code', 'name', 'service_manager', 'comment',
                  'first_question', 'second_question', 'third_question',
                  'fourth_question', 'fourth_comment_question', 'rating',
                  'active']


class CasesSerializer(serializers.ModelSerializer):

    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True
    )

    class Meta:
        model = Cases
        fields = [
            'code', 'created_at', 'priority', 'status', 'theme',
            'description', 'author', 'executor', 'activity_code',
            'activity_name', 'resolution_description', 'users'
        ]
