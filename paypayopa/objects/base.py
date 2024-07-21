from dataclasses import dataclass, field
from typing import Any

from dataclasses_json import dataclass_json, config


@dataclass
class BaseAPIResponse:
    result_info: dict
    data: Any


@dataclass_json
@dataclass
class BaseObj:
    status: str
    accepted_at: int = field(metadata=config(field_name="acceptedAt"))
    requested_at: int = field(metadata=config(field_name="requestedAt"))
    payment_id: str = field(metadata=config(field_name="paymentId"))


@dataclass_json
@dataclass
class Amount:
    amount: int
    currency: str


@dataclass_json
@dataclass
class OrderItem:
    name: str
    category: str
    quantity: int
    product_id: str = field(metadata=config(field_name="productId"))
    unit_price: Amount = field(metadata=config(field_name="unitPrice"))
