from django.db import models
from .validators import validate_file
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(('Users must have an email address'))
        if not first_name:
            raise ValueError(('Users must have a first name'))
        if not last_name:
            raise ValueError(('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Person(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    DOB = models.DateField('Date of birth', blank=True, null=True)
    contact_no = models.IntegerField(blank=True, null=True)
    class Meta:
        abstract = True


class Employee(Person):
    role = models.CharField(max_length=300,default='student')
    salary = models.FloatField(default=0)
    class Meta:
        abstract = True


class Teacher(Employee):
    pass

class Student(Person):
    roll_no = models.IntegerField(primary_key=True)

class Applicants(models.Model):
    full_name = models.CharField(max_length=400)
    contact_no = models.IntegerField()
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=1000, blank=True, null=True)
    position = models.CharField(max_length=500)
    cv = models.FileField(null=True, blank=False, verbose_name="file", validators=[validate_file])



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














