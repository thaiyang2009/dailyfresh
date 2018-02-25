from django.db import models

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey("df_user.UserInfo")
    goods = models.ForeignKey("df_goods.GoodsInfo")
    count = models.IntegerField(default=1)

    def __str__(self):
        return '%s-%s' %(self.user, self.goods)

