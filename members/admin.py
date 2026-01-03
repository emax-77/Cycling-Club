from django.contrib import admin
from .models import Expenses, Member
from .models import ClubEvents, EventSubscribe
from .models import ClubPicture, Sponsor, Sponsorship

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "joined_date",)
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
