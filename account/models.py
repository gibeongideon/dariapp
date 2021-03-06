# from locale import currency
from django.db import models
from django.conf import settings
from .exceptions import NegativeTokens  # , NotEnoughTokens # LockException,
from decimal import Decimal
from django.db.models import Sum
from mpesa_api.core.mpesa import Mpesa
import math
from .paypal_client import CreatePayouts
import logging

logger = logging.getLogger(__name__)

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True       
        
class AccountSetting(TimeStamp):
    min_redeem_refer_credit = models.FloatField(default=1000, blank=True, null=True)
    auto_approve = models.BooleanField(default=False, blank=True, null=True)
    auto_approve_cash_trasfer = models.BooleanField(default=False, blank=True, null=True)
    withraw_factor = models.FloatField(default=1, blank=True, null=True)

    class Meta:
        db_table = "d_accounts_setup"

def account_setting():
    set_up, created = AccountSetting.objects.get_or_create(id=1)  # fail save
    return set_up

class Account(TimeStamp):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="user_accounts",
        blank=True,
        null=True,
    )
    token_count = models.IntegerField(default=0, blank=True, null=True)

    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    actual_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    withraw_power = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )

    refer_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    trial_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=50000, blank=True, null=True
    )

    cum_deposit = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.0, blank=True, null=True
    )
    cum_withraw = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.0, blank=True, null=True
    )
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return "Account No: {0} Balance: {1}".format(self.user, self.balance)

    class Meta:
        db_table = "d_accounts"
        ordering = ("-user_id",)

    @property
    def withrawable_balance(self):
        return min(self.withraw_power, self.balance)

    @property
    def min_refer_to_transfer(self):
        try:
            set_up=account_setting()
            return set_up.min_redeem_refer_credit
        except:
            return 200 #TODO    

    @property
    def balance_usd(self):
        rate_to_usd=Currency.objects.get(name='USD').rate
        return round(self.balance/rate_to_usd,2)

    @property
    def withrawable_balance_usd(self):
        rate_to_usd=Currency.objects.get(name='USD').rate
        return round(self.withrawable_balance/rate_to_usd,2)

    @property
    def c_loss(self):

        return self.cum_deposit-(self.cum_withraw+self.balance)

    def add_tokens(self, number):
        """Increase user tokens amount watch over not to use negative value.

        self -- user whose token_count field  gonna be increased
        number -- tokens amount, must be integer

        In case negative number no changes happened.
        """
        int_num = int(number)
        if int_num > 0:
            self.token_count += int_num

    def decrease_tokens(self, number):
        """Decrease user tokens amount watch over not to set negative value.

        Keyword arguments:
        self -- user whose token_count field is to be decreased
        number -- tokens amount, must be integer, cannot be greater
                than token_count

        In case number is greater than user token_count NegativeTokens
        exception raised, otherwise simply decrease token_count with number.
        """
        int_num = int(number)
        if self.token_count - int_num >= 0:
            self.token_count -= int_num
        else:
            raise NegativeTokens()

class Currency(TimeStamp):
    """Store currencies with specified name and rate to token amount."""

    name = models.CharField(max_length=30, blank=True, null=True)
    rate = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)

    class Meta:
        db_table = "d_currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        """Simply present currency name and it's rate."""
        return self.name + " |Rate: " + str(self.rate)

    @classmethod
    def get_tokens_amount(cls, currency_name, value):
        """Convert value in specified currency to tokens.

        Keyword arguments:
        cls -- enable connect to Currency model,
        currency_name -- allow to get specified currency,
        value -- float value represents amount of real money,

        Could raise Currency.DoesNotExist exception.
        Token value is rounded down after value multiplication by rate.
        """
        curr = cls.objects.get(name=currency_name)
        tokens = value * float(curr.rate)
        tokens_floor = math.floor(tokens)
        return tokens_floor

    @classmethod
    def get_withdraw_amount(cls, currency_name, tokens):
        """Convert tokens to amount of money in specified currency.

        Keyword arguments:
        cls -- enable connect to Currency model,
        currency_name -- allow to get specified currency,
        tokens -- integer value represents number of tokens,

        Could raise Currency.DoesNotExist exception and NegativeTokens
        exception.
        Returned object is casted to Decimal with two places precision.
        """
        curr = cls.objects.get(name=currency_name)
        if tokens < 0:
            raise NegativeTokens()

        value = Decimal(round(tokens / float(curr.rate), 2))
        return value


class RefCredit(TimeStamp):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ref_accountcredit_users",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    current_bal = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    credit_from = models.CharField(max_length=200, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    has_record = models.BooleanField(blank=True, null=True)
    approved = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = "d_refcredits"

    @property
    def refer_balance(self):
        try:
            return float(Account.objects.get(user_id=self.user_id).refer_balance)
        except Exception as e:
            print(e)
            return e

    def update_refer_balance(self):
        try:
            new_bal = self.refer_balance + float(self.amount)
            self.current_bal = new_bal
            Account.objects.filter(user_id=self.user_id).update(refer_balance=new_bal)
            self.closed = True

        except Exception as e:
            print("update_refer_balance", e)
            pass

    def save(self, *args, **kwargs):
        """ Overrride internal model save method to update balance on staking  """
        # if not self.closed:
        try:
            if not self.closed:
                self.update_refer_balance()

        except Exception as e:
            print("RefCredit:", e)
            pass
            # return
        super().save(*args, **kwargs)

class RefCreditTransfer(TimeStamp):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_refer_credit_trans",
        blank=True,
        null=True,
    )  # NOT CASCADE #CK
    amount = models.DecimalField(("amount"), max_digits=12, decimal_places=2, default=0)
    succided = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = "d_refcredit_trans"
        ordering = ("-created_at",)

    def __str__(self):
        return "User {0}:{1}".format(self.user, self.amount)


    def save(self, *args, **kwargs):
        """ Overrride internal model save method to update balance on deposit  """
        if not self.pk and self.amount > 0:
            try:
                set_up = account_setting()
                curr_refer_bal = current_account_referbal_of(self.user_id)
                if (
                    self.amount <= curr_refer_bal
                    and self.amount >= set_up.min_redeem_refer_credit
                    ):
                    new_refer_bal = curr_refer_bal - float(self.amount)
                    update_account_referbal_of(self.user_id, new_refer_bal)
                    curr_bal = current_account_bal_of(self.user_id)
                    new_bal = curr_bal + float(self.amount)
                    update_account_bal_of(self.user_id, new_bal)
                    self.succided = True
                    super().save(*args, **kwargs)
                else:
                    return
            except Exception as e:
                print("ReferTransERROR:", e)
                return
        else:
            return      


class CashDeposit(TimeStamp):
    """Represent single money deposit made by user using 'shop'.
    Define fields to store amount of money, using Decimal field with
    two places precision and maximal six digits, time of deposit creation,
    and connect every deposit with user and used currency.
    """

    # amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tokens = models.DecimalField(max_digits=12,decimal_places=2, blank=True, null=True)
    confirmed = models.BooleanField(default=False, blank=True, null=True)
    deposited = models.BooleanField(blank=True, null=True)
    deposit_type = models.CharField(
        max_length=100, default="Shop Deposit", blank=True, null=True
    )
    has_record = models.BooleanField(blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_deposits",
        blank=True,
        null=True,
    )

    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        """Simply present name of user connected with deposit and amount."""
        return self.user.username + " made " + str(self.amount) + " deposit"

    class Meta:
        db_table = "d_deposits"

    @property
    def current_bal(self):
        return current_account_bal_of(self.user_id)

    @property
    def status(self):
        if self.deposited:
            return "Success"
        return "Failed"


    def update_cum_depo(self):
        try:
            if not self.deposited:
                ctotal_balanc = current_account_cum_depo_of(self.user_id)  # F'
                new_bal = ctotal_balanc + int(self.amount_converted_to_tokens)
                update_account_cum_depo_of(self.user_id, new_bal)  # F
                # self.deposited = True
        except Exception as e:
            print(f"Daru:CashDeposit-update_cum_depo Error:{e}")  # Debug
            pass

    @property
    def amount_converted_to_tokens(self):
        try:
            # currency_name =Currency.objects.get(id=self.currency_id).name
            tokens=Currency.get_tokens_amount(self.currency.name, float(self.amount))
        except Exception as e:#Currency.DoesNotExist:
            print('FAIL CONVERT',e)
            tokens= self.amount 

        return tokens     

    def save(self, *args, **kwargs):
        """ Overrride internal model save method to update balance on deposit  """
        # if self.pk:
        if self.amount > 0:
            try:
                try:
                    if self.confirmed and not self.deposited:
                        ctotal_balanc = current_account_bal_of(self.user_id)  # F
                        self.tokens=self.amount_converted_to_tokens
                        new_bal = ctotal_balanc + int(self.amount_converted_to_tokens)
                        update_account_bal_of(self.user_id, new_bal)  # F
                        self.update_cum_depo()  #####
                        # self.update_tokens()###
                        self.deposited = True
                except Exception as e:
                    print(f"Daru:CashDeposit-Deposited Error:{e}")  # Debug
                    pass

                super().save(*args, **kwargs)  # dillow amount edit feature

            except Exception as e:
                print("DEPOSIT ERROR", e)  # issue to on mpesa deposit error
                return
            # super().save(*args, **kwargs) # allow mount edit
        else:
            return

class CashWithrawal(TimeStamp):  # sensitive transaction
    """Represent user's money withdrawal instance.
    Define fields to store amount of money, using Decimal field with
    two places precision and maximal six digits, time when withdraw is
    signaled and connect every withdraw with user and used currency.
    """

    # amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tokens = models.DecimalField(max_digits=12,decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    approved = models.BooleanField(default=False, blank=True, null=True)
    cancelled = models.BooleanField(default=False, blank=True, null=True)
    withrawned = models.BooleanField(blank=True, null=True)
    confirmed = models.BooleanField(blank=True, null=True)
    has_record = models.BooleanField(blank=True, null=True)
    withr_type = models.CharField(max_length=100,default='shop',blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_withrawals",
        blank=True,
        null=True,
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        """Simply present name of user connected with withdraw and amount."""
        return self.user.username + " want to withdraw " + str(self.amount)

    class Meta:
        db_table = "d_withrawals"
        get_latest_by='id'

    @property
    def user_account(self):
        return current_account_bal_of(
            self.user
        )  # Account.objects.get(user_id =self.user_id)

    @classmethod
    def withraw_amount(cls):
        return cls.objects.all()

    # @classmethod
    # def last_withrawal(cls,user,id):
    #     try:
    #         status=cls.objects.get(id=id).withraw_status

    #     except Exception as e: 
    #         status=None

    #     if status=='pending':
    #         return True
    #     return False 

    # @property
    # def previus_withrawal_is_incomplete(self):
    #     return self.last_withrawal(self.user,self.id-1)


    def update_user_withrawable_balance(self):
        try:
            now_withrawable = float(
                Account.objects.get(user_id=self.user_id).withraw_power
            )
            deduct_amount = float(self.amount_converted_to_tokens)
            total_withwawable = now_withrawable - deduct_amount

            if total_withwawable >= 0:
                Account.objects.filter(user=self.user).update(
                    withraw_power=total_withwawable
                )
        except Exception as e:
            print("update_user_withrawable_balance", e)
            pass

    @property  # TODO no hrd coding
    def charges_fee(self):
        if self.amount <= 100:
            return 0
        elif self.amount <= 200:
            return 0
        else:
            return 0

    def update_cum_withraw(self):
        try:
            if not self.withrawned:
                ctotal_balanc = current_account_cum_withraw_of(self.user_id)  # F
                new_bal = ctotal_balanc + int(self.amount_converted_to_tokens)
                update_account_cum_withraw_of(self.user_id, new_bal)  # F

        except Exception as e:
            print(f"Daru:CashWit-update_cum_wit Error:{e}")  # Debug
            pass

    @property
    def withraw_status(self):
        if self.cancelled:
            return "cancelled"
        if not self.approved:
            return "pending"
        if self.approved and self.withrawned and not self.confirmed:
            return "awaiting confirmation"
        if self.confirmed:
            return "success"
            
        return "failed"

    @property
    def amount_converted_to_tokens(self):
        try:
            tokens=Currency.get_tokens_amount(self.currency.name, float(self.amount))
        except Exception as e:#Currency.DoesNotExist:
            print('FAIL CONVERT',e)
            tokens= self.amount 

        return tokens     

    def save(self, *args, **kwargs):
        """ Overrride internal model save method to update balance on withraw """ 

        # if self.previus_withrawal_is_incomplete:
        #     return
       

        if not self.active:
            return

        if self.cancelled and not self.withrawned:
            self.active = False
            self.approved=False
        else:
            self.cancelled  =False

        if  self.confirmed and self.approved and self.withrawned:
            self.active=False             


        if (self.active and self.amount > 0):  # edit prevent # avoid data ma####FREFACCCC min witraw in settins
            account_is_active = self.user.active
            ctotal_balanc = current_account_bal_of(self.user_id)

            withrawable_bal = min(float(Account.objects.get(user_id=self.user_id).withraw_power)\
            ,float(Account.objects.get(user_id=self.user_id).balance))  

            if account_is_active:  # withraw cash ! or else no cash!
                try:
                    set_up = account_setting()
                    if set_up.auto_approve:
                        self.approved = True                        
                        
                    #DEDUCT
                    if (not self.withrawned and self.approved and not self.cancelled):  # stop repeated withraws and withraw only id approved by ADMIN
                        charges_fee = self.charges_fee  # TODO settings
                        self.tokens=self.amount_converted_to_tokens
                        if (self.tokens + charges_fee) <= withrawable_bal:
                            try:                           
                                new_bal = (
                                    ctotal_balanc - float(self.tokens) - charges_fee
                                )
                                update_account_bal_of(self.user_id, new_bal)  # F
                                self.update_cum_withraw()  ##
                                
                                self.withrawned = True  # transaction done
                                self.update_user_withrawable_balance()                                           

                            except Exception as e:
                                print("ACCC", e)                                  
                                
                                                            
                     #PAYOUTS          
                    if  self.approved and self.withrawned and not self.confirmed and not self.cancelled:
                        if self.withr_type=='mpesa': 
                            try:
                                Mpesa.b2c_request(self.user.phone_number,self.amount,)
                                self.confirmed = True                                                                
                            except Exception as e:
                                logger.exception(f'B2CashWithrawal:{e}')
                                pass                                    
                        elif self.withr_type=='paypal':
                             try:
                                 create_response = CreatePayouts(str(self.amount), self.user.email).create_payouts(True)
                             except Exception as e:
                                 logger.exception(f'paypal-Payout:{e}')
                                 pass
                             else:
                                  if int(create_response.status_code) == 201:
                                      self.confirmed = True 
                                           
                        elif self.withr_type=='shop' and self.withrawned:
                             self.confirmed = True 
                             self.active=False     ##  
                             
                except Exception as e:
                    print("CashWithRawal:", e)
                    return  # incase of error /No withrawing should happen
                    # pass

        if  self.confirmed and self.approved and self.withrawned:
            self.active=False 

        if  self.approved and not self.withrawned:
            self.active=False            

        super().save(*args, **kwargs)


# Helper functions


def current_account_bal_of(user_id):  # F2
    try:
        return float(Account.objects.get(user_id=user_id).balance)
    except Exception as e:
        return e


def current_account_withrawable_bal_of(user_id):  # F2
    try:
        return float(Account.objects.get(user_id=user_id).withrawable_balance())
    except Exception as e:
        return e


def update_account_bal_of(user_id, new_bal):  # F3
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id=user_id).update(balance=new_bal)
        # else:
        #     log_record(user_id, 0, "Account Error")  # REMOVE
    except Exception as e:
        return e


def current_account_trialbal_of(user_id):  # F2
    try:
        return float(Account.objects.get(user_id=user_id).trial_balance)
    except Exception as e:
        return e


def update_account_trialbal_of(user_id, new_bal):  # F3
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id=user_id).update(trial_balance=new_bal)
        # else:
        #     log_record(user_id, 0, "Account Error")  # REMOVE
    except Exception as e:
        return e


def current_account_referbal_of(user_id):  # F2
    try:
        return float(Account.objects.get(user_id=user_id).refer_balance)
    except Exception as e:
        return e


def update_account_referbal_of(user_id, new_bal):  # F3
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id=user_id).update(refer_balance=new_bal)
        # else:
        #     log_record(user_id, 0, "Account Error")  # REMOVE
    except Exception as e:
        return e


def refer_credit_create(credit_to_user, credit_from_username, amount):
    try:
        RefCredit.objects.create(
            user=credit_to_user, credit_from=credit_from_username, amount=amount
        )
    except Exception as e:
        print(f"RRR{e}")


def current_account_cum_depo_of(user_id):  # F2
    try:
        return float(Account.objects.get(user_id=user_id).cum_deposit)
    except Exception as e:
        return e

def update_account_cum_depo_of(user_id, new_bal):  # F3
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id=user_id).update(cum_deposit=new_bal)
        # else:
        #     pass
        #     # log_record(user_id,0,'Account Error') # REMOVE
    except Exception as e:
        return e

def current_account_cum_withraw_of(user_id):  # F2
    try:
        return float(Account.objects.get(user_id=user_id).cum_withraw)
    except Exception as e:
        return e

def update_account_cum_withraw_of(user_id, new_bal):  # F3
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id=user_id).update(cum_withraw=new_bal)
        else:
            pass
            # log_record(user_id,0,'Account Error') # REMOVE
    except Exception as e:
        return e
class CashTransfer(TimeStamp):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="senderss",
        blank=True,
        null=True,
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipientss",
        blank=True,
        null=True,
    )
    # pin = models.IntegerField(max_digits=6, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    approved = models.BooleanField(default=False, blank=True, null=True)
    cancelled = models.BooleanField(default=False, blank=True, null=True)
    success = models.BooleanField(blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def tranfer_cash_to_other_user(self):
        sender_bal = current_account_bal_of(self.sender)
        if (
            self.amount > 0
            and sender_bal >= self.amount
            and self.sender != self.recipient
        ):  ###
            recipient_bal = current_account_bal_of(self.recipient)

            new_bal_from = sender_bal - float(self.amount)
            update_account_bal_of(self.sender, new_bal_from)

            new_bal_to = recipient_bal + float(self.amount)
            update_account_bal_of(self.recipient, new_bal_to)
            self.success = True
            self.active=False
        else:
            self.success = False

    def status(self):
        if self.success:
            return "succided"
        if not self.approved and not self.cancelled:
            return "pending"
        else:
            return "failed"

    def save(self, *args, **kwargs):
        if self.active:
            if not self.cancelled:
                set_up = account_setting()
                if set_up.auto_approve_cash_trasfer:
                    self.approved = True 

                if self.approved and not self.success:
                    self.tranfer_cash_to_other_user()

                super().save(*args, **kwargs)    

            else:
                self.active=False 
                self.success=False
                super().save(*args, **kwargs)
                
        else:
            return        

class RegisterUrl(TimeStamp):
    success = models.BooleanField(default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            Mpesa.c2b_register_url()
        except  Exception as e:
            logger.exception(e)
        super().save(*args, **kwargs)

def cashtore():
    from daru_wheel.models import CashStore
    # all_amount=CashStore.objects.get(id=1).all_amount
    store_obj,created=CashStore.objects.get_or_create(id=1)
    return store_obj.all_amount

def unspinned():
    from daru_wheel.models import Stake
    total = Stake.objects.filter(
        bet_on_real_account=True,
        spinned=False,
        ).aggregate(amount=Sum("amount"))
    return total.get("amount") if total.get("amount") else 0
    
class AccountAnalytic(TimeStamp):
    gain = models.FloatField(default=0, blank=True, null=True)
    all_bets = models.IntegerField(default=1, blank=True, null=True)
    t_bal = models.FloatField(default=0, blank=True, null=True)
    t_wit = models.FloatField(default=0, blank=True, null=True)
    t_in = models.FloatField(default=0, blank=True, null=True)
    t_out = models.FloatField(default=0, blank=True, null=True)
    r_cred = models.FloatField(default=0, blank=True, null=True)
    diffe= models.FloatField(default=0, blank=True, null=True)
  
    flag= models.BooleanField(default=False, blank=True, null=True)

    @property
    def c_bal(self):
        total_cbal = Account.objects.aggregate(bal_amount=Sum("balance"),abal_amount=Sum("withraw_power"))
        if total_cbal.get("bal_amount"):
            return total_cbal.get("bal_amount")
        return 0

    @property
    def wit_amount(self):
        total = CashWithrawal.objects.filter(withrawned=True).aggregate(wit_amount=Sum("tokens"))

        if total.get("wit_amount"):
            return total.get("wit_amount")
        return 0
               
    @property
    def all_in(self):
        total = CashDeposit.objects.filter(deposited=True).aggregate(dep_amount=Sum("tokens"))
        # if total.get("dep_amount"):
        #    return total.get("dep_amount")
        return total.get("dep_amount") if total.get("dep_amount") else 0

    @property
    def ref_amount(self):
        total = Account.objects.aggregate(ref_amount=Sum("refer_balance"))

        if total.get("ref_amount"):
            return total.get("ref_amount")
        return 0
                              
    @property
    def all_out(self):   
        all_amount=float(cashtore()) 
        unspin=float(unspinned())

        return float(self.c_bal)+all_amount+float(self.wit_amount)+float(self.ref_amount)+unspin
    
    @property
    def diff(self):
        try:
            return (float(self.all_in)-float(self.all_out) )
        except Exception as e:
            return e   

    @property
    def status_flag(self):
        if self.t_out>self.t_in:
            return 'Red Flag.Out>IN.Something very Bad!'
        if self.t_in>self.t_out:
            return 'Yellow Flag.Out<In.Something wrong!'            
        return  "All system working great.NO ISSUE!"

    @property
    def severity(self):
        if self.t_in>self.t_out:
            return None
        if self.t_out>self.t_in:
            return False  
        else:
            return  True 

    def save(self, *args, **kwargs):
        if not self.pk:
            # self.gain=CashStore.objects.get(id=1).to_keep#CIRCULARIPORT
            self.t_bal=self.c_bal
            self.t_wit=self.wit_amount
            self.t_in=self.all_in
            self.t_out=self.all_out
            self.flag=self.severity
            self.diffe=self.diff

        super().save(*args, **kwargs)                                         
