from django.db import models
from django.utils import timezone
# Create your models here.

from base_manager import BaseManager
import hashlib
import datetime


class Order(models.Model):

    order_id = models.CharField(max_length=30, primary_key=True)
    user = models.ForeignKey("df_user.UserInfo")
    count = models.IntegerField()
    total = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='实付')
    fare = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='运费')
    area = models.ForeignKey('df_user.AreaInfo', null=True)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=11)
    receiver = models.CharField(max_length=20)
    ctime = models.DateTimeField(auto_now_add=True)
    order_status_choices = (
        (0, '未支付'),
        (1, '已付款'),
        (2, '已发货'),
        (3, '已收货'),
        (4, '已完成'),
    )
    status = models.SmallIntegerField(choices=order_status_choices)


    isDelete = models.BooleanField(default=False)

    objects = BaseManager()
    old_objects = models.Manager()

    def __init__(self, *args, **kwargs):

        uid = kwargs['user'].id if 'user' in kwargs else kwargs.get('user_id')

        kwargs['order_id'] = self.gen_order_id(uid)

        super(Order, self).__init__(*args, **kwargs)

    def gen_order_id(self, uid):
        m = hashlib.md5()
        m.update(str(uid).encode())
        ustr = m.hexdigest()[-7:-1]
        d = datetime.datetime.now()
        timestr = '%s%s%s%s%s%s%s' % (d.year, d.month, d.day, d.hour, d.minute, d.second, str(d.microsecond).rjust(6, '0'))
        return ''.join([timestr, ustr])

    class Meta:
        ordering = ['-ctime']

    def __str__(self):
        return self.order_id

class OrderDetail(models.Model):

    order = models.ForeignKey("Order")
    goods = models.ForeignKey("df_goods.GoodsInfo")
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    objects = BaseManager()
    old_objects = models.Manager()

    @property
    def total(self):
        return self.price*self.count

    def __str__(self):
        return "<%s-%s>" % (self.order, self.goods)

if __name__ == "__main__":
    Order().orderdetail_set