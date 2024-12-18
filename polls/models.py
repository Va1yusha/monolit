from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

# модель Question
class Question(models.Model):
    question_text = models.CharField(max_length=200)  # Поле для текста вопроса макс длина 200 символов
    pub_date = models.DateTimeField('date published')  # Поле для даты публикации вопроса
    image = models.ImageField(upload_to='questions/', blank=True, null=True)  # Поле для изображения вопроса может быть пустым


    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


    def __str__(self):
        return self.question_text

#  модель Choice
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Связываем выбор с вопросом
    choice_text = models.CharField(max_length=200)  # Поле для текста варианта ответа
    votes = models.IntegerField(default=0)  # Поле для хранения количества голосов по умолчанию 0

    # Метод для строкового представления объекта Choice
    def __str__(self):
        return self.choice_text  # Возвращает текст варианта ответа

# модель UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')  # Связываем профиль с пользователем
    bio = models.TextField(blank=True, default="")  # Поле для биографии пользователя может быть пустым
    avatar = models.ImageField(upload_to='user_avatars', blank=True)  # Поле для хранения аватара пользователя

    # Метод для строкового представления объекта UserProfile
    def __str__(self):
        return f'{self.user} Profile'  # Возвращает строку с именем пользователя

# модель Vote
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связываем голос с пользователем
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Связываем голос с вопросом
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Связываем голос с вариантом ответа

    class Meta:
        unique_together = ('user', 'question')  # Ограничение на уникальность: один пользователь может голосовать за один вопрос только один раз