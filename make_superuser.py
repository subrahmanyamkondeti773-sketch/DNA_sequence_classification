import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dna_classification_project.settings')

import django
django.setup()

from django.contrib.auth.models import User

# Try to find the user
try:
    u = User.objects.get(username='Kondetipavan@123')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f"✅ Promoted '{u.username}' to superuser/staff successfully!")
except User.DoesNotExist:
    print("User 'Kondetipavan@123' not found. Listing all users:")
    for user in User.objects.all():
        print(f"  - {user.username} (staff={user.is_staff}, super={user.is_superuser})")
