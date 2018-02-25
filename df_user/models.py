import hashlib

from django.db import models

# Create your models here.

def pwd_gen(pwd):
    s1 = hashlib.sha1()
    s1.update(pwd.encode())
    return s1.hexdigest()


class UserInfo(models.Model):
    uname = models.CharField(max_length=20, unique=True)
    _upwd = models.CharField(max_length=40)
    nikename = models.CharField(max_length=20, default='')
    uemail = models.EmailField(default='', unique=True)
    uphone = models.CharField(max_length=11, default='')
    verify_p = models.BooleanField(default=False)
    verify_e = models.BooleanField(default=False)
    default_addr = models.OneToOneField("AddressInfo", related_name='_user', null=True)

    def __str__(self):
        return self.uname

    @property
    def upwd(self):
        return self._upwd

    @upwd.setter
    def upwd(self, pwd):
        self._upwd = pwd_gen(pwd)

    def check_pwd(self, pwd):
        return self._upwd == pwd_gen(pwd)

class AddressInfo(models.Model):
    user = models.ForeignKey('UserInfo')
    receiver = models.CharField(max_length=25)
    # province = models.ForeignKey("AreaInfo", related_name='province')
    # city = models.ForeignKey("AreaInfo", related_name='city')
    area = models.ForeignKey("AreaInfo", related_name='address', null=True)

    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    postcode = models.CharField(max_length=6)

    def __str__(self):
        return "<%s-%s>" % (self.user, self.area.name)


class AreaInfo(models.Model):
    name = models.CharField(max_length=30)
    parea = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.name