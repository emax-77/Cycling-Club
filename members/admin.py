from django.contrib import admin
from .models import Expenses, Member
from .models import ClubEvents, EventSubscribe
from .models import Product

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "joined_date",)
class ExpensesAdmin(admin.ModelAdmin):
  list_display = ('payment_date', 'event_name', 'purpose', 'amount',)
class ClubEventsAdmin(admin.ModelAdmin):
  list_display = ('event_name', 'event_date', 'event_members')
class EventSubscribeAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'event')
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')

  
admin.site.register(Member, MemberAdmin)
admin.site.register(Expenses, ExpensesAdmin)
#admin.site.register(CustomUser)
admin.site.register(EventSubscribe, EventSubscribeAdmin)
admin.site.register(ClubEvents, ClubEventsAdmin)
admin.site.register(Product, ProductAdmin)
