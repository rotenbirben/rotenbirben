from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from juntagrico.config import Config
from juntagrico.forms import SubscriptionPartSelectForm
from django.utils.translation import gettext as _


class MySubscriptionPartSelectForm(SubscriptionPartSelectForm):
    def __init__(self, selected, *args, **kwargs):
        super().__init__(selected, *args, **kwargs)
        del self.helper.layout[-2]

    def _get_initial(self, subscription_type):
        if subscription_type in self.selected.keys():
            return self.selected[subscription_type]
        return 0

    def clean(self):
        selected = self.get_selected()
        # check that at least one subscription was selected
        if sum(selected.values()) == 0:
            amount_error_message = mark_safe(_('Wähle mindestens 1 {} aus.').format(
                Config.vocabulary('subscription')
            ))
            raise ValidationError(amount_error_message, code='amount_error')
        return super().clean()
