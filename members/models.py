from django.db import models
from django.utils import timezone

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    joined_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    member_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsorships')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    purpose = models.CharField(max_length=255, null=True, blank=True)

class Expenses(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='expenses')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True, related_name='sponsor_expenses')
    payment_date = models.DateField(null=True, blank=True)
    event_name = models.CharField(max_length=255, null=True, blank=True)
    purpose = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ClubEvents(models.Model):
    event_name = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_members = models.ManyToManyField(Member, blank=True, related_name='events')
    event_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name or "Event"

class EventSubscribe(models.Model):
    member = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL, related_name='subscriptions')
    email = models.EmailField(max_length=100)
    event = models.ForeignKey(ClubEvents, on_delete=models.CASCADE, related_name='subscribers')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('email', 'event')

    def __str__(self):
        return f"{self.email} -> {self.event}"

class ClubPicture(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='gallery/')
    event = models.ForeignKey(ClubEvents, null=True, blank=True, on_delete=models.SET_NULL, related_name='pictures')
    uploaded_by = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL, related_name='uploaded_pictures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


