from .utils import get_page_numbers
from django.shortcuts import render, redirect
from api.models import Actives_and_project, Cases
from django.contrib.auth.decorators import login_required
from .forms import ManagerForm, FeedbackForm
import pandas as pd
from feedback.settings import KEYS_LIMIT_TABLE, KEYS_LIMIT_PROJECT
from .models import Feedback
from django.http import HttpResponse


@login_required
def index(request):
    """Отображение главной страницы с активностями."""
    activity_list = get_filtered_activities(request)
    paginator = get_page_numbers(activity_list, request, KEYS_LIMIT_PROJECT)
    user_feedback = Feedback.objects.filter(users=request.user).first()

    user_feedback, created = Feedback.objects.get_or_create(users=request.user)
    form = FeedbackForm(request.POST or None, instance=user_feedback)
    if request.method == 'POST' and form.is_valid():
        user_feedback.rating = form.cleaned_data['rating']
        form.save()

    context = {
        'page_obj': paginator['page_obj'],
        'form': form,
        'user_feedback': user_feedback
    }

    return render(request, 'activity/index.html', context)


def get_filtered_activities(request):
    """Фильтрация активностей, по которым не заполнен отзыв (рейтинг)."""
    is_sending = 'sending' in request.path

    activities = Actives_and_project.objects.filter(
        active__users=request.user,
        rating__isnull=not is_sending
    ).order_by('name').extra(select={'length':'Length(name)'}).order_by('length')

    return activities


@login_required
def managers(request, active_id):
    """Отображение списка менеджеров для указанной активности."""
    active = Actives_and_project.objects.get(pk=active_id)

    if not active:
        return redirect('activity:index')

    cases = get_cases_by_active(request, active)
    paginator = get_page_numbers(cases, request, KEYS_LIMIT_TABLE)

    context = {
        'page_obj': paginator['page_obj'],
        'active': active,
    }

    return render(request, 'activity/managers.html', context)


@login_required
def manager_edit(request, active_id):
    """Редактирование информации о менеджере для конкретной активности."""
    active_manager = Actives_and_project.objects.filter(
        pk=active_id
    ).first()

    if not active_manager:
        return redirect('activity:index')

    form = ManagerForm(request.POST or None, instance=active_manager)

    if 'sending' in request.path:
        return render(
            request,
            'activity/manager_detail.html',
            {
                'active': active_manager
            }
        )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('activity:index')

    return render(
        request,
        'activity/manager_edit.html',
        {
            'form': form,
            'active': active_manager,
        }
    )


def standard_feedback(request, active_id):
    """Автоматическое заполнение формы отзывов для активности."""
    if request.method == "POST":
        active = Actives_and_project.objects.get(pk=active_id)
        active.first_question = "2"
        active.second_question = "2"
        active.third_question = "2"
        active.fourth_question = "2"
        active.comment = "Auto: У меня нет комментариев"
        active.rating = 0

        active.save()
        return redirect("/")

    return redirect("/")


def download_file_project(request, active_id):
    """Скачивание файла проекта для конкретной активности."""
    active = Actives_and_project.objects.get(pk=active_id)
    cases_list = Cases.objects.filter(users_id=request.user, activity_code=active.code)

    data = []
    for case in cases_list:
        data.append({
            "Код": case.code,
            "Создано": case.created_at.strftime('%Y-%m-%d %H:%M'),
            "Приоритет": case.priority,
            "Статус": case.status,
            "Тема": case.theme,
            "Описание": case.description,
            "Автор": case.author,
            "Исполнитель": case.executor,
            "Код активности": case.activity_code,
            "Название проекта": case.activity_name,
            "Описание решения": case.resolution_description,
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="cases_{active.code}.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Cases')

    return response


def get_cases_by_active(request, active_obj: Actives_and_project):
    """Получание списка кейсов по активности."""
    cases_list = Cases.objects.filter(users_id=request.user, activity_code=active_obj.code)
    return cases_list
