from django.contrib import admin
from .models import User
from .models import Userinformation
from .models import Data

# Register your models here.
@admin.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display=( 'id','name' ,'email','password','psw')



admin.site.register(Userinformation)


admin.site.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display=('id','exercise','amount')


