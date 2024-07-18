from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from dataclasses_json import dataclass_json, config


@dataclass
class APIResponse:
    status: dict
    data: dict


@dataclass_json
@dataclass
class BaseObj:
    status: str
    accepted_at: int = field(metadata=config(field_name="acceptedAt"))
    requested_at: int = field(metadata=config(field_name="requestedAt"))


@dataclass_json
@dataclass
class Amount:
    amount: int
    currency: str


@dataclass_json
@dataclass
class Refund(BaseObj):
    merchant_refund_id: str = field(metadata=config(field_name="merchantRefundId"))
    payment_id: str = field(metadata=config(field_name="paymentId"))
    amount: Amount
    reason: str


@dataclass_json
@dataclass
class Refunds:
    data: List[Refund]


@dataclass_json
@dataclass
class OrderItem:
    name: str
    category: str
    quantity: int
    product_id: str = field(metadata=config(field_name="productId"))
    unit_price: Amount = field(metadata=config(field_name="unitPrice"))


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
class Payment(BaseObj):
    payment_id: str = field(metadata=config(field_name="paymentId"))
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
