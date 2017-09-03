from django.contrib import admin
from .models import Exam, Question, Report,Profile,Results


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    model = Profile

class ResultsAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'year','marks')   
    model = Results


class ChoiceInline(admin.TabularInline):
    model = Question
    extra = 1


class ExamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['exam_name']}),
        ('Date Information', {'fields': ['date_published', 'duration','branch',]}),
    ]
    inlines = [ChoiceInline]
    list_display = ('exam_name','duration', 'date_published','branch',)



admin.site.register(Exam, ExamAdmin)
admin.site.register(Results,ResultsAdmin)
admin.site.register(Profile,ProfileAdmin)
