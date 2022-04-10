from twilio.rest import Client
from django.conf import settings
import phonenumbers


class SendSms:
    @classmethod
    def convert_phone_number(cls, phone_number):
        try:
            _phone_number = phonenumbers.parse(phone_number, region="VN")
            phone_number = phonenumbers.format_number(
                _phone_number, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            return None
        return phone_number

    @classmethod
    def send_sms(cls, phone_number, body):
        try:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to=cls.convert_phone_number(phone_number),
                from_=settings.TWILIO_PHONE,
                body=body)
            return True
        except:
            return False
