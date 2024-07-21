import datetime

from paypayopa.objects.payment import PaymentAPIResponse, PaymentBody
from paypayopa.objects.pending_payment import CreatedPendingPaymentBody, CreatedPendingPaymentAPIResponse
from paypayopa.objects.refund import RefundBody, RefundAPIResponse
from .base import Resource
from ..constants.api_list import API_NAMES
from ..constants.url import URL


class Pending(Resource):
    def __init__(self, client=None):
        super(Pending, self).__init__(client)
        self.base_url = URL.PENDING_PAYMENT

    def create_pending_payment(self, data: dict, **kwargs) -> CreatedPendingPaymentAPIResponse:
        url = self.base_url
        if "requestedAt" not in data:
            data['requestedAt'] = int(datetime.datetime.now().timestamp())
        if "merchantPaymentId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for merchantPaymentId")
        if "userAuthorizationId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for userAuthorizationId")
        if "amount" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for amount")
        if not isinstance(data["amount"]["amount"], int):
            raise ValueError("\x1b[31m Amount should be of type integer"
                             " \x1b[0m")
        if "currency" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for currency")
        raw_response = self.post_url(url, data, api_id=API_NAMES.CREATE_REQUEST_ORDER, **kwargs)
        pending_payment = CreatedPendingPaymentBody.from_json(raw_response["data"])
        return CreatedPendingPaymentAPIResponse(result_info=raw_response["resultInfo"], data=pending_payment)

    def get_payment_details(self, merchant_payment_id: str, **kwargs) -> PaymentAPIResponse:
        url = "{}/{}".format(self.base_url, merchant_payment_id)
        if merchant_payment_id is None:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        raw_response = self.fetch(None, url, None, api_id=API_NAMES.GET_REQUEST_ORDER, **kwargs)
        pending_payment = PaymentBody.from_json(raw_response["data"])
        return PaymentAPIResponse(result_info=raw_response["resultInfo"], data=pending_payment)

    def cancel_payment(self, merchant_payment_id: str, **kwargs) -> PaymentAPIResponse:
        url = "{}/{}".format(self.base_url, merchant_payment_id)
        if merchant_payment_id is None:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantPaymentId")
        raw_response = self.delete(None, url, None, api_id=API_NAMES.CANCEL_REQUEST_ORDER, **kwargs)
        return PaymentAPIResponse(result_info=raw_response["resultInfo"], data=None)

    def refund_payment(self, data: dict, **kwargs) -> RefundAPIResponse:
        url = "{}".format(URL.REFUNDS)
        if "merchantRefundId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for merchantRefundId")
        if "requestedAt" not in data:
            data['requestedAt'] = int(datetime.datetime.now().timestamp())
        if "paymentId" not in data:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for paymentId")
        if "amount" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS "
                             "\x1b[0m for amount")
        if not isinstance(data["amount"]["amount"], int):
            raise ValueError("\x1b[31m Amount should be of type integer"
                             " \x1b[0m")
        if "currency" not in data["amount"]:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for currency")
        raw_response = self.post_url(url, data,  api_id=API_NAMES.REFUND_REQUEST_ORDER, **kwargs)
        refund: RefundBody = RefundBody.from_json(raw_response["data"])
        return RefundAPIResponse(result_info=raw_response["resultInfo"], data=refund)

    def refund_details(self, merchant_refund_id: str, **kwargs) -> RefundAPIResponse:
        if merchant_refund_id is None:
            raise ValueError("\x1b[31m MISSING REQUEST PARAMS"
                             " \x1b[0m for merchantRefundId")
        url = "{}/{}".format('/v2/refunds', merchant_refund_id)
        raw_response = self.fetch(None, url, None, api_id=API_NAMES.GET_REFUND, **kwargs)
        refund: RefundBody = RefundBody.from_json(raw_response["data"])
        return RefundAPIResponse(result_info=raw_response["resultInfo"], data=refund)
