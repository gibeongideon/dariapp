# om django.contrib.auth.views import LogoutView
# from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from . import template_views as views
# from .payp_view import views as pviews 
from . import paypal_views
# from .m_pesa_view import views as mviews 



# router = DefaultRouter()

# router.register(r'user', views.UserViewSet)
# router.register(r'custom_users', views.CustomUserViewSet)
# router.register(r'accounts', views.AccountViewSet)
# router.register(r'market', views.MarketInstanceViewSet)
# router.register(r'stake', views.StakeViewSet)
# router.register(r'user_transactions', views.BalanceViewSet)

app_name = "account"

urlpatterns = [
    # path('', include(router.urls)),
    # path('user/', UserRecordView.as_view(), name='users'),
    # path(
    #     "user_trans/_start=<int:start>&_limit=<int:limit>/_user_id=<int:pk>",
    #     views.TransactionView.as_view(),
    # ),
    # path('rest-auth/', include('rest_auth.urls')),
    # templates
    path("refer_credit/", views.refer_credit, name="refer_credit"),
    path("mpesa_withrawal/", views.mpesa_withrawal, name="mpesa_withrawal"),
    path("paypal_withrawal/", views.paypal_withrawal, name="paypal_withrawal"),
    path("deposits/", views.mpesa_deposit, name="mpesa_deposit"),
    path("cash_trans/", views.cash_trans, name="cash_trans"),
    path("stop_cash_trans/", views.stop_cash_trans, name="stop_cash_trans"),
    
    path('paypal/checkout/', views.checkout, name='paypal-checkout'),
    path('paypal/process-payment/', views.process_payment, name='process_payment'),
    path('paypal/payment-done/', views.payment_done, name='payment_done'),
    path('paypal/payment-cancelled/', views.payment_canceled, name='payment_cancelled'),

    # path('paypal-checkout/', views.PaypalFormView.as_view(), name='paypal-checkout'),
    # path('paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    # path('paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),
    # path("paypal_pro/", views.paypal_pro, name="paypal_pro"),
    # path("paypal/", include('paypal.standard.ipn.urls')),

   # path("deposit/", views.deposit, name='deposit'), 
    #path("withraw/", views.withraw, name='withraw'),
    # path("deposit/paypal", pviews.accept_payment_view),
    path("deposit/m-pesa/", views.mpesa_deposit,name='mpesa_deposit'),
    # path("payment-success/", pviews.payment_success),
    # path("withdraw/", pviews.paypal_payout_view)

    #PAYLAL
    
    # path("paypal/deposit/", paypal_views.accept_payment,name="accept_payment"),
    # path("payment_success", paypal_views.payment_success,name="payment_success"),
    path("paypal/withdraw/", paypal_views.paypal_payout,name="paypal_payout")
]
