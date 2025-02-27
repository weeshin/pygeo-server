from typing import Type
from attrs import define
from rio_tiler.io import BaseReader, Reader

@define(kw_only=True)
class TilerFactory:

    reader: Type[BaseReader] = Reader
