from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'paid_at', 'transaction_id')
    list_filter = ('paid_at',)
    search_fields = ('transaction_id', 'booking__user__email')
