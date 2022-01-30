from django.contrib import admin
from .models import (
    UserKey,
    PasswordResetEvent
)

admin.site.register(UserKey)
admin.site.register(PasswordResetEvent)