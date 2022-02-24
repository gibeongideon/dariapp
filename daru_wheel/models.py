from django.db import models
from django.conf import settings
from django.db.models import Sum
from datetime import timedelta
from random import randint
from django.utils import timezone
try:
    from account.models import (
    current_account_trialbal_of,current_account_bal_of,
    update_account_trialbal_of,update_account_bal_of, 
    refer_credit_create,
    )    
except ImportError:
    pass    
from django.contrib.auth import get_user_model
User = get_user_model()

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        

class DaruWheelSetting(TimeStamp):
    return_val = models.FloatField(default=0, blank=True, null=True)
    min_redeem_refer_credit = models.FloatField(default=1000, blank=True, null=True)
    refer_per = models.FloatField(default=0, blank=True, null=True)
    per_to_keep = models.FloatField(default=5, blank=True, null=True)

    curr_unit = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    min_bet = models.DecimalField(
        max_digits=5, default=49.9, decimal_places=2, blank=True, null=True
    )
    win_algo = models.IntegerField(
        default=1,
        help_text="1=Random win_RECO,2=Using i win rate  Algo,3=Sure win_to_impress_",
        blank=True,
        null=True,
    )
    trial_algo = models.IntegerField(
        default=1,
        help_text="1=Normal win_RECO,2=Super win_to_impress,others=Use_win_algo_above",
        blank=True,
        null=True,
    )
    big_win_multiplier = models.FloatField(default=10, blank=True, null=True)

    class Meta:
        db_table = "d_daruwheel_setup"


def wheel_setting():
    set_up, created = DaruWheelSetting.objects.get_or_create(id=1)
    return set_up


class Selection(TimeStamp):
    name = models.CharField(max_length=100, blank=True, null=True)
    odds = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def all_selection(cls):
        return cls.objects.all()

    @classmethod
    def selection_id_list(cls):
        return [_mselect.id for _mselect in cls.objects.all()]

    @classmethod
    def selection_verbose_list(cls):
        return [
            (_mselect.id, _mselect.name, _mselect.odds)
            for _mselect in cls.objects.all()
        ]



class Stake(TimeStamp):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_wp_istakes",
        blank=True,
        null=True,
    )

    marketselection = models.ForeignKey(
        Selection,
        on_delete=models.CASCADE,
        related_name="imarketselections",
        blank=True,
        null=True,
    )  #
    amount = models.DecimalField(
        ("amount"), max_digits=12, decimal_places=2, default=50
    )
    current_bal = models.FloatField(max_length=10, default=0,blank=True, null=True)  # R
    stake_placed = models.BooleanField(blank=True, null=True)  #
    has_record = models.BooleanField(blank=True, null=True)  #
    bet_on_real_account = models.BooleanField(default=False)
    outcome_received = models.BooleanField(default=False, blank=True, null=True)
    spinned = models.BooleanField(default=False, blank=True, null=True)


    def __str__(self):
        return f"stake:{self.amount} by:{self.user}"

    @property
    def this_user_has_cash_to_bet(self):
        set_up = wheel_setting()
        if float(self.amount) > set_up.min_bet:  # unti neative values
            if not self.bet_on_real_account:
                try:
                    if current_account_trialbal_of(self.user_id) >= self.amount:
                        return True
                    return False
                except Exception as e:
                    return e
            else:
                try:
                    if current_account_bal_of(self.user_id) >= self.amount:
                        return True
                    return False
                except Exception as e:
                    return e
        else:
            return False

    def deduct_amount_from_this_user_account(self):
        if not self.bet_on_real_account:
            new_bal = current_account_trialbal_of(self.user_id) - float(self.amount)
            update_account_trialbal_of(self.user_id, new_bal)  # F3
        else:
            new_bal = current_account_bal_of(self.user_id) - float(self.amount)
            self.current_bal = new_bal
            update_account_bal_of(self.user_id, new_bal)  # F3

    def bet_status(self):
        try:
            return OutCome.objects.get(stake_id=self.id).win_status 
        except Exception as e:
            print(f"daru_STATUS ERROR:{e}")
            return "pending"

    @classmethod
    def unspinned(cls, user_id):
        return [
            obj.id
            for obj in cls.objects.filter(user=user_id, spinned=False)
        ]

    @property
    def active_spins(self):
        return self.unspinned(self.user.id)
        # pass

    @property
    def expected_win_amount(self):
        if self.bet_status()=='pending':
            return 'E'+str(self.marketselection.odds*float(self.amount))
        if self.bet_status()=='win':
            return self.marketselection.odds*float(self.amount)            
        else:
            return self.amount    

    def save(self, *args, **kwargs):
        """ Bet could only be registered if user got enoug real or trial balance """
        if not self.pk:
            if current_account_trialbal_of(self.user_id) < 10000:#auto_renew_trial_balance
                update_account_trialbal_of(user_id=self.user_id,new_bal=50000+current_account_trialbal_of(self.user_id))

            if self.this_user_has_cash_to_bet:  # then
                self.deduct_amount_from_this_user_account()
                self.stake_placed = True
            else:
                return  # no db table record to create!
    
            super().save(*args, **kwargs)  # create a db record


class CashStore(models.Model):
    give_away = models.DecimalField(
        ("give_away"), max_digits=12, decimal_places=2, default=0,blank=True, null=True
    )
    to_keep = models.DecimalField(
        ("to_keep"), max_digits=12, decimal_places=2, default=0,blank=True, null=True
    )

    @property
    def all_amount(self):
        try:
            return self.give_away+self.to_keep
        except:
            return 0

class OutCome(TimeStamp):
    stake = models.OneToOneField(
        Stake, on_delete=models.CASCADE, related_name="istakes", blank=True, null=True
    )
    cashstore = models.ForeignKey(
        CashStore,
        on_delete=models.CASCADE,
        related_name="cashstores",
        blank=True,
        null=True,
    )
    result = models.IntegerField(blank=True, null=True)
    pointer = models.IntegerField(blank=True, null=True)
    closed = models.BooleanField(default=False, blank=True, null=True)

    return_per = models.FloatField(blank=True, null=True)
    gain = models.DecimalField(
        ("gain"), max_digits=100, decimal_places=5, blank=True, null=True
    )
    active = models.BooleanField(blank=True, null=True)

    @property
    def real_bet(self):
        try:
            return self.stake.bet_on_real_account
        except:
            return None

    @property
    def current_update_give_away(self):
        return CashStore.objects.get(id=1).give_away

    @staticmethod
    def update_give_away(new_bal):
        CashStore.objects.filter(id=1).update(give_away=new_bal)

    @property
    def current_update_to_keep(self):
        return CashStore.objects.get(id=1).to_keep

    @staticmethod
    def update_to_keep(new_bal):
        CashStore.objects.filter(id=1).update(to_keep=new_bal)

    def user_cum_depo(self):
        pass

    def give_away(self):
        try:
            return self.cashstore.give_away
        except Exception as e:
            return e

    def real_account_result_algo(self):
        try:
            stake_obj=self.stake
            odd = float(stake_obj.marketselection.odds)
            stak = float(stake_obj.amount)
            set_up = wheel_setting()

            if float(self.current_update_give_away) >= set_up.big_win_multiplier * (
                stak * odd
            ):
                # print('quolify_4_B-WIN')
                resu = randint(1, 5)  # properbility_of_winnin_bi
                if resu == 1:
                    # print('and_Luck_Strikes!')
                    return 5
                else:  # RRR
                    # print('..but_no_luck!')
                    pass

            if float(self.current_update_give_away) >= (
                stak * odd
            ):  # *self.stake.marketselection.odds):  ##TO IMPLEMENT
                # print('N-Win')
                set_up = wheel_setting()
                # return 1
                if set_up.win_algo == 1:
                    return randint(1, 2)

                if set_up.win_algo == 2:
                    resu = randint(1, 3)
                    if resu != 1:
                        return 1
                    return 2

                if set_up.win_algo == 3:
                    return 1
                else:
                    return 2
            return 2
        except Exception as e:
            return e

    def trial_account_result_algo(self):
        set_up = wheel_setting()
        if set_up.trial_algo == 1:  # normal win trial
            return randint(1, 2)

        elif set_up.trial_algo == 2:  # super win trial
            random_val = randint(1, 3)
            if random_val == 3:
                return 2
            return 1
        else:
            pass  # toREALNormal Win Algo


    @staticmethod
    def result_to_segment(results=None, segment=29):
        from random import randint, randrange
        if results is None:
            # print('Results is NONE')
            results = randint(1, 2)
        if results == 1:
            rand_odd = randrange(1, segment, 2)
            if rand_odd == 13:
                return 7
            return rand_odd  # odd no b/w 1 to segment(29)
        elif results == 2:
            rand_even = randrange(2, segment, 2)
            if rand_even == 28:
                return 16
            return rand_even  # even no b/w 2 to segment(29)
        elif results == 5:
            return 13  # Bi_win
        elif results == 10:
            return 28  # Loose_Turn


    def selection(self):
        if self.stake is not None:
            return self.stake.marketselection.id
        else:
            return None
    @property
    def segment(self):
        stake_obj=self.stake
        if stake_obj is not None: 
            if stake_obj.marketselection.id == 2:
                return self.result_to_segment(results=self.result)
            else:
                if self.result == 1:
                    return self.result_to_segment(results=2)
                else:
                    return self.result_to_segment(results=1)
        else:
            return self.result_to_segment(results=self.result)
            

    def update_user_trial_account(self, this_user, add_amount):
        current_bal = current_account_trialbal_of(this_user)  # F1
        new_bal = current_bal + add_amount
        update_account_trialbal_of(this_user, new_bal)  # with new_bal

    def update_user_real_account(self, this_user, add_amount):
        current_bal = current_account_bal_of(this_user)  # F1
        new_bal = current_bal + add_amount  # ard Code odds
        update_account_bal_of(this_user, new_bal)  # with new_bal

    def update_values(self):
        try:
            set_up = wheel_setting()
            stake_obj=self.stake
            amount = float(stake_obj.amount)
            odds = float(stake_obj.marketselection.odds)
            per_for_referer = set_up.refer_per  # Settings
            win_amount = (amount * odds)-amount
            
            if per_for_referer > 100:  # Enforce 0<=p<=100 TODO
                per_for_referer = 0

            ref_credit = (per_for_referer / 100) * win_amount
            
            return win_amount, ref_credit
        except Exception as e:
            print("update_al_error")
            print(e)

    @property
    def win_status(self):
        if self.result == 1 or self.result == 5:
           return "win"
        return "loss"

    @classmethod
    def open_for_spin(cls, user_id):
        return cls.objects.filter(user_id=user_id, closed=False)


    @staticmethod
    def update_reference_account(user_id, ref_credit, trans_type):
        # print(user_id,ref_credit,trans_type)
        try:
            this_user = User.objects.get(id=user_id)
            this_user_refercode = (
                this_user.referer_code
            )  # first name is used as referer code
            if not this_user_refercode:
                this_user_refercode = User.objects.get(id=1).code  # settings

            referer_users = User.objects.filter(code=this_user_refercode)
            for referer in referer_users:
                refer_credit_create(referer, this_user.username, ref_credit)  # F4

        except Exception as e:
            return e  # TODO
            
    def run_update_winner_losser_on_real_account(self):       
        this_user_stak_obj=self.stake
        user_id = this_user_stak_obj.user.id        
        win_amount, ref_credit = self.update_values()
        
        if self.result == 1:  ###
            trans_type = "Ispin Win"
            all_amount = win_amount + float(this_user_stak_obj.amount)
                        
            # UUB
            current_bal = float(self.current_update_give_away)
            new_bal = current_bal - win_amount - ref_credit
            self.update_give_away(new_bal)
            self.update_user_real_account(user_id, all_amount) 
            
            
            if ref_credit > 0:
                trans_type = "credit on R Win"
                self.update_reference_account(user_id, ref_credit, trans_type)
                

        elif self.result == 2:
            # UUB
            set_up = wheel_setting()
            current_give_away_bal = float(self.current_update_give_away)
            current_to_keep_bal = float(self.current_update_to_keep)
            _to_keep = (float(set_up.per_to_keep) / 100) * float(
                    self.stake.amount
                )
            _away = float(self.stake.amount) - _to_keep - ref_credit  # re
            
            away = current_give_away_bal + _away
            to_keep = current_to_keep_bal + _to_keep
            self.update_give_away(away)
            self.update_to_keep(to_keep)
            
            if ref_credit > 0:
                trans_type = "credit on R Loss"
                self.update_reference_account(user_id, ref_credit, trans_type)                

        if self.result == 5:  ###
            set_up = wheel_setting()
            trans_type = "Big Win"
            all_amount = float(win_amount * set_up.big_win_multiplier) + float(this_user_stak_obj.amount)
            
            # UUB
            sub_amount = all_amount - float(this_user_stak_obj.amount)
            current_bal = float(self.current_update_give_away)
            new_bal = current_bal - sub_amount
            self.update_give_away(new_bal)
            
            self.update_user_real_account(user_id, all_amount)
                    

             
    def run_update_winner_losser_on_trial_account(self ):
        this_user_stak_obj=self.stake
        user_id = this_user_stak_obj.user.id
        win_amount, ref_credit = self.update_values()
        if self.result == 1:
           all_amount = win_amount + float(this_user_stak_obj.amount)
           self.update_user_trial_account(user_id, all_amount)             
          
    @property
    def determine_result_algo(self): 
        if not self.real_bet:
            return self.trial_account_result_algo()
        else:
            return self.real_account_result_algo()
        
            
    def run_account_update(self):
        stake_obj = self.stake
    
        if stake_obj.bet_on_real_account: 
           self.pointer = self.segment
           self.run_update_winner_losser_on_real_account()
        else:
            self.pointer = self.segment
            self.run_update_winner_losser_on_trial_account()          
            

    def save(self, *args, **kwargs):
        if not self.pk and not self.closed:
            mstore, _ = CashStore.objects.get_or_create(id=1)
            self.cashstore = mstore
            try:
                self.result=self.determine_result_algo
                self.run_account_update()
                self.closed = True
                super().save(*args, **kwargs)
            except Exception as e:
                print(e)
                return
             
