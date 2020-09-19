from django.contrib import admin
from .models import Profile, Ban, Advert, Following, Transaction, TransactionType

# Register your models here.
admin.site.register(Profile)
admin.site.register(Ban)
admin.site.register(Advert)
admin.site.register(Following)
admin.site.register(Transaction)
admin.site.register(TransactionType)