from django.http import HttpResponse
from django.template import loader
from .models import Member
from .models import Payment
from .models import Expenses
from .models import ClubEvents
from .models import EventSubscribe
from .models import ClubPicture 
from .models import Sponsorship
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, get_connection
from django.core.mail import EmailMessage
import logging
import re
import ssl
import smtplib
import datetime

logger = logging.getLogger(__name__)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import plotly.express as px
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone

# Home page 
def welcome(request):
  template = loader.get_template('welcome.html')
  return HttpResponse(template.render(request=request))

# List of all members
def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
  
# Member details
def details(request, id):
  mymember = Member.objects.get(id=id)
  total_paid = Payment.objects.filter(member=mymember, payment_type='membership').aggregate(Sum('amount'))['amount__sum'] or 0
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
    'total_paid': total_paid,
  }
  return HttpResponse(template.render(context, request))
  
#  Balance graph  / total, this year, last year
def balance_graph(request):
  year_now = datetime.datetime.now().year
  year_last = year_now - 1

  sum_fees_total = Payment.objects.filter(payment_type='membership').aggregate(Sum('amount'))['amount__sum'] or 0
  sum_sponsorship_total = (
    (Payment.objects.filter(payment_type='other').aggregate(Sum('amount'))['amount__sum'] or 0)
    + (Sponsorship.objects.aggregate(Sum('amount'))['amount__sum'] or 0)
  )
  sum_expenses_total = Expenses.objects.aggregate(Sum('amount'))['amount__sum'] or 0
  sum_income_total = sum_fees_total + sum_sponsorship_total
  cash_balance_total = sum_income_total - sum_expenses_total

  sum_fees_this_year = Payment.objects.filter(payment_type='membership', period_year=year_now).aggregate(Sum('amount'))['amount__sum'] or 0
  sum_sponsorship_this_year = (
    (Payment.objects.filter(payment_type='other', date_paid__year=year_now).aggregate(Sum('amount'))['amount__sum'] or 0)
    + (Sponsorship.objects.filter(date__year=year_now).aggregate(Sum('amount'))['amount__sum'] or 0)
  )
  sum_expenses_this_year = Expenses.objects.filter(payment_date__year=year_now).aggregate(Sum('amount'))['amount__sum'] or 0
  sum_income_this_year = sum_fees_this_year + sum_sponsorship_this_year
  cash_balance_this_year = sum_income_this_year - sum_expenses_this_year

  sum_fees_last_year = Payment.objects.filter(payment_type='membership', period_year=year_last).aggregate(Sum('amount'))['amount__sum'] or 0
  sum_sponsorship_last_year = (
    (Payment.objects.filter(payment_type='other', date_paid__year=year_last).aggregate(Sum('amount'))['amount__sum'] or 0)
    + (Sponsorship.objects.filter(date__year=year_last).aggregate(Sum('amount'))['amount__sum'] or 0)
  )
  sum_expenses_last_year = Expenses.objects.filter(payment_date__year=year_last).aggregate(Sum('amount'))['amount__sum'] or 0
  sum_income_last_year = sum_fees_last_year + sum_sponsorship_last_year
  cash_balance_last_year = sum_income_last_year - sum_expenses_last_year

  fig_total = px.bar(
    x=["incomes", "payments", "result"],
    y=[float(sum_income_total), float(sum_expenses_total), float(cash_balance_total)],
    labels={"x": "balance", "y": "EUR"},
    title='Club treasury TOTAL'
  )
  # Include Plotly.js only once (via CDN) to keep response size reasonable.
  graph_total = fig_total.to_html(
    full_html=False,
    include_plotlyjs='cdn',
    default_height=500,
    default_width=700,
  )

  fig_this_year = px.bar(
    x=["incomes", "payments", "result"],
    y=[float(sum_income_this_year), float(sum_expenses_this_year), float(cash_balance_this_year)],
    labels={"x": "balance", "y": "EUR"},
    title='Club treasury THIS YEAR'
  )
  graph_this_year = fig_this_year.to_html(
    full_html=False,
    include_plotlyjs=False,
    default_height=500,
    default_width=700,
  )

  fig_last_year = px.bar(
    x=["incomes", "payments", "result"],
    y=[float(sum_income_last_year), float(sum_expenses_last_year), float(cash_balance_last_year)],
    labels={"x": "balance", "y": "EUR"},
    title='Club treasury LAST YEAR'
  )
  graph_last_year = fig_last_year.to_html(
    full_html=False,
    include_plotlyjs=False,
    default_height=500,
    default_width=700,
  )

  template = loader.get_template('balance_graph.html')
  context = {
    'graph_total': graph_total,
    'graph_this_year': graph_this_year,
    'graph_last_year': graph_last_year,
    'year_now': year_now,
    'year_last': year_last,

    # totals
    'sum_fees_total': sum_fees_total,
    'sum_sponsorship_total': sum_sponsorship_total,
    'sum_expenses_total': sum_expenses_total,
    'cash_balance_total': cash_balance_total,

    # this year
    'sum_fees_this_year': sum_fees_this_year,
    'sum_sponsorship_this_year': sum_sponsorship_this_year,
    'sum_expenses_this_year': sum_expenses_this_year,
    'cash_balance_this_year': cash_balance_this_year,

    # last year
    'sum_fees_last_year': sum_fees_last_year,
    'sum_sponsorship_last_year': sum_sponsorship_last_year,
    'sum_expenses_last_year': sum_expenses_last_year,
    'cash_balance_last_year': cash_balance_last_year,
  }
  return HttpResponse(template.render(context, request))
  
# Contact page - to send email to club-admin
def contact(request):
  template = loader.get_template('contact.html')
  context = {}

  if request.method == 'POST':
    name = (request.POST.get('name') or '').strip()
    email = (request.POST.get('email') or '').strip()
    message_content = (request.POST.get('message') or '').strip()

    # prevent header injection (CR/LF) in name/email
    if any(ch in name for ch in ('\n', '\r')) or any(ch in email for ch in ('\n', '\r')):
      context['error_message'] = 'Invalid characters in name or email.'
      return HttpResponse(template.render(context, request))
    name = name.replace('\r', ' ').replace('\n', ' ')

    # validate email format
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
        "Secure connection failed: It was not possible to establish a secure TLS connection to the SMTP server (SSL certificate). "
        "This is often caused by a corporate proxy/antivirus inserting its own certificate. "
        "Check that EMAIL_USE_OS_TRUSTSTORE=1 and restart the server."
      )

    except smtplib.SMTPAuthenticationError:
      logger.exception('SMTPAuthenticationError when sending contact email')
      context['error_message'] = (
        "Gmail refused SMTP login. "
        "Use an 'App password' and save it in EMAIL_HOST_PASSWORD.")

    except smtplib.SMTPException:
      logger.exception('SMTPException when sending contact email')
      context['error_message'] = "An SMTP error occurred while sending the message. Please try again later."

    except Exception as e:
      logger.exception('Unexpected error when sending contact email')
      if getattr(settings, 'DEBUG', False):
        context['error_message'] = f"An error occurred while sending your message. Error: {str(e)}"
      else:
        context['error_message'] = "An error occurred while sending your message. Please try again later."

  return HttpResponse(template.render(context, request))

# Gallery 
def gallery(request):
  club_pictures = ClubPicture.objects.all() 
  template = loader.get_template('gallery.html')
  context = {
    'club_pictures': club_pictures,
  }
  return HttpResponse(template.render(context, request))

# Club treasury 
def club_treasury(request):
  year_now = datetime.datetime.now().year
  year_last = year_now - 1

  period = (request.GET.get('period') or 'all').strip().lower()
  if period not in {'all', 'this_year', 'last_year'}:
    period = 'all'

  membership = Payment.objects.filter(payment_type='membership')
  other_income = Payment.objects.filter(payment_type='other')
  sponsorship = Sponsorship.objects.all()
  expenses = Expenses.objects.all()

  if period == 'this_year':
    membership = membership.filter(period_year=year_now)
    other_income = other_income.filter(date_paid__year=year_now)
    sponsorship = sponsorship.filter(date__year=year_now)
    expenses = expenses.filter(payment_date__year=year_now)
    period_title = f"This year ({year_now})"
  elif period == 'last_year':
    membership = membership.filter(period_year=year_last)
    other_income = other_income.filter(date_paid__year=year_last)
    sponsorship = sponsorship.filter(date__year=year_last)
    expenses = expenses.filter(payment_date__year=year_last)
    period_title = f"Last year ({year_last})"
  else:
    period_title = "All years combined"

  sum_membership = membership.aggregate(Sum('amount'))['amount__sum'] or 0
  sum_sponsorship = (
    (other_income.aggregate(Sum('amount'))['amount__sum'] or 0)
    + (sponsorship.aggregate(Sum('amount'))['amount__sum'] or 0)
  )
  sum_income = sum_membership + sum_sponsorship
  sum_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
  cash_balance = sum_income - sum_expenses

  if period == 'this_year':
    members_qs = Member.objects.all().annotate(
      total_paid=Sum('payments__amount', filter=Q(payments__payment_type='membership', payments__period_year=year_now))
    )
  elif period == 'last_year':
    members_qs = Member.objects.all().annotate(
      total_paid=Sum('payments__amount', filter=Q(payments__payment_type='membership', payments__period_year=year_last))
    )
  else:
    members_qs = Member.objects.all().annotate(
      total_paid=Sum('payments__amount', filter=Q(payments__payment_type='membership'))
    )

  mymembers = []
  for m in members_qs:
    mymembers.append({
      'id': m.id,
      'firstname': m.firstname,
      'lastname': m.lastname,
      'total_paid': m.total_paid or 0,
    })

  mysponsorships = sponsorship.select_related('member').all()
  mysponsorships_model = sponsorship.select_related('sponsor').all()
  myexpenses = expenses.all().values()

  template = loader.get_template('club_treasury.html')
  context = {
    'period': period,
    'period_title': period_title,
    'year_now': year_now,
    'year_last': year_last,

    'sum_membership': sum_membership,
    'sum_sponsorship': sum_sponsorship,
    'sum_income': sum_income,
    'sum_expenses': sum_expenses,
    'cash_balance': cash_balance,

    'mymembers': mymembers,
    'mysponsorships': mysponsorships,
    'mysponsorships_model': mysponsorships_model,
    'myexpenses': myexpenses,
  }
  return HttpResponse(template.render(context, request))

# Club events page with event signup
@login_required
def club_events(request):
  template = loader.get_template('club_events.html')
  today = timezone.localdate()
  year_now = today.year

  # Show only upcoming events (today and future). Exclude events without a date.
  events_this_year = ClubEvents.objects.filter(
    event_date__isnull=False,
    event_date__gte=today,
  ).order_by('event_date', 'event_name')

  # Show registrations for upcoming events
  subscriptions_this_year = (
    EventSubscribe.objects.filter(event__event_date__isnull=False, event__event_date__gte=today)
    .select_related('member', 'event')
    .order_by('-subscribed_at')
  )

  # Find the Member for the logged-in user
  member = getattr(request.user, 'club_member', None)
  candidate_email = (request.user.email or request.user.username or '').strip()

  if member is None:
    member = Member.objects.filter(user=request.user).first()
  if member is None and candidate_email:
    member = Member.objects.filter(email__iexact=candidate_email).first()

  success_message = None
  error_message = None

  if request.method == 'POST':
    event_id = (request.POST.get('event_id') or '').strip()

    if not event_id:
      error_message = 'Please select an event.'
    elif member is None:
      if getattr(settings, 'DEBUG', False):
        error_message = (
          'No club member is linked to your account. '
          f"(DEBUG: username='{request.user.username}', email='{candidate_email or '—'}') "
          'Fix: link a Member via Member.user, or set Member.email to this email.'
        )
      else:
        error_message = 'No club member is linked to your account. Please contact the administrator.'
    else:
      # Only allow upcoming events
      try:
        event = ClubEvents.objects.get(id=event_id, event_date__isnull=False, event_date__gte=today)
      except ClubEvents.DoesNotExist:
        event = None
        error_message = 'The selected event does not exist.'

      if event is not None:
        email = (request.user.email or member.email or request.user.username or '').strip()
        if not email:
          error_message = 'No email address is set for your account. Please contact the administrator.'
        else:
          subscription, created = EventSubscribe.objects.get_or_create(
            email=email,
            event=event,
            defaults={'member': member},
          )

          if not created and subscription.member_id is None:
            subscription.member = member
            subscription.save(update_fields=['member'])

          event.event_members.add(member)

          # Send confirmation email
          subject = _sanitize_header('Event registration')
          safe_event_name = _sanitize_header(event.event_name)
          safe_member_name = _sanitize_header(f'{member.firstname} {member.lastname}'.strip())
          safe_date = _sanitize_header(str(event.event_date) if event.event_date else '')
          message = (
            f'Hi {safe_member_name},\n\n'
            f'you have successfully registered for the event: {safe_event_name}'
            f'{(" (" + safe_date + ")") if safe_date else ""}.\n\n'
            'Thank you and see you soon.\n'
            'Cycling Club'
          )
          email_from = _sanitize_header(str(settings.EMAIL_HOST_USER) if settings.EMAIL_HOST_USER is not None else '')
          recipient_list = [_sanitize_header(email)]

          try:
            validate_email(recipient_list[0])
          except DjangoValidationError:
            error_message = 'An error occurred: invalid recipient email.'
          else:
            try:
              email_msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)

              if getattr(settings, 'DEBUG', False):
                conn = get_connection('django.core.mail.backends.console.EmailBackend')
              else:
                conn = get_connection()

              sent_count = conn.send_messages([email_msg])
              if sent_count and sent_count > 0:
                success_message = 'Done! You are registered for the event.'
              else:
                success_message = 'Registration was saved, but the email could not be sent.'

            except BadHeaderError:
              logger.warning('BadHeaderError when sending club_events confirmation email.')
              success_message = 'Registration was saved, but the email could not be sent (invalid header).'

            except ssl.SSLError:
              logger.exception('SSL error when sending club_events confirmation email')
              success_message = (
                'Registration was saved, but a TLS connection to the SMTP server could not be established. '
                'Check EMAIL_USE_OS_TRUSTSTORE=1 and restart the server.'
              )

            except smtplib.SMTPAuthenticationError:
              logger.exception('SMTPAuthenticationError when sending club_events confirmation email')
              success_message = (
                'Registration was saved, but Gmail refused SMTP login. '
                "Use an 'App password' and save it in EMAIL_HOST_PASSWORD."
              )

            except smtplib.SMTPException:
              logger.exception('SMTPException when sending club_events confirmation email')
              success_message = 'Registration was saved, but an SMTP error occurred while sending the email.'

            except Exception:
              logger.exception('Unexpected error when sending club_events confirmation email')
              success_message = 'Registration was saved, but an error occurred while sending the email.'

    # refresh list after POST
    subscriptions_this_year = (
      EventSubscribe.objects.filter(event__event_date__isnull=False, event__event_date__gte=today)
      .select_related('member', 'event')
      .order_by('-subscribed_at')
    )

  context = {
    'success_message': success_message,
    'error_message': error_message,
    'events_this_year': events_this_year,
    'subscriptions_this_year': subscriptions_this_year,
    'year_now': year_now,
  }
  return HttpResponse(template.render(context, request))
  
 # Sanitize header values (remove CR/LF to prevent header injection)
def _sanitize_header(val):
  return re.sub(r'[\r\n]+', ' ', (val or '')).strip()



        
  
