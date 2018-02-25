#!/usr/bin/env python
# coding:utf-8

from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url

register = template.Library()

@register.simple_tag
def page_handler(page_obj, tid, sid):
    '''  < Prev 1 ... 4 5 6 7 8 ... 12  Next > '''

    # 获取总页面数
    page_count = page_obj.paginator.num_pages
    # 获取中间显示的按钮数量
    page_num = 10
    # 获取当前页数
    current_page = page_obj.number

    if page_count > 1:  # 如果总页数大于1
        if page_count <= page_num:  # 如果总页数小于或等于按钮数，没有隐藏的按钮
            s = 1
            e = page_count
        elif current_page <= page_num // 2 + 1: # 如果当前页码小于或等于按钮数量， 在最前几页中，能显示出第一页按钮
            s = 1
            e = page_num
        elif current_page >= page_count - page_num // 2:  # 如果当前页码大于或等于（总页数-（按钮数量//2）），最后几页了
            e = page_count
            s = e - page_num + 1
        else:   # 两头都有隐藏的按钮
            s = current_page - page_num // 2
            e = s + page_num - 1
        btn_list = range(s, e + 1)


        """
        <div class="pagenation">
            {% if page.prev != 0 %}
                <a href="{% url 'list' tid sid page.prev %}">	&lt;上一页</a>
            {% endif %}
            {% for n in page.paginator.page_range %}
                {% if n == pid %}
                    <a href="javascript:;" class="active">{{ n }}</a>
                {% else %}
                    <a href="{% url 'list' tid sid n %}">{{ n }}</a>
                {% endif %}
            {% endfor %}
            {% if page.next != 0 %}
                <a href="{% url 'list' tid sid page.next %}">下一页	&gt;</a>
            {% endif %}
        
        </div>
        
        """


        lis = []
        lis.append('<div class="pagenation">')

        if current_page != 1:
            li = '<a href="%s">	&lt;上一页</a>' % resolve_url('list', tid, sid, page_obj.prev)  #{% url 'list' tid sid page.prev %}
            lis.append(li)

        # if current_page - 1 > page_num // 2 and page_count > page_num:
        #     li = '<li><a href="%s" aria-label="Previous"><span aria-hidden="true">1</span></a></li>' % (
        #         page_obj.paginator.callback(current_page=1),)
        #     lis.append(li)
        #     if current_page - page_num > 1:
        #         li = '<li><span>...</span></li>'
        #         lis.append(li)

        for i in btn_list:
            if current_page == i:
                li = '<a href="javascript:;" class="active">%s</a>' % i
            else:
                li = '<a href="%s">%s</a>' % (resolve_url('list', tid, sid, i) , i)
            lis.append(li)

        # if current_page < page_count - (page_num // 2) and page_count > page_num:
        #     print(current_page+page_num, page_count)
        #     if page_count > current_page + page_num:
        #         li = '<li><span>...</span></li>'
        #         lis.append(li)
        #     li = '<li><a href="%s">%s<span class="sr-only">(current)</span></a></li>' % (
        #         page_obj.paginator.callback(current_page=page_count), page_count,)
        #     lis.append(li)

        if current_page != page_count:
            li = '<a href="%s">下一页	&gt;</a>' % resolve_url('list', tid, sid, page_obj.next) # {% url 'list' tid sid page.next %}
            lis.append(li)

        lis.append('</div>')

        return mark_safe(''.join(lis))
    return ''