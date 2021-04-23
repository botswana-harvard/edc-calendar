from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, weak=False,
          dispatch_uid="create_or_update_calender_event_on_post_save")
def create_or_update_calender_event_on_post_save(sender, instance, raw,
                                     created, using, **kwargs):
    if not raw and not kwargs.get('update_fields'):
        try:
            instance.create_or_update_calender_event()
        except AttributeError as e:
            if 'create_or_update_calender_event' not in str(e):
                raise