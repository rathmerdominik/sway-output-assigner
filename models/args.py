from typing import List, Optional
from pydantic import BaseModel


class Args(BaseModel):
    monitor: Optional[List[str]]
    get_outputs: Optional[bool]
    bind: Optional[bool]
    move: Optional[bool]
    select: Optional[bool]
