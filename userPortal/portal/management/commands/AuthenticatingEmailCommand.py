from django.core.management import BaseCommand, CommandError
from portal.models import AuthenticateEmailTask, AuthenticateEmail, PortalUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        non_send_emails = AuthenticateEmailTask.objects.select_related().filter(
            status=AuthenticateEmailTask.EMAIL_STATUS_WAIT)
        email_need_send = [(email.authenticate_email.portal_user.email,
                            email.authenticate_email.authenticate_email_code)
                           for email in non_send_emails]
        self.send_authenticated_email(email_need_send)

    def send_authenticated_email(self, email_pair_list):
        for email, code in email_pair_list:
            print 'send [{code}] to email[{email}]' % {'code': code, 'email': email}
