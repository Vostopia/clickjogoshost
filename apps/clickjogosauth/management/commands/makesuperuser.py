from optparse import make_option
from django.core.management import BaseCommand, CommandError
from ... import models


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    )
    help = "Turns the given user (by username) into a superuser"
    args = '<username>'

    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = True

    def handle(self, username, *args, **options):
        try:
            user = models.User.objects.filter(username=username).get()
        except models.User.DoesNotExist:
            raise CommandError("User %s does not exist" % username)

        user.is_superuser = True
        user.is_staff = True
        user.save()
        print "User %s (%s) is promoted to superuser" % (username, user.id)