from django.shortcuts import redirect, render
from juntagrico.config import Config
from juntagrico.view_decorators import create_subscription_session

from rotenbirben.forms import MySubscriptionPartSelectForm


@create_subscription_session
def cs_select_subscription(request, cs_session):
    if request.method == 'POST':
        form = MySubscriptionPartSelectForm(cs_session.subscriptions, request.POST)
        if form.is_valid():
            cs_session.subscriptions = form.get_selected()
            return redirect(cs_session.next_page())
    else:
        form = MySubscriptionPartSelectForm(cs_session.subscriptions)

    render_dict = {
        'form': form,
        'subscription_selected': sum(form.get_selected().values()) > 0,
        'hours_used': Config.assignment_unit() == 'HOURS',
    }
    return render(request, 'createsubscription/select_subscription.html', render_dict)
