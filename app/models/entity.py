from typing import List, Optional  
from dataclasses import dataclass, field
import uuid

# Candidate is a clear Entity
@dataclass(kw_only=True) # This kw_only to avoid the error "non-default argument follows default argument".
class Entity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
