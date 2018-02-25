import json
from django.shortcuts import render, redirect, HttpResponse, resolve_url, get_object_or_404
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.core.cache import cache
from . import models
from . import task
from df_order.models import Order
from .decorators import require_login
from df_goods.models import GoodsInfo
# Create your views here.


def register(request):
    user_id = request.session.get('user_id')
    if user_id:
        return redirect('index')
    return render(request, 'df_user/register.html')


def register_handle(request):

    user_id = request.session.get('user_id')
    if user_id:
        return redirect('index')
    # 接收用户数据
    user_name = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    email = request.POST.get('email')

    # 判断两次密码
    if pwd != cpwd:
        return render(request, 'df_user/register.html')

    user_obj = models.UserInfo()
    user_obj.uname = user_name
    user_obj.upwd = pwd
    user_obj.uemail = email
    user_obj.save()

    request.session['user_id'] = user_obj.id
    request.session['user_name'] = user_obj.uname

    return redirect(resolve_url('info'))


def login(request):



    user_id = request.session.get('user_id')
    if user_id:
        return redirect('index')
    username = request.COOKIES.get('username', '')
    context = {
        'username': username
    }
    next_url = request.GET.get('next_url')
    if next_url:
        context['next_url'] = next_url

    return render(request, 'df_user/login.html', context)

from django.utils.http import urlsafe_base64_decode
def login_handle(request):
    print(request.get_full_path())


    user_id = request.session.get('user_id')
    if user_id:
        return redirect('index')

    username = request.POST.get('username')
    pwd = request.POST.get('pwd')

    user_li = models.UserInfo.objects.filter(uname=username)

    context = {
        'username': username
    }

    if not user_li or len(user_li) != 1:
        context['user_error'] = '用户名错误！'
        return render(request, 'df_user/login.html', context)


    if not user_li[0].check_pwd(pwd):
        context['pwd_error'] = '密码错误！'
        return render(request, 'df_user/login.html', context)

    user_obj = user_li[0]
    request.session['user_id'] = user_obj.id
    request.session['user_name'] = user_obj.uname

    # 获取
    next_url = request.GET.get('next_url')
    if next_url:
        next_url = urlsafe_base64_decode(next_url).decode()
        response = redirect(next_url)
    else:
        response = redirect(resolve_url('info'))

    if request.POST.get('remember', False):
        response.set_cookie('username', user_obj.uname, max_age=60*60*24*7)
    else:
        response.delete_cookie('username')

    return response


@require_login
def logout(request):
    request.session.flush()
    return redirect('index')


def check_username(request):
    username = request.GET.get('username')
    count = models.UserInfo.objects.filter(uname=username).count()
    data = {
        'count': count,
        'status': 200
    }
    return HttpResponse(json.dumps(data))

def check_email(request):
    email = request.GET.get('email')
    count = models.UserInfo.objects.filter(uemail=email).count()
    data = {
        'count': count,
        'status': 200
    }
    return HttpResponse(json.dumps(data))

@require_login
def site(request):

    if request.method == 'POST':
        consignee = request.POST.get('consignee')
        address = request.POST.get('address')
        code = request.POST.get('code')
        phone = request.POST.get('phone')

        data = {
            'status': 200,
            'errors': []
        }

        if not consignee:
            data['status'] = 400
            data['errors'].append('收件人不能为空!')

        if not address:
            data['status'] = 400
            data['errors'].append('收件地址不能为空!')

        if not phone:
            data['status'] = 400
            data['errors'].append('收件手机不能为空!')

        if not data['errors']:
            user_obj = request.df_user

            user_obj.ushou = consignee
            user_obj.uaddress = address
            user_obj.uyoubian = code
            user_obj.uphone = phone
            user_obj.save()

    context = {
        'user': request.df_user,
        'page_name': 'site',
        'shen': models.AreaInfo.objects.filter(parea__isnull=True),

    }

    return render(request, 'df_user/user_center_site.html', context)


@require_login
def change_site(request, aid):
    addr_obj = get_object_or_404(models.AddressInfo, pk=aid)


    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        aid = request.POST.get('aid')

        if len(receiver)>=2 and len(address)>=5 and len(phone)==11:
            area_obj = get_object_or_404(models.AreaInfo, pk=aid)
            addr_obj.area = area_obj
            addr_obj.receiver = receiver
            addr_obj.address = address
            addr_obj.phone = phone
            addr_obj.save()

        next_url = request.GET.get('next_url')
        if next_url:
            return redirect(next_url)
        return redirect('site')

    context = {
        'addr': addr_obj
    }


    return render(request, 'df_user/user_center_edit.html', context)



@require_login
def info(request):

    record = request.COOKIES.get('record')

    if record:
        record_li = record.split(',')
        records_obj_q = GoodsInfo.objects.filter(pk__in=record_li)
        # 根据访问顺序对查询结果排序
        records_obj = []
        for i in [int(i) for i in record_li]:
            for g in records_obj_q:
                if i == g.id:
                    records_obj.append(g)
                    break
    else:
        records_obj = []

    context = {
        'user': request.df_user,
        'page_name': 'site',
        'records': records_obj
    }

    return render(request, 'df_user/user_center_info.html', context)


@require_login
def order(request):
    pid = request.GET.get('p', 1)

    pid = int(pid)

    orders = Order.objects.filter(user=request.df_user)

    p = Paginator(orders, 5)


    if pid > p.num_pages or pid < 1:
        pid = 1
    page = p.page(pid)
    if pid == p.num_pages:
        page.next = 0
    else:
        page.next = page.next_page_number()
    if pid == 1:
        page.prev = 0
    else:
        page.prev = page.previous_page_number()

    context = {
        'user': request.df_user,
        'page': page,
    }

    return render(request, 'df_user/user_center_order.html', context)





def area_handle(request):
    aid = request.GET.get('aid')
    area_obj = models.AreaInfo.objects.get(pk=aid)
    context = {
        'data': list(area_obj.areainfo_set.values()),
        'status': 200

    }
    return HttpResponse(json.dumps(context))

@require_login
def edit_info(request):
    if request.method == "POST":
        data = request.POST.get('data')
        user_obj = request.df_user
        if data:
            dic = json.loads(data)

        u_dic = {}
        for k,v in dic.items():
            if hasattr(user_obj, k):
                setattr(user_obj, k, v)
                u_dic[k] = v
        if 'uemail' in dic:
            user_obj.verify_e = False
        if 'uphone' in dic:
            user_obj.verify_p = False
        user_obj.save()

        response = {
            'status': 200,
            'data': u_dic,
        }

        return JsonResponse(response)




@require_login
def verify(request):


    if request.method == 'GET':
        t = request.GET.get('t')
        if t:
            if t == 'p' and request.df_user.verify_p:
                return redirect('info')
            elif t == 'e' and request.df_user.verify_e:
                return redirect('info')
            context = {
                'page_name': '验证手机号' if t == 'p' else '验证邮箱',
                'user': request.df_user,
                't': t,
            }
            return render(request, 'df_user/user_center_verify.html', context)

    elif request.method == 'POST':
        t = request.POST.get('t')
        if t == 'p':
            # 验证手机号
            code = request.POST.get('code')
            cache_code = cache.get(request.df_user.uphone)
            if cache_code and code.lower() == cache_code.lower():
                cache.delete(request.df_user.uphone)
                request.df_user.verify_p = True
                request.df_user.save()
                return redirect('info')
            else:
                context = {
                    'page_name': '验证手机号',
                    'user': request.df_user,
                    't': t,
                    'msg': '验证码错误！'
                }
                return render(request, 'df_user/user_center_verify.html', context)

        elif t == 'e':
            # 验证邮箱
            code = request.POST.get('code')
            cache_code = cache.get(request.df_user.uemail)
            if cache_code and code.lower() == cache_code.lower():
                cache.delete(request.df_user.uemail)
                request.df_user.verify_e = True
                request.df_user.save()
                return redirect('info')
            else:
                context = {
                    'page_name': '验证手机号',
                    'user': request.df_user,
                    't': t,
                    'msg': '验证码错误！'
                }
                return render(request, 'df_user/user_center_verify.html', context)

    return redirect('info')



@require_login
def send_captcha(request):
    t = request.GET.get('t')
    data = {
        'status': 200
    }
    if t:
        if t == 'p' and not request.df_user.verify_p:
            # 发送手机验证码
            result = task.send_sms_captcha.delay(request.df_user.uphone)
            data['tid'] = result.id
        elif t == 'e' and not request.df_user.verify_e:
            # 发送邮箱验证码
            result = task.send_email_captcha.delay(request.df_user.uemail)
            data['tid'] = result.id
        else:
            data['status'] = 400
    else:
        data['status'] = 400
    return JsonResponse(data)

