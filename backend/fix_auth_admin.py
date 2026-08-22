import re

with open('apps/core/admin.py', 'r') as f:
    content = f.read()

auth_unfold_code = """
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
"""

if 'class UserAdmin(' not in content:
    content += auth_unfold_code
    with open('apps/core/admin.py', 'w') as f:
        f.write(content)
    print("Added auth models to Unfold")
else:
    print("Already added")
