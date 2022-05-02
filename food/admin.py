from django.contrib import admin
from .models import Donation, Claim, NGOExtra, DonarExtra, Notice
# Register your models here. (by sumit.luv)
class NGOExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(NGOExtra, NGOExtraAdmin)

class DonarExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(DonarExtra, DonarExtraAdmin)

class DonationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Donation, DonationAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)

class ClaimAdmin(admin.ModelAdmin):
    pass
admin.site.register(Claim, ClaimAdmin)
