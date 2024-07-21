from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from dataclasses_json import dataclass_json, config

from paypayopa.objects.base import BaseObj, BaseAPIResponse, Amount, OrderItem


@dataclass_json
@dataclass
class Refund(BaseObj):
    merchant_refund_id: str = field(metadata=config(field_name="merchantRefundId"))
    amount: Amount
    reason: str


@dataclass_json
@dataclass
class Refunds:
    data: List[Refund]


@dataclass_json
@dataclass
class PaymentMethod:
    amount: Amount
    type: str


def deserialize_refunds(refunds_data: Dict[str, Any]) -> List[Refund]:
    # noinspection PyUnresolvedReferences
    return [Refund.from_dict(refund) for refund in refunds_data.get('data', [])]


@dataclass_json
@dataclass
class PaymentBody(BaseObj):
    merchant_payment_id: str = field(metadata=config(field_name="merchantPaymentId"))
    user_authorization_id: str = field(metadata=config(field_name="userAuthorizationId"))
    amount: Amount
    order_description: str = field(metadata=config(field_name="orderDescription"))
    order_items: List[OrderItem] = field(metadata=config(field_name="orderItems"))
    payment_methods: List[PaymentMethod] = field(metadata=config(field_name="paymentMethods"))
    store_id: Optional[str] = field(default=None, metadata=config(field_name="storeId"))
    terminal_id: Optional[str] = field(default=None, metadata=config(field_name="terminalId"))
    order_receipt_number: Optional[str] = field(default=None, metadata=config(field_name="orderReceiptNumber"))
    metadata: Optional[Dict[str, Any]] = None
    refunds: List[Refund] = field(default_factory=list, metadata=config(decoder=deserialize_refunds))


@dataclass
class PaymentAPIResponse(BaseAPIResponse):
    data: PaymentBody | None
