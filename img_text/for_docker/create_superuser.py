import os
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from mainimg.models import Price, UsersToDocs

User = get_user_model()

try:
    User.objects.create_superuser(
        username=os.getenv("DJANGO_SUPERUSER_USERNAME", "admin"),
        email=os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com"),
        password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
    )
    print("Superuser created successfully.")

except IntegrityError:
    print("Superuser already exists.")


Price(id=1, file_type='png', price=1).save()
Price(id=2, file_type='jpeg', price=2).save()
Price(id=3, file_type='gif', price=3).save()
Price(id=4, file_type='webp', price=4).save()
Price(id=5, file_type='bmp', price=5).save()
Price(id=6, file_type='tiff', price=6).save()
print("Price add!!!")

UsersToDocs(id=1, username="admin").save()
print('Add Userstodocs!!!')

