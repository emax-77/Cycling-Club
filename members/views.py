from django.http import HttpResponse
from django.template import loader
from .models import Member

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
  sum_fees = sum([x['member_fees'] for x in mymembers])
  template = loader.get_template('template.html')
  context = {
    'mymembers': mymembers,
    'sum_fees': sum_fees,
  }
  return HttpResponse(template.render(context, request))
  
  
def member_fees_summary(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('member_fees_summary.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))