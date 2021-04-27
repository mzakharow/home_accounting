from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile
from account.tasks import send_mail_task
from home_accounting import settings


def user_login(request):
    """ обработчик входа пользователя """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('transfers-list'))
            else:
                return HttpResponse('Disabled account')
        else:
            messages.success(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    """ обработчик регистрации пользователя """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            cd = user_form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    subject = f"Регистрация на сайте 'Личная Бухгалтерия'"
                    message = f"Поздравляем, {cd['username']}! \nВы зарегистрированы!"
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['email']])
                    # send_mail_task.delay(cd['email'], cd['username'])
                    return HttpResponseRedirect(reverse('transfers-list'))
                else:
                    return HttpResponse('Disabled account')
            return HttpResponseRedirect(reverse('account:login'))
        else:
            messages.success(request, 'Ошибка создания пользователя')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """ обработчик редактирования пользователя """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('transfers-list'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})