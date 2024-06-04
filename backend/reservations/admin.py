from django.contrib import admin
from reservations.models import Request, AcceptedReservations, RejectedReservations 
from users.models import User


class ListD(admin.ModelAdmin):
    list_display = ('res_id','participant_id', 'activity_id','status')

    def res_id(self, obj):
        return obj.id
    res_id.short_description = 'RequestID'
    
admin.site.register(Request, ListD)
admin.site.register(AcceptedReservations)
admin.site.register(RejectedReservations)
