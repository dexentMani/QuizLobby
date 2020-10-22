from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=20, blank=False, null=False)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name




class Student(models.Model):
    full_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=200, blank=False, null=False)
    status = models.CharField(max_length=20, blank=False, null=False)
    joining_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.full_name

class Users(models.Model):

    profile = [
        ('teacher','Teacher'),
        ('student','Student'),
    ]

    role = models.CharField(max_length=50, choices=profile, blank=True, null=True)
    teacher_fk = models.ForeignKey(Teacher, on_delete=models.CASCADE,blank=True, null=True)
    student_fk = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    def __str__(self):
        return self.username



class Contact(models.Model):
    full_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=200, blank=False, null=False)
    question = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.full_name

class Course(models.Model):
    teacher_rel = models.ManyToManyField(Teacher, blank=True)
    student_fk = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    course_name = models.CharField(max_length=400, blank=False, null=False)
    course_type = models.CharField(max_length=200, blank=True, null=True)
    course_code = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        return self.course_name

class Classroom(models.Model):
    teacher_fk = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    student_fk = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    course_fk = models.ForeignKey(Course, on_delete=models.CASCADE)
    details = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return self.details

class QuestionBook(models.Model):
    teacher_fk = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    details = models.CharField(max_length=400, blank=False, null=False)
    question_type = models.CharField(max_length=2000, blank=False, null=False)

    def __str__(self):
        return self.details

class add_questions(models.Model):
    teacher_fk = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=False)
    questions = models.CharField(max_length=2000, blank=False, null=False)
    def __str__(self):
        return self.questions

class AnswerBook(models.Model):
    ans = models.OneToOneField(QuestionBook, on_delete=models.CASCADE, blank=False, null=False)
    details = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.details

class Quiz(models.Model):
    teacher_rel = models.ManyToManyField(Teacher)
    student_rel = models.ManyToManyField(Student)
    course_rel = models.ManyToManyField(Course)
    class_rel = models.ManyToManyField(Classroom)
    question_fk = models.ForeignKey(QuestionBook, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField('starting-date')
    end_date = models.DateTimeField('end-date')
    start_time = models.TimeField('start-time')
    end_time = models.TimeField('end-time')
    points = models.IntegerField(default=0)
    quiz_title = models.CharField(max_length=300, blank=False, null=False)




    def __str__(self):
        return self.quiz_title + '' + 'Date:' + self.start_date.strftime("%m/%d/%Y, %H:%M:%S") + '' + 'Subject:' + self.course_rel.all()[0].course_name


class Result(models.Model):
    student_rel = models.ManyToManyField(Student)
    course_rel = models.ManyToManyField(Course)
    class_rel = models.ManyToManyField(Classroom, blank=True)
    performance = models.CharField(max_length=400)
    pub_date = models.DateTimeField('publish-date')

    def __str__(self):
        return self.student_rel.all()[0].full_name + '-' + self.course_rel.all()[0].course_name














