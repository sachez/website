from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from payments.forms import Register, SignInForm, TakeCreditForm, VerificationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from payments.models import Credit, VerificationInformation, ExtUser
from django.http import JsonResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from payments.tasks import get_curse as gc
import re
import json

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
redis = getattr(settings, 'CACHE_REDIS', None)

# Create your views here.


@login_required(login_url='/payments/sign_in')
def get_curse(request):
    i = 1
    curse = {}
    while True:
        try:
            curse = json.loads(redis.get(redis.keys('*')[-i]).decode())
            if curse['status'] == 'SUCCESS':
                return JsonResponse({
                    'success': True,
                    'error': None,
                    'curse': curse['result']
                })
            i += 1
        except IndexError:
            return JsonResponse({
                'success': False,
                'error': 'Service Unavailable',
                'curse': None
            })


@login_required(login_url='/payments/sign_in')
def user_home(request, id):
    lains = Credit.objects.filter(fo_key=request.user)
    return render(request, 'payments/user_home.html', context={
        'lains': lains
    })


@login_required(login_url='/payments/sign_in')
def take_credit(request):
    take_credit_form = TakeCreditForm()

    if request.method == "POST":
        take_credit_form = TakeCreditForm(request.POST)
        if take_credit_form.is_valid():
            credit = take_credit_form.save(commit=False)
            credit.fo_key = ExtUser.objects.get(email=request.user)
            credit.save()

        return redirect(user_home, id=ExtUser.objects.get(email=request.user).pk)

    return render(request, 'payments/take_credit.html', context={
        'take_credit_form': take_credit_form,
        'id': ExtUser.objects.get(email=request.user).pk
    })


@login_required(login_url='/payments/sign_in')
def verification(request):
    verification_form = VerificationForm()

    if request.method == "POST":
        verification_form = VerificationForm(request.POST, request.FILES)
        if verification_form.is_valid():
            user = ExtUser.objects.get(email=request.user)

            if not user.has_perm("auth.take_credit"):
                user.user_permissions.add(
                    Permission.objects.get(codename="take_credit")
                )

            verification_inf = verification_form.save(commit=False)
            verification_inf.owner = user
            verification_inf.ver_inform_upload = True
            verification_inf.save()

            return redirect(user_home, id=ExtUser.objects.get(email=request.user).pk)

    return render(request, 'payments/verification.html', context={
        'verification_form': verification_form,
        'id': ExtUser.objects.get(email=request.user).pk
    })


def register(request):
    reg_form = Register()
    return render(request, 'payments/registr.html', context={
        'reg_form': reg_form
    })


def ajax_check_form(request):

    if request.method == "POST":
        reg_form = Register(request.POST)

        if reg_form.is_valid():

            reg = reg_form.clean()
            print(reg['conv'])
            if reg['pas'] != reg['ver_pas']:
                return JsonResponse({
                    'success': False,
                    'error': 'Password don\'t the same'
                })

            if not reg['conv']:
                return JsonResponse({
                    'success': False,
                    'error': 'Read the link'
                })

            if ExtUser.objects.filter(email=request.POST['email']).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'ExtUser with the same email exists'
                })

            data = {
                'email': reg['email'],
                'password': reg['pas']
            }

            new_user = ExtUser.objects.create_user(**data)

            login(request, authenticate(
                request,
                email=data['email'],
                password=data['password']
            ))

            return JsonResponse({
                'success': True,
                'error': None,
                'redirect_page': '/payments/user=' + str(new_user.pk)
            })

        return JsonResponse({
            'success': False,
            'error': 'Data is invalid'
        })

    return JsonResponse({
        'success': False,
        'error': ''
    })


@cache_page(CACHE_TTL)
@csrf_protect
def sign_in(request):
    sign_in_form = SignInForm()
    print(request)

    if request.method == "POST":
        sign_in_form = SignInForm(request.POST)
        if sign_in_form.is_valid():
            user = ExtUser.objects.get(email=sign_in_form.cleaned_data['email'])

            login(request, authenticate(
                email=sign_in_form.cleaned_data['email'],
                password=sign_in_form.cleaned_data['pas']
            ))

            return redirect('/payments/user='+str(user.pk))

    return render(request, 'payments/sign_in.html', context={
        'signin_form': sign_in_form
    })


def check_reg_form(request):

    email_pattern = re.compile('^[0-9a-zA-Z.]+@[0-9a-zA-Z]+\.[a-zA-Z]{2,3}$')

    if not email_pattern.match(request.POST['email']) \
            or re.search('[а-яА-Я]', request.POST['pas']) \
            or re.search('[а-яА-Я]', request.POST['ver']):

        return JsonResponse({
            'success': 0,
            'error': 'All fields must be written in English'
        })

    if ExtUser.objects.filter(email=request.POST['email']).exists():
        return JsonResponse({
            'success': 0,
            'error': 'User with the same email exists'
        })

    if request.POST['pas'] != request.POST['ver']:
        return JsonResponse({
            'success': 0,
            'error': 'Passwords don\' the same'
        })

    return JsonResponse({'success': 'done', 'error': ""})
