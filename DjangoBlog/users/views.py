import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from mixins import LoginRequiredMixin

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,100}$")
PASSWORD_RE = re.compile(r"^.{6,100}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_verify(password, verify):
    return password == verify


def valid_email(email):
    if email == '':  # Allows blank emails since they are not required
        return True
    return EMAIL_RE.match(email)


class Login(View):
    def get(self, request):
        return render(request, 'sign_in.html')

    def post(self, request):
        username = request.POST['username']
        user = authenticate(username=username, password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Welcome back %s!' % username)
                redirectUrl = request.GET.get('next')
                if redirectUrl:
                    return HttpResponseRedirect(redirectUrl)
                return HttpResponseRedirect(reverse('blog_HomePage'))
            else:
                messages.add_message(request, messages.INFO, 'Sorry that account has been disabled.')
        else:
            messages.add_message(request, messages.INFO, 'Sorry that is a wrong username + password combination.')
        return render(request, 'sign_in.html', {'username': username})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You have been signed out')
        return HttpResponseRedirect(reverse('blog_HomePage'))


class SignUp(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'sign_up.html', {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
        email = request.POST['email']

        if not valid_username(username):
            messages.add_message(request, messages.INFO, 'Sorry that is not a valid username, letters and numbers only.')
        if User.objects.filter(username=username):
            messages.add_message(request, messages.INFO, 'Sorry that username is taken.')
        if not valid_password(password) or password != verify:
            messages.add_message(request, messages.INFO, 'Ensure your passwords match and are at least 6 charecters.')
        if not valid_email(email):
            messages.add_message(request, messages.INFO, 'That is not a valid email address.')
        if messages.get_messages(request):
            params = {'username': username,
                      'email': email}
            return render(request, 'sign_up.html', params)
        else:
            newUser = User.objects.create_user(username, email, password)
            messages.add_message(request, messages.SUCCESS, 'New user %s created!' % newUser.username)
            return HttpResponseRedirect(reverse('admin_AdminUserList'))


class EditUser(LoginRequiredMixin, View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        return render(request, 'edit_user.html', {'editUser': user})

    def post(self, request, id):
        user = User.objects.get(id=id)
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
        email = request.POST['email']
        active = request.POST['active'] == 'active'

        if not valid_username(username):
            messages.add_message(request, messages.INFO, 'Sorry that is not a valid username, letters and numbers only.')
        if User.objects.filter(username=username).exclude(id=id):
            messages.add_message(request, messages.INFO, 'Sorry that username is taken.')
        if (password and verify) and not valid_password(password) or password != verify:
            messages.add_message(request, messages.INFO, 'Ensure your passwords match and are at least 6 charecters.')
        if email and not valid_email(email):
            messages.add_message(request, messages.INFO, 'That is not a valid email address.')
        if messages.get_messages(request):
            params = {'username': username,
                      'email': email,
                      'is_active': active}
            return render(request, 'edit_user.html', params)

        user.username = username
        if password:
            user.set_password(password)
        user.email = email
        user.is_active = active
        user.save()
        messages.add_message(request, messages.SUCCESS, 'User "%s" was updated!' % username)
        return render(request, 'edit_user.html', {'editUser': user})
