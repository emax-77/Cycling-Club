from django.http import HttpResponse
from django.template import loader
from .models import Member
from .models import Payment
from .models import Expenses
from .models import ClubEvents
from .models import EventSubscribe
from .models import ClubPicture 
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, get_connection
from django.core.mail import EmailMessage
import logging
import re
import ssl
import smtplib

logger = logging.getLogger(__name__)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import plotly.express as px
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

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
  total_paid = Payment.objects.filter(member=mymember, payment_type='membership').aggregate(Sum('amount'))['amount__sum'] or 0
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
    'total_paid': total_paid,
  }
  return HttpResponse(template.render(context, request))
  
# page with graph and balance
def balance_graph(request):
  mymembers = Member.objects.all()
  myexpenses = Expenses.objects.all().values()
  sum_fees = Payment.objects.filter(payment_type='membership').aggregate(Sum('amount'))['amount__sum'] or 0
  sum_expenses = sum([x['amount'] for x in myexpenses])
  cash_balance = sum_fees - sum_expenses

  # create a bar graph
  fig = px.bar(x=["incomes", "payments", "result"], y=[sum_fees, sum_expenses, cash_balance], labels={"x":"balance", "y":"EUR"}, title='Club treasury')
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
    name = (request.POST.get('name') or '').strip()
    email = (request.POST.get('email') or '').strip()
    message_content = (request.POST.get('message') or '').strip()

    # Prevent header injection (CR/LF) in name/email
    if any(ch in name for ch in ('\n', '\r')) or any(ch in email for ch in ('\n', '\r')):
      context['error_message'] = 'Invalid characters in name or email.'
      return HttpResponse(template.render(context, request))
    name = name.replace('\r', ' ').replace('\n', ' ')

    # Validate email format
    try:
      validate_email(email)
    except DjangoValidationError:
      context['error_message'] = 'Please provide a valid email address.'
      return HttpResponse(template.render(context, request))

    subject = f'Message from Cycling Club, user: {name}'
    message = f'{name} ({email}) wrote:\n\n{message_content}'
    email_from = str(settings.EMAIL_HOST_USER) if settings.EMAIL_HOST_USER is not None else ''
   
    subject = _sanitize_header(subject)
    email_from = _sanitize_header(email_from)
    recipient_list = [_sanitize_header(r) for r in getattr(settings, 'CONTACT_RECIPIENT_LIST', [])]

    if not recipient_list:
      context['error_message'] = 'Contact recipient is not configured.'
      return HttpResponse(template.render(context, request))

    # validate recipient emails
    for r in recipient_list:
      try:
        validate_email(r)
      except DjangoValidationError:
        context['error_message'] = 'Invalid recipient email configured.'
        return HttpResponse(template.render(context, request))

    try:
      email_msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)

      debug_mode = getattr(settings, 'DEBUG', False)
      if debug_mode:
        # In DEBUG print the email to the console (no real SMTP).
        conn = get_connection('django.core.mail.backends.console.EmailBackend')
      else:
        # In production use the configured backend (SMTP via my_ebike.email_backend).
        conn = get_connection()

      sent_count = conn.send_messages([email_msg])
      if sent_count and sent_count > 0:
        context['success_message'] = "Thank you! Your message has been sent successfully."
      else:
        context['error_message'] = "Email was not sent. Please try again later."

    except BadHeaderError:
      logger.warning('BadHeaderError when sending contact email (subject/from/to sanitized).')
      context['error_message'] = "Invalid header found in the email. Please check header values (no newlines)."

    except ssl.SSLError:
      logger.exception('SSL error when sending contact email')
      context['error_message'] = (
        "Nepodarilo sa nadviazať zabezpečené TLS spojenie so SMTP serverom (SSL certifikát). "
        "Často to spôsobí firemný proxy/antivírus, ktorý vkladá vlastný certifikát. "
        "Skontroluj, že EMAIL_USE_OS_TRUSTSTORE=1 a reštartuj server."
      )

    except smtplib.SMTPAuthenticationError:
      logger.exception('SMTPAuthenticationError when sending contact email')
      context['error_message'] = (
        "Gmail odmietol prihlásenie do SMTP. "
        "Použi 'App password' a ulož ho do EMAIL_HOST_PASSWORD.")

    except smtplib.SMTPException:
      logger.exception('SMTPException when sending contact email')
      context['error_message'] = "Nastala SMTP chyba pri odosielaní správy. Skús to prosím neskôr."

    except Exception as e:
      logger.exception('Unexpected error when sending contact email')
      if getattr(settings, 'DEBUG', False):
        context['error_message'] = f"An error occurred while sending your message. Error: {str(e)}"
      else:
        context['error_message'] = "Nastala chyba pri odosielaní správy. Skús to prosím neskôr."

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
  members = Member.objects.all()
  mymembers = []
  for m in members:
      total = Payment.objects.filter(member=m, payment_type='membership').aggregate(Sum('amount'))['amount__sum'] or 0
      mymembers.append({'id': m.id, 'firstname': m.firstname, 'lastname': m.lastname, 'total_paid': total})

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

        event_sub = EventSubscribe(name=name, email=email, event=event)
        event_sub.save()

        user = User.objects.create_user(username=name, email=email)
        
        subject = _sanitize_header('Welcome to Cycling Club')
        safe_username = _sanitize_header(user.username)
        safe_event = _sanitize_header(event)
        message = f'Hi {safe_username}, thank you for registering for {safe_event} event.'
        email_from = _sanitize_header(str(settings.EMAIL_HOST_USER) if settings.EMAIL_HOST_USER is not None else '')
        recipient_list = [_sanitize_header(user.email)]

        # Validate recipient email
        try:
          validate_email(recipient_list[0])
        except DjangoValidationError:
          success_message = "An error occurred: invalid recipient email."
          context = {
              'success_message': success_message,
              'myevents': myevents,
              'members_subscribed_for_event': members_subscribed_for_event,
          }
          return HttpResponse(template.render(context, request))

        try:
          email_msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)

          if getattr(settings, 'DEBUG', False):
            conn = get_connection('django.core.mail.backends.console.EmailBackend')
          else:
            conn = get_connection()

          sent_count = conn.send_messages([email_msg])
          if sent_count and sent_count > 0:
            success_message = "Thank you! You are now registered for the event."
          else:
            success_message = "Email was not sent. Please try again later."

        except BadHeaderError:
          logger.warning('BadHeaderError when sending club_events confirmation email.')
          success_message = "An error occurred: Invalid email header."

        except ssl.SSLError:
          logger.exception('SSL error when sending club_events confirmation email')
          success_message = (
            "Nepodarilo sa nadviazať zabezpečené TLS spojenie so SMTP serverom (SSL certifikát). "
            "Skontroluj, že EMAIL_USE_OS_TRUSTSTORE=1 a reštartuj server."
          )

        except smtplib.SMTPAuthenticationError:
          logger.exception('SMTPAuthenticationError when sending club_events confirmation email')
          success_message = (
            "Gmail odmietol prihlásenie do SMTP. "
            "Použi 'App password' a ulož ho do EMAIL_HOST_PASSWORD."
          )

        except smtplib.SMTPException:
          logger.exception('SMTPException when sending club_events confirmation email')
          success_message = "Nastala SMTP chyba pri odosielaní emailu. Skús to prosím neskôr."

        except Exception as e:
          logger.exception('Unexpected error when sending club_events confirmation email')
          if getattr(settings, 'DEBUG', False):
            success_message = f"An error occurred while sending the confirmation email. Error: {str(e)}"
          else:
            success_message = "Nastala chyba pri odosielaní potvrdzujúceho emailu. Skús to prosím neskôr."

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

 # sanitize header values to prevent header injection (remove CR/LF)
def _sanitize_header(val):
  return re.sub(r'[\r\n]+', ' ', (val or '')).strip()



        
  
