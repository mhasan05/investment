from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(InvestmentPlan)
admin.site.register(Investment)
admin.site.register(Transaction)
admin.site.register(WithdrawalRequest)
admin.site.register(DepositRequest)
