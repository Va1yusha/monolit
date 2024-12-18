from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, DeleteAccountForm,QuestionForm, ChoiceForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, UserProfile, Vote
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Пользователь а именно: Регистрация, Авторизация, Выход из акаунта, Удаление акаунта

def login_view(request):  # функция входа
    if request.method == 'POST':  # проверка на запрос методом POST
        form = LoginForm(request, data=request.POST)  # создаем экземпляр формы LoginForm с данными POST-запроса
        if form.is_valid():  # проверка на валидность
            username = form.cleaned_data.get('username')  # Получаем имя пользователя
            password = form.cleaned_data.get('password')  # Получаем пароль
            user = authenticate(username=username, password=password)  # проверка на существование пользователя
            if user is not None:  # Если пользователь найден
                login(request, user)  # Выполняем вход
                return redirect('home/')  # Перенаправляем пользователя на главную страницу
            else:  # Если пользователь не найден
                messages.error(request, "Неверный логин или пароль.")  # Отправляем ошибку
    else:  # Если запрос не POST
        form = LoginForm() #создаем пустую форму
    return render(request, 'polls/login.html', {'form': form})  # Отображаем шаблон входа с формой

@login_required  # ограничиваем доступ не авторизированным пользователям
def logout_view(request):  # функция выхода
    logout(request)  # Выходим из системы
    return redirect('/')  # Перенаправляем на авторизацию

@login_required  # ограничиваем доступ не авторизированным пользователям
def delete_account(request):  # функция удаление аккаунта
    if request.user.is_authenticated:  # Проверяем аутентифицирован ли пользователь
        if request.method == 'POST':  # проверка на метод POST
            form = DeleteAccountForm(request.POST)  # Создаем экземпляр формы DeleteAccountForm с данными POST-запроса
            if form.is_valid() and form.cleaned_data['confirm_delete']:  # Проверка на валидацию формы и подтверждения удаления
                request.user.delete()  # Удаляем пользователя
                logout(request)  # Выходим из системы
                return redirect('/')  # Перенаправляем на главную страницу
        else:  # Если запрос не POST
            form = DeleteAccountForm() #создаем пустую форму
        return render(request, 'polls/delete_account.html', {'form': form})  # Отображаем шаблон удаления аккаунта
    else:  # Если пользователь не аутентифицирован
        return redirect('polls:login')  # Перенаправляем на страницу входа

def register(request):  # Определяем представление для регистрации пользователя
    if request.method == 'POST':  # проверка на метод POST
        form = RegistrationForm(request.POST, request.FILES)  # Создаем экземпляр формы RegistrationForm с POST-запроса
        if form.is_valid():  # Проверяем, валидна ли форма
            user = form.save()  # Сохраняем пользователя
            UserProfile.objects.create(user=user, avatar=form.cleaned_data['avatar'])  # Создаем профиль пользователя с аватаром
            return redirect('/')  # Перенаправляем на авторизацию
    else:  # Если запрос не POST
        form = RegistrationForm() # создаем пустую форму
    return render(request, 'polls/register.html', {'form': form})  # Отображаем регистрацию с формой

@login_required
def edit_profile_view(request):
    user = request.user
    user_profile = user.userprofile  # Получаем UserProfile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            user_profile.avatar = form.cleaned_data.get('avatar')  # Обновляем аватар в UserProfile
            user_profile.save()  # Сохраняем изменения в UserProfile
            messages.success(request, "Профиль обновлен!")
            return redirect('polls:profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'polls/edit_profile.html', {'form': form}) # Отображаем шаблон редактирования профиля с формой

@login_required  # ограничиваем доступ не авторизированным пользователям
def profile_view(request):  # функция показа профиля
    user = request.user  # Получаем текущего пользователя
    return render(request, 'polls/profile.html', {'user': user})  # Отображаем шаблон профиля с данными пользователя

# ОПРОСНИК

def create_question(request):  # функция создания вопроса
    if request.method == 'POST':  # Проверяем на POST метод
        question_form = QuestionForm(request.POST, request.FILES)  # Создаем экземпляр формы QuestionForm с данными из POST запроса
        choice_forms = [ChoiceForm(request.POST, prefix=str(i)) for i in range(3)]  # Создаем три формы для вариантов ответов

        if question_form.is_valid() and all(choice_form.is_valid() for choice_form in choice_forms):  # Проверка валидности
            question = question_form.save(commit=False)  # Не сохраняем еще в БД, но создаем объект вопроса
            question.pub_date = timezone.now()  # Устанавливаем текущую дату
            question.save()  # Сохраняем вопрос в БД
            for choice_form in choice_forms:  # Проходим по всем формам вариантов ответов
                choice = choice_form.save(commit=False)  # Создаем вариант ответа
                choice.question = question  # Привязываем вариант к созданному вопросу
                choice.save()  # Сохраняем вариант ответа в БД
            return redirect('polls:index')  # Перенаправляем на страницу со списком вопросов
    else:  # Если запрос не POST
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=str(i)) for i in range(3)]  # Создаем три пустые формы для вариантов ответов

    context = {  # Создаем контекст для передачи данных в шаблон
        'question_form': question_form,  # Передаем форму вопроса
        'choice_forms': choice_forms,  # Передаем формы вариантов ответов
    }
    return render(request, 'polls/create_question.html', context)  # Отображаем шаблон создания вопроса с формами

class IndexView(generic.ListView):  # функция главной страницы с вопросами
    template_name = 'polls/index.html'  # Указываем шаблон для отображения
    context_object_name = 'latest_question_list'  # Указываем имя контекстного объекта для шаблона

    def get_queryset(self):  # Определяем какие объекты будут переданы в шаблон
        return Question.objects.order_by('-pub_date')  # Возвращаем все вопросы отсортированные по дате публикации

class DetailView(generic.DetailView):  # Определяем представление для отображения деталей вопроса
    model = Question  # Указываем модель с которой будет работать это представление
    template_name = 'polls/detail.html'  # Указываем шаблон для отображения

class ResultsView(generic.DetailView):  # Определяем представление для отображения результатов голосования
    model = Question  # Указываем модель с которой будет работать это представление
    template_name = 'polls/results.html'  # Указываем шаблон для отображения


def vote(request, question_id):  # Определяем представление для голосования за вопрос
    question = get_object_or_404(Question, pk=question_id)  # Получаем вопрос по его ID или возвращаем 404 если не найден

    # Проверяем голосовал ли пользователь уже за этот вопрос
    if Vote.objects.filter(user=request.user, question=question).exists():  # Проверяем, есть ли запись о голосе пользователя за этот вопрос.
        return redirect(reverse('polls:results', args=(question.id,)))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # Получаем выбранный вариант ответа по ID из POST-запроса
    except (KeyError, Choice.DoesNotExist):  # Если ключ не найден или вариант ответа не существует
        return render(request, 'polls/detail.html', {  # Отображаем детали вопроса с сообщением об ошибке
            'question': question,
            'error_message': 'Вы не сделали выбор.'
        })
    else:  # Если выбор сделан успешно
        selected_choice.votes += 1  # Увеличиваем количество голосов для выбранного варианта
        selected_choice.save()  # Сохраняем изменения в БД

        # Сохраняем голос пользователя.
        Vote.objects.create(user=request.user, question=question, choice=selected_choice)  # Создаем запись о голосе пользователя

        return redirect(reverse('polls:results', args=(question.id,)))  # Перенаправляем пользователя на страницу с результатами голосования