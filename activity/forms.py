from django import forms
from .models import Feedback
from api.models import Actives_and_project



class ManagerForm(forms.ModelForm):

    class Meta:

        model = Actives_and_project
        
        fields = (
            'first_question',
            'second_question',
            'third_question',
            'fourth_question',
            'fourth_comment_question',
            'rating',
            'comment'
        )

        labels = {
            'first_question': 'Требовалась ли тебе помощь менеджера при решении кейсов?',
            'second_question': 'Участвовал ли менеджер в решении кейсов?',
            'third_question': 'Было ли это участие полезным?',
            'fourth_question': 'Есть ли у тебя вопросы по текущему проекту, которые нужно обсудить с менеджером?',
            'fourth_comment_question': 'Вопросы по проекту:',
            'rating': 'Оцени работу менеджера в проекте по шкале от -1 до 2, где:',
            'comment': 'Комментарий (поле свободное для заполнения):',
        }

        help_texts = {
            'rating': '''-1 - неудовлетворительное качество управления проектом
                         0 - нет замечаний
                         1 - хорошее, качественное управление проектом
                         2 - сверхусилия, глубокое погружение в проект, постоянная связь с проектной командой''',  
            'comment': 'Отзыв на сотрудника'
        }
    
        widgets = {'first_question': forms.RadioSelect(attrs={'class': "cl-checkbox"}),
                   'second_question': forms.RadioSelect(attrs={'class': "cl-checkbox"}),
                   'third_question': forms.RadioSelect(attrs={'class': "cl-checkbox"}),
                   'fourth_question': forms.RadioSelect(attrs={'class': "cl-checkbox"}),
                   'fourth_comment_question': forms.Textarea(attrs={'name':'body', 'rows':5, 'cols':105, 'label': '', 'style': 'margin-top: 5px; margin-bottom: 5px;'}),
                   'comment': forms.Textarea(attrs={'name':'body', 'rows':7, 'cols':105, 'label': ''})}


    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'id': 'comment',
                                                    'class': 'form-control'})
    
        self.fields['rating'].widget.attrs.update({'id': 'rating',
                                                   'class': 'form-control'})
        
        self.fields['second_question'].widget.attrs.update({'id': 'second_question'})
        self.fields['third_question'].widget.attrs.update({'id': 'third_question'})
        self.fields['fourth_question'].widget.attrs.update({'id': 'fourth_question'})
        self.fields['fourth_comment_question'].widget.attrs.update({'id': 'fourth_comment_question',
                                                                     'class':'form-control'})
        self.fields['rating'].initial = 0
        self.fields['third_question'].required = False
        self.fields['rating'].widget.attrs['min'] = -1
        self.fields['rating'].widget.attrs['max'] = 2


class FeedbackForm(forms.ModelForm):

    class Meta:

        model = Feedback

        fields = (
            'feedback_comment',
            'rating'
        )

        labels = {
            'feedback_comment': 'Посоветуй, что нам можно улучшить!',
        }

        widgets = {
            'feedback_comment': forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':50, 'label': ''})
        }

        help_texts = {
            'feedback_comment': 'Поле свободное для заполнения.'
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback_comment'].widget.attrs.update({'id': 'feedback_comment',
                                                             'class': 'form-control'})
