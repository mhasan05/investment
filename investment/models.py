# models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class InvestmentPlan(models.Model):
    """
    e.g. "Monthly", "6 months", "Yearly"
    duration_days: integer duration in days (30, 180, 365)
    rate_percent: profit percentage for the whole duration (not annualized) OR annualized depending on your choice
    is_compound: whether returns compound (True) or simple (False) - optional
    """
    name = models.CharField(max_length=50, unique=True)
    duration_days = models.PositiveIntegerField()
    rate_percent = models.DecimalField(max_digits=6, decimal_places=2)  # e.g. 5.00
    is_compound = models.BooleanField(default=False)
    min_amount = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Investment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.PROTECT)
    principal = models.DecimalField(max_digits=18, decimal_places=2)
    profit_amount = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    reinvest = models.BooleanField(default=False)  # whether user opted to auto-reinvest at settlement
    settled_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)  # optional for audit / details

    def __str__(self):
        return f"{self.user} - {self.plan.name} - {self.principal}"

    def is_expired(self):
        return timezone.now() >= self.end_date and self.status == 'active'
    


class Transaction(models.Model):
    TX_TYPES = [('credit','credit'), ('debit','debit')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tx_type = models.CharField(max_length=10, choices=TX_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    reference = models.CharField(max_length=128, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class WithdrawalRequest(models.Model):
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('paid','Paid')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    wallet_address = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)



class DepositRequest(models.Model):
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('paid','Paid')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

