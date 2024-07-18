from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from paypayopa.objects.base import BaseObj, BaseAPIResponse, Amount


@dataclass_json
@dataclass
class RefundBody(BaseObj):
    merchant_payment_id: str = field(metadata=config(field_name="merchantPaymentId"))
    amount: Amount
    reason: str


@dataclass
class RefundAPIResponse(BaseAPIResponse):
    data: RefundBody | None
