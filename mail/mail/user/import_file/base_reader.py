from abc import ABC
from typing import List


class BaseReader(ABC):

    def __init__(self, file: object):
        ...

    @property
    def items(self) -> List:
        ...
