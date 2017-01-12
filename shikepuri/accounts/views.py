from cms.models import File
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import RegisterForm


def index(request):
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/index.html', context)


@login_required
def mypage(request):
    files = File.objects.filter(author=request.user).order_by('id')
    context = {'user': request.user, 'files': files}

    return render(request, 'accounts/mypage.html', context)


def regist(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'accounts/regist.html', context)


@require_POST
def regist_save(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('accounts:index')

    context = {
        'form': form,
    }
    return render(request, 'accounts/regist.html', context)
