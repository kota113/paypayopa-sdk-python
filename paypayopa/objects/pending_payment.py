from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json, config

from paypayopa.objects.base import BaseAPIResponse, Amount, OrderItem


# todo: validate with the actual API response. implemented based on the API documentation
@dataclass_json
@dataclass
class CreatedPendingPaymentBody:
    requested_at: int = field(metadata=config(field_name="requestedAt"))
    merchant_payment_id: str = field(metadata=config(field_name="merchantPaymentId"))
    user_authorization_id: str = field(metadata=config(field_name="userAuthorizationId"))
    amount: Amount
    expires_at: int = field(metadata=config(field_name="expiryDate"))
    store_id: str = field(metadata=config(field_name="storeId"), default=None)
    terminal_id: str = field(metadata=config(field_name="terminalId"), default=None)
    order_receipt_number: str = field(metadata=config(field_name="orderReceiptNumber"), default=None)
    order_description: str = field(metadata=config(field_name="orderDescription"), default=None)
    order_items: List[OrderItem] = field(metadata=config(field_name="orderItems"), default=None)
    metadata: dict = field(metadata=config(field_name="metadata"), default=None)
    product_type: str = field(metadata=config(field_name="productType"), default=None)


@dataclass
class CreatedPendingPaymentAPIResponse(BaseAPIResponse):
    data: CreatedPendingPaymentBody | None
