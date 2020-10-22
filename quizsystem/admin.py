from django.contrib import admin

# Register your models here.
from .models import Teacher, QuestionBook, Quiz, AnswerBook, Course, Classroom, Contact, Student, Users, Result,add_questions

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Quiz)
admin.site.register(QuestionBook)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(Contact)
admin.site.register(Result)
admin.site.register(AnswerBook)
admin.site.register(Users)
admin.site.register(add_questions)
