# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from df_user import user_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import df_user
import df_cart
from django.db import transaction
from models import *
from datetime import *


@user_decorator.login
def order(request):
    user = df_user.models.UserInfo.objects.get(id=request.session['user_id'])

    get = request.GET
    cart_id = get.getlist('cart')
    # 列表解析
    # cart_ids = [int(item) for item in cart_id]
    carts = df_cart.models.CartInfo.objects.filter(id__in=cart_id)
    context = {
        'title': '提交订单',
        'page_name': 1,
        'carts': carts,
        'user': user
    }
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    '''
    事物：一旦操作失败则全部回滚
    1.创建订单对象
    2.判断商品的库存
    3.创建详单对象
    4.修改商品库存
    5.删除购物车
    '''
    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.GET.get('cart_ids')
    uid = request.session["user_id"]
    user = df_user.models.UserInfo.objects.get(pk=uid)
    address1 = '%s(%s收)%s'%(user.uaddress, user.ushou, user.uphone)
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.GET.get('total'))
        order.oaddress = address1
        order.save()
        # 创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = df_cart.models.CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gkucun >= cart.count: # 如果库存大于购买数量
                #减少商品库存
                goods.gkucun = cart.goods.gkucun-cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车
                cart.delete()
            else:#如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/df_cart/')
        transaction.savepoint_commit(tran_id)
        data = {'ok': 1}
    except Exception as e:
        print '=============%s' % e
        transaction.savepoint_rollback(tran_id)
        txterror = '=============%s' % e
        data = {'ok': 0, 'error': txterror}
        return JsonResponse(data)
    return JsonResponse(data)


















































