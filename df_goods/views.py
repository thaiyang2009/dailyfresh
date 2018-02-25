from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.shortcuts import resolve_url
from django.core.urlresolvers import reverse
from django.core import paginator
from . import models
from df_user.models import UserInfo
from df_cart.models import Cart
from df_user.decorators import get_user
# Create your views here.


@get_user
def index(request):
    types = models.TypeInfo.objects.all()

    # 创建测试数据
    # template_goods = models.GoodsInfo.objects.first()
    #
    # for t in types:
    #     for i in range(100):
    #         models.GoodsInfo.objects.create(
    #             gtitle=str(i)*4,
    #             gpic=template_goods.gpic,
    #             gprice=template_goods.gprice,
    #             gsummary=str(i)*4,
    #             gstorage=9999,
    #             gcontent=str(i)*4,
    #             gtype=t
    #         )

    goods_dic = {}
    for t in types:
        goods = models.GoodsInfo.objects.filter(gtype=t)[0:4]
        goods_dic[t] = goods

    slides = models.Slide.objects.all()
    advs = models.Adv.objects.all()

    context = {
        'user': request.df_user,
        'types': types,
        'goods_dic': goods_dic,
        'slides': slides,
        'advs': advs,
        'cart_count': Cart.objects.filter(user_id=request.session.get('user_id')).count()
    }

    return render(request, 'df_goods/index.html', context)


@get_user
def detail(request, gid):

    goods_obj = get_object_or_404(models.GoodsInfo, pk=gid)
    goods_obj.gclick += 1
    goods_obj.save()
    types = models.TypeInfo.objects.all()
    new_goods = models.GoodsInfo.objects.all()[0:2]

    context = {
        'user': request.df_user,
        'goods': goods_obj,
        'types': types,
        'new_goods': new_goods,
        'cart_count': Cart.objects.filter(user_id=request.session.get('user_id')).count()
    }

    response = render(request, 'df_goods/detail.html', context)

    record = request.COOKIES.get('record')

    if record:
        record_li = record.split(',')
        if str(goods_obj.id) in record_li:
            record_li.remove(str(goods_obj.id))
        record_li.insert(0, str(goods_obj.id))
        if len(record_li) > 5:
            record_li = record_li[0: 5]
    else:
        record_li = [str(goods_obj.id)]
    response.set_cookie('record', ','.join(record_li))


    return response


@get_user
def goods_list(request, tid, sid, pid):
    # t = models.GoodsInfo.objects.last()
    # count = 0
    # for g in models.GoodsInfo.objects.all():
    #     count += 1
    #     g.gtitle = '民众都喜爱'
    #     g.save()
    #     if count == 50:
    #         break


    tid = int(tid)
    sid = int(sid)
    pid = int(pid)
    sid_choices = {
        0: '-pk',
        1: '-gprice',
        2: '-gclick',
    }

    if sid not in sid_choices:
        raise Http404('sort argument error.')




    if tid == 0:
        goods_li = models.GoodsInfo.objects.all().order_by(sid_choices[sid])
        new_goods = models.GoodsInfo.objects.all()[0:2]
    else:
        gtype = get_object_or_404(models.TypeInfo, pk=tid)
        goods_li = models.GoodsInfo.objects.filter(gtype=gtype).order_by(sid_choices[sid])
        new_goods = models.GoodsInfo.objects.filter(gtype=gtype)[0:2]

    pre_page = 20
    p = paginator.Paginator(goods_li, pre_page)

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
        'tid': tid,
        'sid': sid,
        'pid': pid,
        'page': page,
        'new_goods': new_goods,
        'types': models.TypeInfo.objects.all(),
    }
    if tid != 0:
        context['gtype'] = gtype


    return render(request, 'df_goods/list.html', context)



from haystack.generic_views import SearchView

class MySearchView(SearchView):
    """My custom search view."""

    # def get_queryset(self):
    #     queryset = super(MySearchView, self).get_queryset()
    #     # further filter queryset based on some set of criteria
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        context['new_goods'] = models.GoodsInfo.objects.all()[0: 2]
        print(context)
        return context
