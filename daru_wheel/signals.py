from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import OutCome, Analytic  # , WheelSpin, Stake
from channels.layers import get_channel_layer

# from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

# from time import sleep


@receiver(post_save, sender=OutCome)
def on_results_save(sender, instance, **kwargs):
    if instance.market is not None:
        pointer_val = instance.pointer  # fix id
        market_id = instance.market_id

        try:
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                "daru_spin", {"type": "spin_pointer", "pointer": pointer_val,}
            )

            async_to_sync(channel_layer.group_send)(
                "daru_spin", {"type": "market_info", "market": market_id,}
            )
        except Exception as ce:
            print(f"Channel error:{ce}")  # debug
            pass  # issues with channel shouldn't inter normal business from being done

        try:
            try:  # need test
                cum, created = Analytic.objects.update_or_create(id=1)
                if created:
                    pass
            except Exception as ce:
                print("CUMsinal", ce)
                pass

        except Exception as re:
            print(f"REESignal error:{re}")  # debug
            pass  # results later/manual by admin incase
    else:
        pass

