from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
# Create your views here.


def index(request):

    return  JsonResponse({'result': True, 'msg': "User is registered"})


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return HttpResponse(
                json.dumps({'result': False, 'code': 101, 'msg': "The account exists"}),
                'application/json'
            )
        else:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            password=password)

            login(request, user)

            return HttpResponse(
                json.dumps({'result': True, 'msg': "User is registered"}),
                'application/json'
            )

    return HttpResponse(
        json.dumps({'result': False, 'msg': "Only accepted posts"}),
        'application/json'
    )


def login(request):
    data = {}
    try:
        if request.method == 'POST':
            email = request.POST.get('user')
            password = request.POST.get('pass')
            remember = request.POST.get('remember')
            user = authenticate(username=email, password=password)

            if user and user.is_active:
                login(request, user)
                data['result'] = True

                if remember:
                    request.session.set_expiry(0)
            else:
                exists = User.objects.filter(username=email).exists()
                data['result'] = False
                if exists:
                    data['error'] = '-110'  # Incorrect password
                    data['msg'] = 'Incorrect password'
                else:
                    data['result'] = False
                    data['error'] = '-120'  # User does not exists
                    data['msg'] = 'Email does not exists'
        else:
            data['result'] = False
            data['error'] = ''  # User does not exists
            data['msg'] = 'Only accepted posts'

    except Exception as exp:
        data['result'] = False
        data['error'] = '500'  # User does not exists
        data['msg'] = 'Internal error, please try again'

        # errorLogger.error("error in login_page.  errId=123030", extra={'exp': exp})

    return HttpResponse(json.dumps(data))