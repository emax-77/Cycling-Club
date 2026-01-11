from django.contrib import admin
from .models import Expenses, Member
from .models import ClubEvents, EventSubscribe
from .models import ClubPicture, Sponsor, Sponsorship, Payment

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "email", "user", "joined_date",)
class ExpensesAdmin(admin.ModelAdmin):
  list_display = ('payment_date', 'event_name', 'purpose', 'amount',)
class ClubEventsAdmin(admin.ModelAdmin):
  list_display = ('event_name', 'event_date', 'members_count')
  def members_count(self, obj):
    return obj.event_members.count()
  members_count.short_description = 'Members'
class EventSubscribeAdmin(admin.ModelAdmin):
  list_display = ('email', 'event', 'subscribed_at')
class ClubPictureAdmin(admin.ModelAdmin):
  list_display = ('name', 'description')

  
admin.site.register(Member, MemberAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(EventSubscribe, EventSubscribeAdmin)
admin.site.register(ClubEvents, ClubEventsAdmin)
admin.site.register(ClubPicture, ClubPictureAdmin)
admin.site.register(Sponsor)
admin.site.register(Sponsorship)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('member', 'payment_type', 'period_year', 'event', 'amount', 'date_paid')
  list_filter = ('payment_type', 'period_year')
  search_fields = ('member__firstname', 'member__lastname', 'member__id')
