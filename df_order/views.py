from django.shortcuts import render, redirect, get_object_or_404, Http404, resolve_url
from django.http import JsonResponse
from django.db import transaction

from df_user.decorators import require_login
from df_cart.models import Cart
from df_goods.models import GoodsInfo
from df_user.models import AddressInfo
from . import models
# Create your views here.


@require_login
def place_order(request):

    """
    第一种情况：购物车
    参数： 购物车的ids
    获取cart_objs

    第二种情况：立即购买
    参数：gid, count
    获取goods

    :param request:
    :return:
    """

    context = {
        'user': request.df_user,
        'fare': 10,
        'cart_count': Cart.objects.filter(user=request.df_user).count()
    }

    cids = request.GET.getlist('cids')
    if cids:
        carts = Cart.objects.filter(pk__in=cids, user=request.df_user)
        context['carts'] = carts
    else:
        gid = request.GET.get('gid')
        count = request.GET.get('count')
        if gid and count:
            goods_obj = get_object_or_404(GoodsInfo, pk=gid)
            context['goods'] = goods_obj
            context['count'] = count
        else:
            raise Http404('argments error.')

    return render(request, 'df_order/place_order.html', context)




@require_login
def order_handle(request):

    """
    从购物车：
    创建订单
    判断库存，创建详单
    修改库存
    删除购物车


    从立即购买： 商品ID，数量
    获取商品对象
    创建订单
    判断库存，创建详单
    修改库存

    :param request:
    :return:
    """
    data = {}
    sp = transaction.savepoint()
    user = request.df_user
    fare = 10
    error_msgs = []
    addr_id = request.POST.get('addr_id')
    if addr_id:
        addr_obj = get_object_or_404(AddressInfo, pk=addr_id)
        try:
            cids = request.POST.getlist('cids')
            print('cids-->', cids)

            if cids:
                carts = Cart.objects.filter(pk__in=cids)
                carts_total = sum([c.count * c.goods.gprice for c in carts])
                total = carts_total + fare
                ckwargs = {
                    'user': user,
                    'count': len(carts),
                    'total': total,
                    'fare': fare,
                    'area': addr_obj.area,
                    'address': addr_obj.address,
                    'phone': addr_obj.phone,
                    'receiver': addr_obj.receiver,
                    'status': 0,
                }

                # 创建订单
                order_obj = models.Order(**ckwargs)
                order_obj.save()

                # 创建详单
                order_detail_li = []
                for c in carts:
                    if c.goods.gstorage < c.count:  # 库存不足
                        transaction.savepoint_rollback(sp)  # 回退
                        msg = '商品: [%s] 库存不足！' % c.goods.gtitle
                        error_msgs.append(msg)  # 转回购物车
                        raise Exception(msg)
                    dkwargs = {
                        'order': order_obj,
                        'goods': c.goods,
                        'count': c.count,
                        'price': c.goods.gprice,
                        'unit': c.goods.gunit,
                    }
                    order_detail = models.OrderDetail(**dkwargs)
                    order_detail.save()
                    order_detail_li.append(order_detail)

                # 修改库存
                for c in carts:
                    c.goods.gstorage -= c.count
                    c.save()
                # 删除购物车
                carts.delete()

                transaction.savepoint_commit(sp)  # 提交

            else:


                # 判断库存，创建详单
                # 修改库存

                gid = request.POST.get('gid')
                count = request.POST.get('count')
                count = int(count)

                if count < 1:
                    return redirect('index')
                # 获取商品对象
                goods_obj = get_object_or_404(GoodsInfo, pk=gid)
                total = goods_obj.gprice * count + fare
                # 创建订单
                ckwargs = {
                    'user': user,
                    'count': 1,
                    'total': total,
                    'fare': fare,
                    'area': addr_obj.area,
                    'address': addr_obj.address,
                    'phone': addr_obj.phone,
                    'receiver': addr_obj.receiver,
                    'status': 0,
                }

                # 创建订单
                order_obj = models.Order(**ckwargs)
                order_obj.save()

                # 创建详单
                order_detail_li = []
                if goods_obj.gstorage < count:  # 库存不足
                    transaction.savepoint_rollback(sp)  # 回退
                    msg = '商品: [%s] 库存不足！' % goods_obj.gtitle
                    error_msgs.append(msg)
                    raise Exception(msg)

                dkwargs = {
                    'order': order_obj,
                    'goods': goods_obj,
                    'count': count,
                    'price': goods_obj.gprice,
                    'unit': goods_obj.gunit,
                }
                order_detail = models.OrderDetail(**dkwargs)
                order_detail.save()
                order_detail_li.append(order_detail)

                # 修改库存
                goods_obj.gstorage -= count
                goods_obj.save()

                transaction.savepoint_commit(sp)  # 提交

        except Exception as e:
            transaction.savepoint_rollback(sp)
            print(e)
            data['status'] = 400
            if error_msgs:
                data['error_msgs'] = error_msgs
            return JsonResponse(data)

        data['status'] = 200
        data['url'] = resolve_url('order')
    return JsonResponse(data)


