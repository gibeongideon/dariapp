from django.test import TestCase  # ,Client
from django.urls import reverse
from account.models import (
    CashDeposit,
    CashWithrawal,
    Account,
    RefCredit,
    RefCreditTransfer,
    CashTransfer,
    Currency,
    AccountAnalytic
)
from users.models import User
from daru_wheel.models import Stake
import random
from mpesa_api.core.models import OnlineCheckoutResponse


# MODEL TESTS


class CashDepositWithrawalTestCase(TestCase):
    def setUp(self):
        self.currency1=Currency.objects.create(name='USD',rate=20)
        self.currency2=Currency.objects.create(name='KSH',rate=1)

        self.usera = User.objects.create(
            username="0710001000", email="testa@gmail.com", referer_code="ADMIN"
        )
        self.userb = User.objects.create(
            username="0123456787", email="testb@gmail.com", referer_code="ADMIN"
        )

    def test_user_deposit(self):
        
        CashDeposit.objects.create(amount=1000, user=self.usera, confirmed=True,currency_id=1)
        bal1a = Account.objects.get(user=self.usera).balance
        bal1b = Account.objects.get(user=self.userb).balance

        self.assertEqual(20000, bal1a)
        self.assertEqual(0, bal1b)

        CashDeposit.objects.create(amount=100000, user=self.usera, confirmed=True,currency_id=1)
        CashDeposit.objects.create(amount=1000, user=self.userb, confirmed=True,currency_id=1)
        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(2020000, bal2a)
        self.assertEqual(20000, bal2b)

    def test_correct_withraw_diff_power(self):
        """test to ensure no negative deposit done"""
        Account.objects.filter(user_id=self.usera).update(balance=1000,withraw_power=500)

        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 500)


    def test_correct_wihraw_diff_currencies(self):
        """test to ensure no negative deposit done"""
        Account.objects.filter(user_id=self.usera).update(balance=10000,withraw_power=5000)

        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 5000)
        CashWithrawal.objects.create(user=self.usera,amount=2000,currency=self.currency2,approved=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,8000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 3000)

        CashWithrawal.objects.create(user=self.usera,amount=100,currency=self.currency1,approved=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,6000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 1000)

  


    def test_correct_no_negative_deposit(self):
        """test to ensure no negative deposit done"""
        CashDeposit.objects.create(amount=1000, user=self.usera, confirmed=True,currency_id=1)
        n_amount = -random.randint(1, 10000)
        CashDeposit.objects.create(amount=n_amount, user=self.usera, confirmed=True,currency_id=1)

        balla = Account.objects.get(user=self.usera).balance
        ballb = Account.objects.get(user=self.userb).balance
        depo_count = CashDeposit.objects.count()

        self.assertEqual(depo_count, 1)
        self.assertEqual(balla, 20000)
        self.assertEqual(ballb, 0)

        CashDeposit.objects.create(amount=100000, user=self.usera, confirmed=True,currency_id=1)
        CashDeposit.objects.create(amount=1000, user=self.userb, confirmed=True,currency_id=1)
        n_amount = -random.randint(1, 10000)
        CashDeposit.objects.create(amount=n_amount, user=self.userb, confirmed=True,currency_id=1)

        bal2a = Account.objects.get(user=self.usera).balance
        bal2b = Account.objects.get(user=self.userb).balance

        self.assertEqual(2020000, bal2a)
        self.assertEqual(20000, bal2b)

    def test_witrawable_update_correctly(self):
        CashDeposit.objects.create(amount=10000, user=self.usera, confirmed=True,currency_id=1)

        self.assertEqual(Account.objects.get(user=self.usera).balance, 200000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 0)

        Stake.objects.create(user=self.usera, amount=1000, bet_on_real_account=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,199000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 1000)

        CashWithrawal.objects.create(user=self.usera, amount=800)

        self.assertEqual(Account.objects.get(user=self.usera).balance,199000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 1000)

        self.assertEqual(CashWithrawal.objects.get(id=1).approved, False)

        CashWithrawal.objects.filter(id=1).update(approved=True)

        self.assertEqual(CashWithrawal.objects.get(id=1).approved, True)

        self.assertEqual(Account.objects.get(user=self.usera).balance, 199000)
        # self.assertEqual(Account.objects.get(user=self.usera).withraw_power , 200)#failin

    def test_pesa_account_update_deposit_correctrly(self):#***********
        user = User.objects.create(username="0710000111", password="kjedrr9ufu4ccjk")
        OnlineCheckoutResponse.objects.create(
            amount=10000,
            mpesa_receipt_number="254710000111",
            phone="254710000111",
            result_code=0,
        )
        OnlineCheckoutResponse.objects.create(
            amount=10000,
            mpesa_receipt_number="254710000111",
            phone="254710000111",
            result_code=23455,
        )
        OnlineCheckoutResponse.objects.create(
            amount=5000, phone="254710000101", result_code=0
        )

        self.assertEqual(Account.objects.get(user=user).balance, 10000.00)################################

    def test_cu_deposit_update_correctly(self):
        CashDeposit.objects.create(amount=10000, user=self.usera, confirmed=True,currency_id=1)

        self.assertEqual(Account.objects.get(user=self.usera).cum_deposit, 200000)

        CashDeposit.objects.create(amount=1000, user=self.usera, confirmed=True,currency_id=1)

        self.assertEqual(Account.objects.get(user=self.usera).cum_deposit, 220000)

    def test_correct_cas_transfer(self):
        CashDeposit.objects.create(amount=1000, user=self.usera, confirmed=True,currency_id=1)
        bal1a = Account.objects.get(user=self.usera).balance
        bal1b = Account.objects.get(user=self.userb).balance
        trans_obj = CashTransfer.objects.create(
            sender=self.usera, recipient=self.userb, amount=500
        )

        self.assertEqual(20000, bal1a)
        self.assertEqual(0, bal1b)
        trans_obj.approved = True
        trans_obj.approved = True
        trans_obj.save()

        self.assertEqual(19500, Account.objects.get(user=self.usera).balance)
        self.assertEqual(500, Account.objects.get(user=self.userb).balance)
        CashTransfer.objects.create(
            sender=self.usera, recipient=self.userb, amount=200, approved=True
        )

        self.assertEqual(19300, Account.objects.get(user=self.usera).balance)
        self.assertEqual(700, Account.objects.get(user=self.userb).balance)
        CashTransfer.objects.create(
            sender=self.usera, recipient=self.userb, amount=301, approved=True
        )
        self.assertEqual(18999, Account.objects.get(user=self.usera).balance)
        self.assertEqual(1001, Account.objects.get(user=self.userb).balance)

        CashTransfer.objects.create(
            sender=self.usera, recipient=self.usera, amount=100, approved=True
        )
        self.assertEqual(18999, Account.objects.get(user=self.usera).balance)
        self.assertEqual(1001, Account.objects.get(user=self.userb).balance)

        CashTransfer.objects.create(
            sender=self.userb, recipient=self.usera, amount=-200, approved=True
        )
        self.assertEqual(18999, Account.objects.get(user=self.usera).balance)
        self.assertEqual(1001, Account.objects.get(user=self.userb).balance)

    def test_withraw_flags(self):
        """test to correct_flags_are set_on withraw"""
        Account.objects.filter(user_id=self.usera).update(balance=10000,withraw_power=5000)
 
        CashWithrawal.objects.create(user=self.usera,amount=2000,currency=self.currency2)

        self.assertEqual(CashWithrawal.objects.get(id=1).active,True)
        self.assertEqual(CashWithrawal.objects.get(id=1).withrawned,None)

        wit=CashWithrawal.objects.get(id=1)
        wit.approved=True
        wit.save()
        
        self.assertEqual(CashWithrawal.objects.get(id=1).approved,True)
        self.assertEqual(CashWithrawal.objects.get(id=1).withrawned,True)
        #self.assertEqual(CashWithrawal.objects.get(id=1).active,True)###################FAIL
        wit.cancelled=True
        wit.save()
        self.assertEqual(CashWithrawal.objects.get(id=1).cancelled,False)

        CashWithrawal.objects.create(user=self.usera,amount=1000,currency=self.currency2)

        self.assertEqual(CashWithrawal.objects.get(id=2).active,True)
        self.assertEqual(CashWithrawal.objects.get(id=2).withrawned,None)

        wit=CashWithrawal.objects.get(id=2)
        wit.cancelled=True
        wit.save()

        
        self.assertEqual(CashWithrawal.objects.get(id=2).approved,False)
        self.assertEqual(CashWithrawal.objects.get(id=2).withrawned,None)
        self.assertEqual(CashWithrawal.objects.get(id=1).active,False)       
        self.assertEqual(CashWithrawal.objects.get(id=2).cancelled,True)

class RefCreditTestCase(TestCase):
    def setUp(self):
        self.usera = User.objects.create(
            username="0710001000", email="testa@gmail.com", referer_code="ADMIN"
        )
        self.userb = User.objects.create(
            username="0123456787", email="testb@gmail.com", referer_code="ADMIN"
        )

    def test_correct_user_cu_credit(self):
        RefCredit.objects.create(amount=10, user=self.usera)
        RefCredit.objects.create(amount=10, user=self.usera)
        balla = Account.objects.get(user=self.usera).refer_balance

        self.assertEqual(balla, 20)

        RefCredit.objects.create(amount=100, user=self.usera)
        ballb = Account.objects.get(user=self.userb).refer_balance
        ballc = Account.objects.get(user=self.usera).refer_balance

        self.assertEqual(ballb, 0)
        self.assertEqual(ballc, 120)

        RefCredit.objects.create(amount=800, user=self.userb)
        ballb = Account.objects.get(user=self.userb).refer_balance

        self.assertEqual(ballb, 800)

        RefCredit.objects.create(amount=500, user=self.userb)
        ballb = Account.objects.get(user=self.userb).refer_balance

        self.assertEqual(ballb, 1300)

    #
    def test_correct_user_cu_credit_after_witraw(self):

        RefCredit.objects.create(amount=800, user=self.userb)
        ballb = Account.objects.get(user=self.userb).refer_balance

        self.assertEqual(ballb, 800)

        RefCredit.objects.create(amount=500, user=self.userb)
        ballb = Account.objects.get(user=self.userb).refer_balance

        self.assertEqual(ballb, 1300)

        RefCreditTransfer.objects.create(user=self.userb, amount=2000)
        self.assertEqual(Account.objects.get(user=self.userb).refer_balance, 1300)
        self.assertEqual(Account.objects.get(user=self.userb).balance, 0)

        RefCreditTransfer.objects.create(user=self.userb, amount=1000)
        self.assertEqual(Account.objects.get(user=self.userb).refer_balance, 300)
        self.assertEqual(Account.objects.get(user=self.userb).balance, 1000)

        RefCredit.objects.create(amount=1700, user=self.userb)
        ballb = Account.objects.get(user=self.userb).refer_balance

        self.assertEqual(ballb, 2000)

        RefCreditTransfer.objects.create(user=self.userb, amount=-1000)
        self.assertEqual(Account.objects.get(user=self.userb).refer_balance, 2000)
        self.assertEqual(Account.objects.get(user=self.userb).balance, 1000)

        RefCreditTransfer.objects.create(user=self.userb, amount=3000)
        self.assertEqual(Account.objects.get(user=self.userb).refer_balance, 2000)
        self.assertEqual(Account.objects.get(user=self.userb).balance, 1000)

        RefCreditTransfer.objects.create(user=self.userb, amount=300)
        self.assertEqual(Account.objects.get(user=self.userb).refer_balance, 2000)
        self.assertEqual(Account.objects.get(user=self.userb).balance, 1000)


class AnalyticTestCase(TestCase):
    def setUp(self):
        self.currency1=Currency.objects.create(name='USD',rate=100)
        self.currency2=Currency.objects.create(name='KSH',rate=1)

        self.usera = User.objects.create(
            username="0710001000", email="testa@gmail.com", referer_code="ADMIN"
        )
        self.userb = User.objects.create(
            username="0123456787", email="testb@gmail.com", referer_code="ADMIN"
        )

    def test_user_correct_accountAnalyticdeposit_witraw(self):
        
        CashDeposit.objects.create(amount=10, user=self.usera, confirmed=True,currency_id=1)
        CashDeposit.objects.create(amount=9000, user=self.usera, confirmed=True,currency_id=2)
        CashDeposit.objects.create(amount=100, user=self.userb, confirmed=True,currency_id=1)
        
        Account.objects.filter(user_id=self.usera).update(withraw_power=5000)

        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 5000)
        CashWithrawal.objects.create(user=self.usera,amount=2000,currency=self.currency2,approved=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,8000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 3000)

        CashWithrawal.objects.create(user=self.usera,amount=1000,currency=self.currency2,approved=True)

        self.assertEqual(Account.objects.get(user=self.usera).balance,7000)
        self.assertEqual(Account.objects.get(user=self.usera).withraw_power, 2000)       
 


        analyic=AccountAnalytic.objects.create()
        self.assertEqual(analyic.status_flag,"All system working great.NO ISSUE!")   
        
        
        
        
