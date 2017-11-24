from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^productlists/$', CreateView.as_view(), name="create"),
    url(r'^productlists/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
    url(r'^productlists/(?P<pk>[0-9]+)/delete$', DetailsView.as_view(), name="details"),
    url(r'^createuser/$', UserView.as_view(), name="create_user"),
    url(r'^login/$', LoginView, name="login_user"),
    url(r'productlists/(?P<pk>[0-9]+)/buy/$', BuyView.as_view(), name="buy_product"),
    url(r'productlists/(?P<pk>[0-9]+)/rate/$', RateProduct.as_view(), name="rate_product"),
    url(r'verifyadmin/(?P<token>.+?)/$', VerifyAdmin.as_view(), name="verify_user")
]
