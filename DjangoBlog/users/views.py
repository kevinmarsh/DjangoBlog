import re

from django.shortcuts import render, redirect
from django.views.generic.base import View

from users.models import User

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


def login(request):
    if request.method == 'GET':
        return render_to_response('sign_in.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        userDB = User.objects.filter(username=username)
        
        if userDB and userDB[0].password == password:
            
            from django.http import HttpResponse
            return HttpResponse('<p>' + username + password + ' is correct</p>')
        else:
            return HttpResponse('<p>' + username + password + ' is wrong</p>')


class SignUp(View):
    def get(self, request):
        return render(request, 'sign_up.html', {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
        email = request.POST['email']

        errorMsgs = []
        if not valid_username(username):
            errorMsgs.append('Sorry that is not a valid username, letters and numbers only.')
        if User.objects.filter(username=username):
            errorMsgs.append('Sorry that username is taken.')
        if not valid_password(password) or password != verify:
            errorMsgs.append('Ensure your passwords match and are at least 6 charecters.')
        if not valid_email(email):
            errorMsgs.append('That is not a valid email address.')
        if errorMsgs:
            params = {'username': username,
                      'email': email,
                      'errorMsgs': errorMsgs}
            return render(request, 'sign_up.html', params)
        else:
            newUser = User(username=username,
                           password=password,
                           email=email)
            newUser.save()
            return redirect('blog_HomePage', msgs=['Welcome %s' % username])


def signUp(request):
    if request.method == 'GET':
        return render_to_response('sign_up.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
        email = request.POST['email']
        dupName = User.objects.filter(username=username)
        if not valid_username(username) or not valid_password(password) or password != verify or not valid_email(email):
            error_username = 'sorry that name is taken' if dupName else ''
            error_username = 'sorry that name is invalid' if valid_username(username) else ''
            error_password = 'sorry that password is invalid' if valid_password(password) else ''
            error_verify = 'the passwords didn\' match' if password != verify else ''
            error_email = 'sorry that email is not valid' if valid_email(email) else ''
            return render_to_response('sign_up.html', 
                                      {'username': username, 
                                       'error_username': error_username,
                                       'error_password': error_password,
                                       'error_verify': error_verify, 
                                       'email': email,
                                       'error_email': error_email})
        else:
            newUser = User(username=username,
                           password=password,
                           email=email)
            newUser.save()
            return HttpResponseRedirect('/' + username)
        from django.http import HttpResponse
        return HttpResponse('<p>' + username + password + ' is correct</p>')
