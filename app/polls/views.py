from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from app.polls.models import *
import json
# Create your views here.

def get_accounts(request):
    data = {}
    try:
        if request.user.is_authenticated:
            accounts = Account.objects.filter(user=request.user)
            array_accounts = []
            for account in accounts:
                acc = {
                        'id': account.id,
                        'name': account.name
                    }
                array_accounts.append(acc)
            data['accounts'] = array_accounts
        else:
            data['status'] = False
        return JsonResponse(data)
    except Exception as e:
        data['result'] = False
        data['error'] = '500'  # User does not exists
        data['msg'] = 'Internal error, please try again'
    return JsonResponse(data)


@csrf_exempt
def register_transaction(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')

        Transaction.objects.create(account_id=account_id,
                                   description=description,
                                   amount=amount)

        return JsonResponse({'result': True, 'msg': "Transaction is registered"})

    return HttpResponse(
        json.dumps({'result': False, 'msg': "Only accepted posts"}),
        'application/json'
    )


def log_out(request):
    logout(request)
    return JsonResponse({'status': True})


def index(request):
    return JsonResponse({'result': True, 'msg': "User is registered"})




@csrf_exempt
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
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

@csrf_exempt
def login_user(request):
    data = {}
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # remember = request.POST.get('remember')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                data['result'] = True

                # if remember:
                #     request.session.set_expiry(0)
            else:
                exists = User.objects.filter(username=username).exists()
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

    return JsonResponse(data)
