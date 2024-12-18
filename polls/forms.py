from django import forms  # Импортируем базовый класс форм из Django.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Импортируем формы для создания пользователей и аутентификации.
from django.contrib.auth.models import User  # Импортируем модель пользователя из встроенной системы аутентификации Django.
from .models import Question, Choice  # Импортируем модели Question и Choice из текущего приложения.

# форма для вопросов
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # Указываем, что это форма будет с моделью Question
        fields = ['question_text', 'image']  # Определяем поля которые будут включены в форму

# Определяем форму для создания и редактирования вариантов ответов
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice  # Указываем что это модель Choice
        fields = ['choice_text']  # Определяем поля которые будут включены в форму

# Определяем форму регистрации пользователя, наследуя от UserCreationForm.
class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField()  # Добавляем поле для загрузки аватара пользователя.

    class Meta:
        model = User  # Указываем что это модель User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')  # Определяем поля которые будут включены в форму

# Определяем форму для редактирования профиля пользователя
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User  #
        fields = ('username', 'email', 'first_name', 'last_name')  # Определяем поля которые будут включены в форму

    avatar = forms.ImageField(label="Аватар", required=False)  # Добавляем поле для загрузки аватара пользователя

# функция входа
class LoginForm(AuthenticationForm):
    pass  # Используем стандартную функциональность AuthenticationForm без изменений

# функция удаления
class DeleteAccountForm(forms.Form):
    confirm_delete = forms.BooleanField(label='Удалить аккаунт', required=True)  # Поле для подтверждения удаления аккаунта обязательное для заполнения