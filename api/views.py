import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ActivesSerializer, CasesSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from feedback.settings import JWT_PASSWORD, JWT_LOGIN
from .models import Actives_and_project, Cases
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": "Пользователь с таким именем уже существует."})

        serializer.save()


class UploadActivitiesView(APIView):

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"detail": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        df = pd.read_excel(file)

        required_columns = ['Код активности', 'Название активности', 'Сервис-менеджер']
        if not all(column in df.columns for column in required_columns):
            return Response({"detail": "File must contain the required columns."}, status=status.HTTP_400_BAD_REQUEST)

        Actives_and_project.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='api_actives_and_project';")

        try:
            for user in User.objects.all()[1:]:
                username = user.first_name.replace('_', ' ').title()
                for _, row in df.iterrows():
                    activity_value = row['Код активности']
                    case = Cases.objects.filter(executor=username, activity_code=activity_value).first()

                    if not case:
                        continue

                    activity_data = {
                        'code': activity_value,
                        'name': row['Название активности'],
                        'service_manager': row['Сервис-менеджер'],
                        'comment': None,
                        'first_question': None,
                        'second_question': None,
                        'third_question': None,
                        'fourth_question': None,
                        'fourth_comment_question': None,
                        'rating': None,
                        'active': case.id
                    }

                    serializer = ActivesSerializer(data=activity_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Activities uploaded successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadCasesView(APIView):

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"detail": "File not provided."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        try:
            df = pd.read_excel(file)

            required_columns = ['Код', 'Создано', 'Приоритет', 'Статус', 'Тема', 
                                'Описание', 'Автор', 'Исполнитель', 'Активность', 
                                'Описание решения']
            if not all(column in df.columns for column in required_columns):
                return Response({"detail": "File must contain the required columns."}, status=status.HTTP_400_BAD_REQUEST)

            Cases.objects.all().delete()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='api_cases';")

            for _, row in df.iterrows():

                activity_full = row['Активность']
                engineer = row['Исполнитель'].replace(' ', '_').lower()
                activity_parts = activity_full.split(" ", 1)

                if len(activity_parts) == 2:
                    activity_code = activity_parts[0]
                    activity_name = activity_parts[1]
                else:
                    activity_code = activity_full
                    activity_name = ""

                try:
                    users = User.objects.get(first_name=engineer)
                    users_id = users.id
                except User.DoesNotExist:
                    users_id = None

                task_data = {
                    'code': row['Код'],
                    'created_at': row['Создано'],
                    'priority': row['Приоритет'],
                    'status': row['Статус'],
                    'theme': row['Тема'],
                    'description': row['Описание'],
                    'author': row['Автор'],
                    'executor': row['Исполнитель'],
                    'activity_code': activity_code,
                    'activity_name': activity_name,
                    'resolution_description': row['Описание решения'],
                    'users': users_id
                }

                serializer = CasesSerializer(data=task_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": "Tasks uploaded successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetUserFeedbackView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        project_code = request.data.get('project_code')
        service_manager = request.data.get('service_manager')

        if not username or not project_code or not service_manager:
            return Response({"detail": "Необходимо предоставить username, project_code и service_manager."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            actives_to_reset = Actives_and_project.objects.filter(
                code=project_code,
                service_manager=service_manager,
                active__users=user
            )

            if not actives_to_reset.exists():
                return Response({"detail": "Не найдены активности для сброса."}, status=status.HTTP_404_NOT_FOUND)

            actives_to_reset.update(
                comment=None,
                first_question=None,
                second_question=None,
                third_question=None,
                fourth_question=None,
                fourth_comment_question=None,
                rating=None
            )

            return Response({"detail": "Форма обратной связи для пользователя и проекта успешно сброшена."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExportActivesToExcelView(APIView):

    def get(self, request, *args, **kwargs):
        data = Actives_and_project.objects.select_related('active').values(
            'active__executor',
            'name',
            'service_manager',
            'comment',
            'first_question',
            'second_question',
            'third_question',
            'fourth_question',
            'fourth_comment_question',
            'rating'
        )

        df = pd.DataFrame(list(data))

        df.rename(columns={
            'active__executor': 'Инженер',
            'name': 'Проект',
            'service_manager': 'Менеджер',
            'comment': 'Комментарий',
            'first_question': 'Требовалась ли помощь менеджера?',
            'second_question': 'Участвовал ли менеджер в решении кейсов?',
            'third_question': 'Было ли это участие полезным?',
            'fourth_question': 'Есть ли вопросы по проекту?',
            'fourth_comment_question': 'Комментарий к вопросу 4',
            'rating': 'Оценка'
        }, inplace=True)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=actives_export.xlsx'

        df.to_excel(response, index=False)

        return response


class CustomTokenObtainPairView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if username == JWT_LOGIN and password == JWT_PASSWORD:
            user = authenticate(username=username, password=password)
            if user is not None:
                token = AccessToken.for_user(user)
                return Response({"access": str(token)}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Неверный логин или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "У вас нет прав для получения токена"}, status=status.HTTP_403_FORBIDDEN)
