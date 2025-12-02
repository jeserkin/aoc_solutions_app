from abc import abstractmethod
from enum import Enum
from typing import List
from typing import Union

from ninja import Schema
from ninja import UploadedFile


# Create your models here.
class Part(Enum):
    ONE = 1
    TWO = 2


class Solution(Schema):
    part: int
    result: Union[int, str]


class Resolver:
    @abstractmethod
    def resolve(self, problem_input: UploadedFile) -> List[Solution]:
        pass