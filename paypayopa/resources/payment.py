from .base import Resource
from ..constants.url import URL
from ..constants.api_list import API_NAMES
import datetime

from paypayopa.objects.payment import PaymentBody, PaymentAPIResponse
from paypayopa.objects.payment_auth import RevertPaymentAuthAPIResponse, RevertPaymentAuthBody
from paypayopa.objects.refund import RefundAPIResponse


class Payment(Resource):
    def __init__(self, client=None):
        super(Payment, self).__init__(client)
        self.base_url = URL.PAYMENT

    def create(self, data: dict, **kwargs) -> PaymentAPIResponse:
        url = self.base_url
        if "requestedAt" not in data:
            data['requestedAt'] = int(datetime.datetime.now().timestamp())
        if "merchantPaymentId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for merchantPaymentId")
        if "amount" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for amount")
        if not isinstance(data["amount"]["amount"], int):
            raise ValueError("\x1b[31m Amount should be of type integer"
                             " \x1b[0m")
        if "currency" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for currency")
        raw_response = self.post_url(url, data, api_id=API_NAMES.CREATE_PAYMENT, **kwargs)
        payment: PaymentBody = PaymentBody.from_json(raw_response["data"])
        return PaymentAPIResponse(result_info=raw_response["resultInfo"], data=payment)

    def get_payment_details(self, merchant_payment_id: str, **kwargs) -> PaymentAPIResponse:
        url = "{}/{}".format(self.base_url, merchant_payment_id)
        if merchant_payment_id is None:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        raw_response = self.fetch(None, url, None, api_id=API_NAMES.GET_PAYMENT, **kwargs)
        payment: PaymentBody = PaymentBody.from_json(raw_response["data"])
        return PaymentAPIResponse(result_info=raw_response["resultInfo"], data=payment)

    def cancel_payment(self, merchant_payment_id: str, **kwargs) -> PaymentAPIResponse:
        url = "{}/{}".format(self.base_url, merchant_payment_id)
        if merchant_payment_id is None:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        raw_response = self.delete(None, url, None, api_id=API_NAMES.CANCEL_PAYMENT, **kwargs)
        return PaymentAPIResponse(result_info=raw_response["resultInfo"], data=None)

    def refund_payment(self, data: dict, **kwargs) -> RefundAPIResponse:
        return self.client.Pending.refund_payment(data, **kwargs)

    def refund_details(self, merchant_refund_id: str, **kwargs) -> RefundAPIResponse:
        return self.client.Pending.refund_details(merchant_refund_id, **kwargs)

    # todo: implement PaymentAuthorization Object
    # docs: https://www.paypay.ne.jp/opa/doc/v1.0/preauth_capture#tag/Payment/operation/capturePaymentAuth
    def capture_payment(self, data=None, **kwargs):
        if data is None:
            data = {}
        url = "{}/{}".format('/v2/payments', 'capture')
        if "requestedAt" not in data:
            data['requestedAt'] = int(datetime.datetime.now().timestamp())
        if "merchantPaymentId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        if "merchantCaptureId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        if "orderDescription" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for merchantPaymentId")
        if "amount" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for amount")
        if type(data["amount"]["amount"]) != int:
            raise ValueError("\x1b[31m Amount should be of type integer"
                             " \x1b[0m")
        if "currency" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for currency")
        return self.post_url(url, data, api_id=API_NAMES.CAPTURE_PAYMENT, **kwargs)

    # todo: based on the document. not checked yet.
    def create_continuous_payment(self, data: dict, **kwargs) -> PaymentAPIResponse:
        url = "{}/{}".format('/v1/subscription', 'payments')
        if "requestedAt" not in data:
            data['requestedAt'] = int(datetime.datetime.now().timestamp())
        if "merchantPaymentId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        if "userAuthorizationId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for userAuthorizationId")
        if "amount" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for amount")
        if not isinstance(data["amount"]["amount"], int):
            raise ValueError("\x1b[31m Amount should be of type integer"
                             " \x1b[0m")
        if "currency" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for currency")
        raw_response = self.post_url(url, data, api_id=API_NAMES.CREATE_CONTINUOUS_PAYMENT, **kwargs)
        payment: PaymentBody = PaymentBody.from_json(raw_response["data"])
        return PaymentAPIResponse(result_info=raw_response["resultInfo"], data=payment)

    # todo: based on the document. not checked yet.
    def revert_payment(self, data=None, **kwargs) -> RevertPaymentAuthAPIResponse:
        if data is None:
            data = {}
        url = "{}/{}/{}".format('/v2/payments', 'preauthorize', 'revert')
        if "requestedAt" not in data:
            data['requestedAt'] = int(datetime.datetime.now().timestamp())
        if "merchantRevertId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        if "paymentId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        raw_response = self.post_url(url, data, api_id=API_NAMES.REVERT_AUTHORIZE, **kwargs)
        revert: RevertPaymentAuthBody = RevertPaymentAuthBody.from_json(raw_response["data"])
        return RevertPaymentAuthAPIResponse(result_info=raw_response["resultInfo"], data=revert)
