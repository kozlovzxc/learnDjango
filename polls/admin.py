from django.contrib import admin

from .models import Question, Choice


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    fields = ['choice_text']
    model = Choice
    extra = 2


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    # fields = ['question_text', 'pub_date']
    fieldsets = (
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    )
    inlines = [ChoiceInline]

    list_display = ['question_text', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
