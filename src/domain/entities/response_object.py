from dataclasses import dataclass, field
from typing import Literal

STATUS = Literal['success', 'error', 'other']


@dataclass
class ResponseObject:
    status: STATUS
    message: str = field(default_factory=str)
