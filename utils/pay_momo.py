import json
import requests
import uuid
import hmac
import hashlib
import codecs
from django.conf import settings
from api_files.models import ReceptionRecord


class MomoPayment:
    @classmethod
    def oder_info(cls, records=ReceptionRecord):
        order_info = "paywithMoMo"
        redirect_url = settings.REDIRECT_URL_MOMO
        ipn_url = settings.IPN_URL_MOMO
        amount = str(records.file.amount)
        order_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        request_type = "onDelivery"
        extra_data = ""
        raw_signature = "accessKey=" + settings.ACCESS_KEY_MOMO + "&amount=" + amount + "&extraData=" + extra_data + "&ipnUrl=" + ipn_url + "&orderId=" + order_id + "&orderInfo=" + order_info + "&partnerCode=" + settings.PARTNER_CODE_MOMO + "&redirectUrl=" + redirect_url + "&requestId=" + request_id + "&requestType=" + request_type
        signature = cls.signature_generator(raw_signature)
        data = {
            "partnerCode": settings.PARTNER_CODE_MOMO,
            "partnerName": "Test",
            "storeId": "epoch-making",
            "requestType": request_type,
            "ipnUrl": ipn_url,
            "redirectUrl": redirect_url,
            "orderId": order_id,
            "amount": amount,
            "lang": "vi",
            "orderInfo": order_info,
            "requestId": request_id,
            "extraData": extra_data,
            "signature": signature
        }
        records.order_id = order_id
        records.request_id = request_id
        records.save()
        return cls.create_payment(data)

    @classmethod
    def signature_generator(cls, raw_signature):
        return hmac.new(codecs.encode(settings.SECRETKEY_MOMO), codecs.encode(raw_signature),
                        hashlib.sha256).hexdigest()

    @classmethod
    def create_payment(cls, data):
        endpoint_create = "https://test-payment.momo.vn/v2/gateway/api/create"
        payload = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", endpoint_create, headers=headers, data=payload)
        return response.json()
