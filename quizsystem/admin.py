from django.contrib import admin

# Register your models here.
from .models import Teacher, QuestionBook, Quiz, AnswerBook, Course, Classroom, Contact, Student, Result,add_questions,User, Applicants
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First-Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last-Name'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm-Password'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password',  'first_name', 'last_name', 'is_active',
            'is_staff'
        )

    def clean_password(self):
# Password can't be changed in the admin
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()









admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Quiz)
admin.site.register(QuestionBook)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(Contact)
admin.site.register(Result)
admin.site.register(AnswerBook)
admin.site.register(User, UserAdmin)
admin.site.register(Applicants)

