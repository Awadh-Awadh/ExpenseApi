from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(body=data['email_body'], subject=data['subject'], to=[data['to_email']])
        email.send()
