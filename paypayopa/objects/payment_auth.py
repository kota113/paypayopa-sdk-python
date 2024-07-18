from dataclasses import dataclass

from dataclasses_json import dataclass_json

from paypayopa.objects.base import BaseObj, BaseAPIResponse


@dataclass_json
@dataclass
class RevertPaymentAuthBody(BaseObj):
    reason: str


@dataclass
class RevertPaymentAuthAPIResponse(BaseAPIResponse):
    data: RevertPaymentAuthBody | None
