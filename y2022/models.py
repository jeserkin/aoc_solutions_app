from enum import Enum

from ninja import Schema


# Create your models here.
class Part(Enum):
    ONE = 1
    TWO = 2


class Solution(Schema):
    part: int
    result: int
