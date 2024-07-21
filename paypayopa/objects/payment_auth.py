from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from dataclasses_json import dataclass_json, config

from paypayopa.objects.base import BaseObj, BaseAPIResponse, Amount, OrderItem
from paypayopa.objects.payment import PaymentMethod


@dataclass_json
@dataclass
class RevertPaymentAuthBody(BaseObj):
    reason: str


@dataclass
class RevertPaymentAuthAPIResponse(BaseAPIResponse):
    data: RevertPaymentAuthBody | None


@dataclass_json
@dataclass
class _Refund:
    status: str
    accepted_at: int = field(metadata=config(field_name="acceptedAt"))
    merchant_refund_id: str = field(metadata=config(field_name="merchantRefundId"))
    payment_id: str = field(metadata=config(field_name="paymentId"))
    amount: Amount
    requested_at: int = field(metadata=config(field_name="requestedAt"))
    reason: str


@dataclass_json
@dataclass
class Capture:
    accepted_at: int = field(metadata=config(field_name="acceptedAt"))
    merchant_capture_id: str = field(metadata=config(field_name="merchantCaptureId"))
    amount: Amount
    order_description: str = field(metadata=config(field_name="orderDescription"))
    requested_at: int = field(metadata=config(field_name="requestedAt"))
    expires_at: int = field(metadata=config(field_name="expiresAt"))
    status: str


@dataclass_json
@dataclass
class Revert:
    accepted_at: int = field(metadata=config(field_name="acceptedAt"))
    merchant_revert_id: str = field(metadata=config(field_name="merchantRevertId"))
    requested_at: int = field(metadata=config(field_name="requestedAt"))
    reason: str


def deserialize_refunds(data: Dict[str, Any]) -> List[_Refund]:
    # noinspection PyUnresolvedReferences
    return [_Refund.from_dict(refund) for refund in data.get('data', [])]


def deserialize_captures(data: Dict[str, Any]) -> List[Capture]:
    # noinspection PyUnresolvedReferences
    return [Capture.from_dict(capture) for capture in data.get('data', [])]


@dataclass_json
@dataclass
class PaymentAuthBody(BaseObj):
    merchant_payment_id: str = field(metadata=config(field_name="merchantPaymentId"))
    user_authorization_id: str = field(metadata=config(field_name="userAuthorizationId"))
    amount: Amount
    order_description: str = field(metadata=config(field_name="orderDescription"))
    order_items: List[OrderItem] = field(metadata=config(field_name="orderItems"))
    payment_methods: List[PaymentMethod] = field(metadata=config(field_name="paymentMethods"))
    expires_at: int = field(metadata=config(field_name="expiresAt"))
    store_id: Optional[str] = field(default=None, metadata=config(field_name="storeId"))
    terminal_id: Optional[str] = field(default=None, metadata=config(field_name="terminalId"))
    order_receipt_number: Optional[str] = field(default=None, metadata=config(field_name="orderReceiptNumber"))
    metadata: Optional[Dict[str, Any]] = None
    # noinspection PyUnresolvedReferences
    refunds: List[_Refund] = field(default_factory=list, metadata=config(decoder=deserialize_refunds))
    #  noinspection PyUnresolvedReferences
    captures: List[Capture] = field(default_factory=list, metadata=config(decoder=deserialize_captures))
    revert: Optional[Revert] = None


@dataclass
class PaymentAuthAPIResponse(BaseAPIResponse):
    data: PaymentAuthBody | None
