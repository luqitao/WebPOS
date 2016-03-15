from django.core.management import BaseCommand

from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail('test',
                  'just a test',
                  'liangliu@fiberhome.com',
                  ['liuliang1982920@qq.com'], auth_user='liangliu',
                  auth_password='0210926861.fh', fail_silently=False)
