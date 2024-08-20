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
from django.conf import settings
from django.core.mail import send_mail
import plotly.express as px
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required # decorator to ensure user is logged in

# list of all members page
def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
  
# member details page
def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))
  
# home page (displayed first after login)  
def welcome(request):
  template = loader.get_template('welcome.html')
  return HttpResponse(template.render(request=request))

# page with graph and balance
def balance_graph(request):
  mymembers = Member.objects.all().values()
  myexpenses = Expenses.objects.all().values()
  sum_fees = sum([x['member_fees'] for x in mymembers])
  sum_expenses = sum([x['amount'] for x in myexpenses])
  cash_balance = sum_fees - sum_expenses

  # create a bar graph
  fig = px.bar(x=["incomes", "payments", "result"], y=[sum_fees, sum_expenses, cash_balance], labels={"x":"balance", "y":"EUR"}, title='Club treasury 2024')
  graph = fig.to_html(full_html=False, default_height=500, default_width=700)

  template = loader.get_template('balance_graph.html')
  context = {'graph':graph,
             'sum_fees': sum_fees,
             'sum_expenses': sum_expenses,
             'cash_balance': cash_balance        
  } 
  return HttpResponse(template.render(context, request))

# test page
def testing(request):  
  template = loader.get_template('template.html')
  return HttpResponse(template.render(request=request))

# gallery page
def gallery(request):
  club_pictures = ClubPicture.objects.all() 
  template = loader.get_template('gallery.html')
  context = {
    'club_pictures': club_pictures,
  }
  return HttpResponse(template.render(context, request))

# club treasury page   
def club_treasury(request):
  mymembers = Member.objects.all().values()
  myexpenses = Expenses.objects.all().values()
  template = loader.get_template('club_treasury.html')
  context = {
    'mymembers': mymembers,
    'myexpenses': myexpenses
  }
  return HttpResponse(template.render(context, request))

# club events page with event sign up
def club_events(request):
  myevents = ClubEvents.objects.all().values()
  members_subscribed_for_event = EventSubscribe.objects.all().values()
  template = loader.get_template('club_events.html')
  
  # signing up for a club event and sending confirmation email to user
  if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        event = request.POST.get('event', None)
        event_sub = EventSubscribe(name=name, email=email, event=event)
        event_sub.save()

        user = User.objects.create_user(username=name, email=email)        
        subject = 'Welcome to Cycling Club'
        message = f'Hi {user.username}, thank you for registering for {event} event.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )


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
    






        
  
