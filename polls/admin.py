from django.contrib import admin  
from .models import Question, Choice  

# Определяем класс ChoiceInLine, который будет отображать варианты ответов (Choice) в виде инлайновой формы в админке
class ChoiceInLine(admin.TabularInline):
    model = Choice  # Указываем, что будет работать с моделью Choice
    extra = 3  # Указываем, что по умолчанию будет отображаться 3 пустые формы для добавления новых вариантов ответов

# Определяем класс QuestionAdmin, который будет управлять отображением модели Question в админке
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]  # Указываем, что в админке для Question будут отображаться инлайновые формы ChoiceInLine

# Регистрируем модель Question и связываем ее с классом QuestionAdmin в админке
admin.site.register(Question, QuestionAdmin)
