from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from df_user.decorators import require_login
from . import models
from df_goods.models import GoodsInfo
# Create your views here.



@require_login
def cart(request):

    # models.Cart.objects.filter(user=request.df_user).delete()

    cart_li = models.Cart.objects.filter(user=request.df_user)
    context = {
        'user': request.df_user,
        'page_name': 'site',
        'cart_li': cart_li,

    }
    return render(request, 'df_cart/cart.html', context)


@require_login
def add(request):
    # 接收操作的商品ID
    goods_id = request.GET.get('gid')
    count = request.GET.get('count', '0')
    if not count.isdigit():
        raise Http404('count argment error.')

    count = int(count)

    # 获取商品对象
    goods_obj = get_object_or_404(GoodsInfo, pk=goods_id)

    # 查询购物车信息
    cart_li = models.Cart.objects.filter(user=request.df_user)

    print(cart_li)

    # 判断商品是否在购物车中
    for cart_obj in cart_li:
        print(id(goods_obj), id(cart_obj.goods))
        if goods_obj.id == cart_obj.goods.id:
            break
    else: # 不在购车中，创建购物车对象
        cart_obj = models.Cart()
        cart_obj.count = 0
        cart_obj.goods = goods_obj
        cart_obj.user = request.df_user

    if count == 0: # 追加一个数量
        count = cart_obj.count + 1
        if count > goods_obj.gstorage:
            count = goods_obj.gstorage
        cart_obj.count = count
    elif count < 0: # 减少一个数量
        count = cart_obj.count - 1
        if count < 1:
            count = 1
        cart_obj.count = count
    else: # 改成指定数量
        if count > goods_obj.gstorage:
            count = goods_obj.gstorage
        cart_obj.count = count

    cart_obj.save()

    if request.is_ajax():
        data = {
            'count': cart_obj.count,
            'cart_count': models.Cart.objects.filter(user=request.df_user).count(),
            'gstorage': goods_obj.gstorage,
        }
        return JsonResponse(data)

    return redirect('cart')


@require_login
def del_cart(request):
    if request.is_ajax():
        cid = request.GET.get('cid')
        cart_obj = get_object_or_404(models.Cart, pk=cid)
        cart_obj.delete()
        return JsonResponse({'status': 200})
    return redirect('cart')



