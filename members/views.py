from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Member
from .models import Expenses
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ClubEvents
from .models import EventSubscribe

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
  
def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))
  
def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  return HttpResponse(template.render())

def template2(request):  
  template = loader.get_template('template2.html')
  return HttpResponse(template.render())

def gallery(request):
  template = loader.get_template('gallery.html')
  return HttpResponse(template.render())
  
def club_events(request):
  myevents = ClubEvents.objects.all().values()
  template = loader.get_template('club_events.html')
  context = {
    'myevents': myevents,
  }
  return HttpResponse(template.render(context, request))

def club_treasury(request):
  mymembers = Member.objects.all().values()
  myexpenses = Expenses.objects.all().values()
  sum_fees = sum([x['member_fees'] for x in mymembers])
  sum_expenses = sum([x['amount'] for x in myexpenses])
  cash_balance = sum_fees - sum_expenses
  template = loader.get_template('club_treasury.html')
  context = {
    'mymembers': mymembers,
    'sum_fees': sum_fees,
    'myexpenses': myexpenses,
    'sum_expenses': sum_expenses,
    'cash_balance': cash_balance,
  }
  return HttpResponse(template.render(context, request))


def event_subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        event = request.POST.get('event', None)

        if not name or not email:
            messages.error(request, "You must type name and/or email to subscribe to an Event")
            return redirect("/")

        subscribe_user = EventSubscribe.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = EventSubscribe()
        subscribe_model_instance.name = name
        subscribe_model_instance.email = email
        subscribe_model_instance.event = event

        subscribe_model_instance.save()
        messages.success(request, f'{email} member was successfully subscribed to event!')
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
#@user_is_superuser
def newsletter(request):
    return redirect('/')