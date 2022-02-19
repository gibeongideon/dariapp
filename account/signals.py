from .models import (
    Account,
    # CashWithrawal,
    CashDeposit,
    Checkout,
    update_account_bal_of,
    current_account_bal_of,
    # log_record,
)
from .models import account_setting,Currency
from daru_wheel.models import Stake  # DD
from mpesa_api.core.models import OnlineCheckoutResponse

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.update_or_create(user=instance)
        # print(f'User{instance.username} Account Created ')#Debug


@receiver(post_save, sender=OnlineCheckoutResponse)  # TODO
def update_account_balance_on_mpesa_deposit(sender, instance, created, **kwargs):
    # if created:
    try:
        if int(instance.result_code) == 0:
            try:
                this_user = User.objects.get(phone_number=str(instance.phone))
            except User.DoesNotExist:
                this_user = User.objects.create_user(
                    username=str(instance.phone), password=str(instance.phone)
                )  # 3#??
            currency=Currency.objects.get(name='USD')    

            CashDeposit.objects.create(
                user=this_user,
                amount=instance.amount,
                deposit_type="M-pesa Deposit",
                currency=currency,
                confirmed=True,
            )
        else:
            pass

    except Exception as e:
        print("MPESA DEPO", e)


@receiver(post_save, sender=Stake)
def update_user_withraw_power_onstake(sender, instance, created, **kwargs):
    try:
        if created and instance.bet_on_real_account is True:
            set_up = account_setting()
            now_withrawable = float(
                Account.objects.get(user_id=instance.user_id).withraw_power
            )
            # print(f'now_withrawableS:{now_withrawable}')
            added_amount = float(instance.amount) / set_up.withraw_factor
            # print(f'added_amountS:{added_amount}')
            total_withwawable = now_withrawable + added_amount

            if total_withwawable > 0:
                Account.objects.filter(user_id=instance.user_id).update(
                    withraw_power=total_withwawable
                )

    except Exception as e:
        print("Withrable cal err_onstake", e)



@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        try:
            my_pk = int(ipn_obj.invoice)
            mytransaction = CashDeposit.objects.get(pk=my_pk)
            assert ipn_obj.mc_gross == mytransaction.amount and ipn_obj.mc_currency == 'USD'
        except Exception:
            logger.exception('Paypal ipn_obj data not valid!')
        else:
            logger.exception('Confirmed Comleted Paypal Deposit Transaction!')
            mytransaction.confirmed = True
            mytransaction.save()
       
    else:
        logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)


valid_ipn_received.connect(paypal_payment_received)

