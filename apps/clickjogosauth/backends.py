import datetime
import requests

from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from .models import User

import logging
logger = logging.getLogger(__name__)


class ClickJogosBackend(ModelBackend):

    def authenticate(self, clickjogos_id=None, **kwargs):
        try:
            if not clickjogos_id:
                return None

            #get userdata from clickjogos
            url = "%s/user/%s/%s/%s" % (settings.CLICKJOGOS_URL, settings.CLICKJOGOS_KEY, settings.CLICKJOGOS_SECRET, clickjogos_id)
            userdata = requests.get(url).json()

            #if user is not authenticated with our app
            if "error" in userdata:
                logger.warn("Error in getting user data for clickjogos user %s, %s" % (clickjogos_id, userdata["error"]["message"]))
                return None

            info = userdata["info"]
            user = None
            try:
                user = User.objects.get(clickjogos_id=clickjogos_id)
            except User.DoesNotExist:
                pass

            if not user:
                try:
                    user = User.objects.get(username=info["nickname"])
                    user.clickjogos_id = clickjogos_id
                    user.save()
                except User.DoesNotExist:
                    pass

            if not user:
                try:
                    user = User.objects.get(email=info["email"])
                    user.clickjogos_id = clickjogos_id
                    user.save()
                except User.DoesNotExist:
                    pass

            if not user:
                user = User()
                user.clickjogos_id = clickjogos_id
                user.username = info["nickname"]
                user.email = info["email"]
                user.gender = info["gender"]
                year, month, day = info["birthdate"].split("-")
                user.birthday = datetime.date(int(year), int(month), int(day))
                user.save()

        except Exception:
            logger.exception("Unexpected error in authentication backend")
            raise

        return user