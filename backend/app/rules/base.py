from abc import ABC, abstractmethod
from typing import Optional, Any
from pydantic import BaseModel

# 1. Define the Standard Output for ANY Rule
class RuleResult(BaseModel):
    rule_name: str
    triggered: bool
    risk_score: float  # 0.0 to 100.0
    reason: Optional[str] = None

# 2. The Abstract Contract
class BaseRule(ABC):
    """
    All compliance rules must inherit from this class.
    This ensures the Rule Engine can run them blindly.
    """
    
    @property
    @abstractmethod
    def rule_name(self) -> str:
        pass

    @abstractmethod
    async def check(self, transaction: Any, customer_context: Any = None) -> RuleResult:
        """
        The core logic. 
        Input: Transaction data (and optional customer history).
        Output: RuleResult.
        """
        pass