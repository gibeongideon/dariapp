import json
from channels.generic.websocket import WebsocketConsumer
from .models import OutCome, Stake
from account.models import current_account_bal_of


class QspinConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.accept()

    def disconnect(self, close_code):
        pass

    def update_stake_as_spinned(self, stakeid):
        Stake.objects.filter(user=self.user, id=stakeid).update(spinned=True)

    def return_pointer(self):
        spinz = Stake.unspinned(self.user)
        if len(spinz) > 0:
            spin_id = spinz[0]
            self.update_stake_as_spinned(spin_id)
            pointer_obj, _ = OutCome.objects.get_or_create(stake_id=spin_id)
            return pointer_obj.pointer
        else:
            return 777

    # Receive pointer from spin group
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ipointer = text_data_json["ipointer"]
        ipointer = self.return_pointer()
        if ipointer:
            self.send(text_data=json.dumps({"ipointer": ipointer,}))


class XspinConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.accept()

    def disconnect(self, close_code):
        pass

    def update_stake_as_spinned(self, stakeid):
        Stake.objects.filter(user=self.user, id=stakeid).update(spinned=True)
       
   
    def return_pointer(self):
        spinz = Stake.unspinnedx(self.user)
        if len(spinz) > 0:
            spin_id = spinz[0]
            self.update_stake_as_spinned(spin_id)
            pointer_obj, _ = OutCome.objects.get_or_create(stake_id=spin_id)
            win_a=float(pointer_obj.win_multiplier*pointer_obj.stake.amount)
            return pointer_obj.pointer,win_a
        else:
            return 888,None

    # Receive pointer from spin group
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ipointer = text_data_json["ipointer"]
        
        ipointer,win_a = self.return_pointer()
        self.send(text_data=json.dumps({"ipointer": ipointer,"win_a": win_a,}))

               
                
                     
            
            

            
