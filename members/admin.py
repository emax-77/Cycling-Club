from django.contrib import admin
from .models import Expenses, Member

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "joined_date",)
class ExpensesAdmin(admin.ModelAdmin):
  list_display = ('payment_date', 'event_name', 'purpose', 'amount',)
  
admin.site.register(Member, MemberAdmin)
admin.site.register(Expenses, ExpensesAdmin)