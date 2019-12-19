from django.conf.urls import url, include
import store.views

urlpatterns = [
    url(r'register$', store.views.register),
    url(r'login$', store.views.login),
    url(r'getMessage$', store.views.getMessage),
    url(r'alterMessage$', store.views.alterMessage),
    url(r'getComdyInfoByClassId$', store.views.getComdyInfoByClassId),
    url(r'getComdyInfoById$', store.views.getComdyInfoById),
    url(r'addBasket$', store.views.addBasket),
    url(r'DeleteBasketMessage$', store.views.DeleteBasketMessage),
    url(r'getBasketMessage$', store.views.getBasketMessage),
    url(r'addSalesRecord$', store.views.addSalesRecord),
    url(r'addLog$', store.views.addLog),
    url(r'send_email$', store.views.send_email),
    url(r'upLoadImage$', store.views.upLoadImage),
]