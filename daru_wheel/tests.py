from django.test import TestCase
from users.models import User
from account.models import *#Currency,CashDeposit
from daru_wheel.models import (
    Stake,
    CashStore,
    OutCome,
    Selection,
    DaruWheelSetting,
)
import random

def create_test_user(username):
    """simplify create_test_user"""
    ran_value = random.randint(1, 99)
    email = f"user{ran_value}@darucasino.com"

    return User.objects.create(username=str(username), email=email)


def deposit_to_test_user(user_id, amount=10000,currency='KES'):      
    Currency.objects.create(name='KES',rate=1)
    Currency.objects.create(name='USD',rate=100)
    if currency=='KES':
        c1=Currency.objects.get(id=1)
    else:
        c1=Currency.objects.get(id=2)    
    
    CashDeposit.objects.create(user_id=user_id, amount=amount, confirmed=True,currency=c1)
    
    
    
class StakeTestCase(TestCase):
    def setUp(self):
        self.user = create_test_user('user')
        deposit_to_test_user(self.user.id, amount=10000,currency='KES')
      

        self.marketselection1, _ = Selection.objects.get_or_create(
            id=1,
            # mrtype=self.market,
            name="RED",
            odds=2,
        )

        self.marketselection2, _ = Selection.objects.get_or_create(
            id=2,
            # mrtype=self.market,
            name="YELLOW",
            odds=2,
        )

    def test_no_balance_bet(self):

        self.assertEqual(current_account_bal_of(self.user.id), 10000)
        self.assertEqual(current_account_trialbal_of(self.user.id), 50000)

        Stake.objects.create(user=self.user,spinx=True,  amount=1000)
        Stake.objects.create(user=self.user, amount=60000)

        self.assertEqual(current_account_bal_of(self.user.id), 10000)

        Stake.objects.create(user=self.user,spinx=True, bet_on_real_account=True, amount=500)
        Stake.objects.create(user=self.user,spinx=False, bet_on_real_account=True, amount=500)
        Stake.objects.create(user=self.user,spinx=True, bet_on_real_account=True, amount=10000)
        Stake.objects.create(user=self.user,  bet_on_real_account=True, amount=10000)

        self.assertEqual(Stake.objects.count(), 3)
        
    def test_neative_bet(self):
        Stake.objects.create(user=self.user, bet_on_real_account=True, amount=-100)
        Stake.objects.create(user=self.user, bet_on_real_account=True, amount=-100)

        self.assertEqual(Stake.objects.count(), 0)

        Stake.objects.create(user=self.user, bet_on_real_account=True, amount=100)
        Stake.objects.create(user=self.user, bet_on_real_account=True, amount=100)

        self.assertEqual(Stake.objects.count(), 2) 
        
        
