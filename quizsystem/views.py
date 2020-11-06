from django.views import generic
import logging
from .models import User, Student
from django.shortcuts import render, redirect
from django.views.generic import View,RedirectView, TemplateView
from .admin import AddUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.forms import forms
from django.contrib import messages
from .forms import ApplicationForm
# Create your views here

class IndexView(TemplateView):
    template_name = 'quizsystem/index.html'


class Home_view(TemplateView):
    template_name = 'quizsystem/home.html'


@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def signup_view(request):
    registered = False
    if request.method == 'POST':
        user_form = AddUserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            registered=True
            return redirect("login")

        else:
            messages.warning(request, str(user_form.errors), extra_tags='alert-danger')

    else:
        user_form = AddUserForm()
    return render(request, 'quizsystem/signup.html', {
        'user_form' : user_form,
        'registered' : registered})


def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            messages.warning(request, "Invalid Credentials Given", extra_tags="alert-danger")
            return render(request, 'quizsystem/login.html')

    else:
        return render(request, 'quizsystem/login.html', {})



class Application_Form_View(View):
    form_class = ApplicationForm
    template_name = 'quizsystem/application_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save()
            return render(request, 'quizsystem/login.html', {'applicant': applicant})

        messages.warning(request, str(form.errors), extra_tags='alert-danger')
        return render(request,self.template_name,{'form': form} )













# messages.success(request, 'Your account was created Successfully!', extra_tags="alert-success")
# user.set_password(user.password)
# student = student_form.save(commit=False)
# student.user = user
# student.save()








# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'quizsystem/signup.html'
#
#     def get(self, request):
#         logging.info('Coming in userformview get method')
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     # def post(self, request):
#     #     logging.info('Coming in userformview post method')
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         username = form.cleaned_data['email']
    #         password = form.cleaned_data['password']
    #         user.set_password(password)
    #         user.save()
    #
    #         user = authenticate(username=username, password=password)
    #
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return redirect('')
    #         return render(request, self.template_name, {'form': form})







# class LoginView(generic.CreateView):
#     model = User
#     fields = ['email', 'password']
#     template_name = 'quizsystem/login.html'
#
# class LoginFormView(View):
#     form_class = LoginForm
#     template_name = 'quizsystem/login.html'
#
#     def get(self, request):
#         print('coming in get method!')
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         username = form.cleaned_data['email']
#         password = form.cleaned_data['password']
#         user = authenticate(username=username, password=password)
#         print('Coming in Post Before If')
#         if user.is_authenticated:
#             return render(request, template_name="quizsystem/signup.html")
#         else:
#             return render(request, template_name='quizsystem/login.html')

















