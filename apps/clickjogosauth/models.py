from calendar import timegm
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import jwt


class User(AbstractUser):
    clickjogos_id = models.CharField(blank=True, db_index=True, max_length=64)
    birthday = models.DateField(null=True)

    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=1)

    def create_jwt(self):
        return jwt.encode({
            'exp': timegm((now() + relativedelta(hours=2)).utctimetuple()),
            'uid': self.clickjogos_id,
            'provider': 'clickjogos',
            'info': {
                'nickname': self.username,
                'email': self.email,
                'gender': self.gender,
                'birthdate': self.birthday.strftime("%Y-%m-%d") if self.birthday else None,
            }
        }, settings.CLICKJOGOS_SECRET)
