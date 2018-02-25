#!/usr/bin/env python
# coding:utf-8


from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url
from df_user.models import AreaInfo, UserInfo

register = template.Library()


@register.simple_tag
def default_address(addr_obj):
    if addr_obj:
        address_li = []
        area_obj = addr_obj.area
        while area_obj:
            address_li.append(area_obj.name)
            area_obj = area_obj.parea
        address_li.reverse()
        address_li.append(addr_obj.address)
        address_li.append('(%s 收)' % addr_obj.receiver)
        address_li.append('%s' % addr_obj.phone)
        return mark_safe(' '.join(address_li))






@register.simple_tag
def address_handle(addr_obj):
    if addr_obj:
        address_li = []
        area_obj = addr_obj.area
        while area_obj:
            address_li.append(area_obj.name)
            area_obj = area_obj.parea
        address_li.reverse()
        address_li.append(addr_obj.address)
        address_li.append('(%s 收)' % addr_obj.receiver)
        address_li.append('%s' % addr_obj.phone)
        return mark_safe(' '.join(address_li))





@register.simple_tag
def gen_area_select(area, s_li=None):
    if s_li is None:
        s_li = []
    if area.parea:


        li = []
        li.append('<select><option value="">--选择--</option>')

        for t in area.parea.areainfo_set.all():
            if area.id == t.id:
                s = '<option value="%s" selected>%s</option>' % (t.id, t.name)
            else:
                s = '<option value="%s">%s</option>' % (t.id, t.name)
            li.append(s)

        li.append('</select>')

        s_li.insert(0, ''.join(li))

        gen_area_select(area.parea, s_li)

    else:
        # 省
        li = []
        shen = AreaInfo.objects.filter(parea__isnull=True)
        li.append('<select><option value="">--选择--</option>')

        for t in shen:
            if area.id == t.id:
                s = '<option value="%s" selected>%s</option>' % (t.id, t.name)
            else:
                s = '<option value="%s">%s</option>' % (t.id, t.name)
            li.append(s)

        li.append('</select>')
        s_li.insert(0, ''.join(li))

# r = []
# ttt(UserInfo.objects.first().default_addr.area, r)
# print(r)

@register.simple_tag
def select_handle(addr_obj):
    result = []
    gen_area_select(addr_obj.area, result)
    return mark_safe(''.join(result))




