from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from .models import Member
from .models import Expenses
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ClubEvents
from .models import EventSubscribe
from .models import ClubPicture 
import plotly.express as px

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
  mymembers = Member.objects.all().values()
  myexpenses = Expenses.objects.all().values()
  sum_fees = sum([x['member_fees'] for x in mymembers])
  sum_expenses = sum([x['amount'] for x in myexpenses])
  cash_balance = sum_fees - sum_expenses
  fig = px.bar(x=["incomes", "payments", "result"], y=[sum_fees, sum_expenses, cash_balance], labels={"x":"balance", "y":"EUR"}, title='Club treasury 2024')
  fig.update_layout(
    font_family="Courier New",
    font_color="blue",
    font_size=25,
    title_font_family="Times New Roman",
    title_font_color="red",
    title_font_size=35,
    title = {
      'y':0.9,
      'x':0.5,
      'xanchor': 'center',
      'yanchor': 'top'
      }
    
  )
  fig.write_html('template.html', auto_open=True)
  template = loader.get_template('template.html')
  context = {'fig':fig,}

  return HttpResponse(template.render(context, request))

def template2(request):  
  template = loader.get_template('template2.html')
  return HttpResponse(template.render())

def gallery(request):
  club_pictures = ClubPicture.objects.all() 
  template = loader.get_template('gallery.html')
  context = {
    'club_pictures': club_pictures,
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

def club_events(request):
  myevents = ClubEvents.objects.all().values()
  members_subscribed_for_event = EventSubscribe.objects.all().values()
  template = loader.get_template('club_events.html')
  if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        event = request.POST.get('event', None)
        
        event_sub = EventSubscribe(name=name, email=email, event=event)
        event_sub.save()

        context = {
          'myevents': myevents,
          'members_subscribed_for_event': members_subscribed_for_event,
        }

        return HttpResponse(template.render(context, request))
  else:
        context = {
          'myevents': myevents,
          'members_subscribed_for_event': members_subscribed_for_event,
        }
        return HttpResponse(template.render(context, request))
    






        
  
