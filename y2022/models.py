from enum import Enum
from typing import Union

from ninja import Schema


# Create your models here.
class Part(Enum):
    ONE = 1
    TWO = 2


class Solution(Schema):
    part: int
    result: Union[int, str]
