from django.http import HttpResponse
from django.template import loader
from .models import Member
from .models import Expenses
from .models import ClubEvents
from .models import EventSubscribe
from .models import ClubPicture 
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
import plotly.express as px
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required 

# home page (displayed first after login)  
def welcome(request):
  template = loader.get_template('welcome.html')
  return HttpResponse(template.render(request=request))

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


# contact page - to send email to club-admin
def contact(request):
    template = loader.get_template('contact.html')
    context = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        subject = f'Message from Cycling Club, user: {name}'
        message = f'{name} ({email}) wrote:\n\n{message_content}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['peter.wirth@gmail.com']

        try:
            # send email
            send_mail(subject, message, email_from, recipient_list)
            context['success_message'] = "Thank you! Your message has been sent successfully."
        except BadHeaderError:
            # handle email header errors
            context['error_message'] = "Invalid header found in the email."
        except Exception as e:
            # general error handling
            context['error_message'] = f"An error occurred while sending your message. Error: {str(e)}"

    return HttpResponse(template.render(context, request))


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

# club events page with event signup
def club_events(request):
    myevents = ClubEvents.objects.all().values()
    members_subscribed_for_event = EventSubscribe.objects.all().values()
    template = loader.get_template('club_events.html')

    # signing up for a club event, send confirmation email to user and print success message
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        event = request.POST.get('event')

        # save event subscription
        event_sub = EventSubscribe(name=name, email=email, event=event)
        event_sub.save()

        # create  user
        user = User.objects.create_user(username=name, email=email)
        
        # setup email
        subject = 'Welcome to Cycling Club'
        message = f'Hi {user.username}, thank you for registering for {event} event.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            # attempt to send email
            send_mail(subject, message, email_from, recipient_list)
            success_message = "Thank you! You are now registered for the event."
        except BadHeaderError:
            # handle email header errors
            success_message = "An error occurred: Invalid email header."
        except Exception as e:
            # general error handling
            success_message = f"An error occurred while sending the confirmation email. Error: {str(e)}"

        context = {
            'success_message': success_message,
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

    
# test page
def testing(request):
    template = loader.get_template('template.html')
    return HttpResponse(template.render(request=request))






        
  
