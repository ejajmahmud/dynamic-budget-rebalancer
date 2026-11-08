"""Core Dynamic Budget Rebalancer implementation."""
from typing import Dict, Any, Optional


class PhaseQuota:
    def __init__(self, phase_name: str, allocated: int):
        self.phase_name = phase_name
        self.allocated = allocated
        self.used = 0

    @property
    def remaining(self) -> int:
        return max(0, self.allocated - self.used)


class DynamicBudgetRebalancer:
    def __init__(self, initial_budgets: Dict[str, int]):
        self.phases: Dict[str, PhaseQuota] = {
            k: PhaseQuota(k, v) for k, v in initial_budgets.items()
        }

    def consume(self, phase_name: str, tokens: int) -> bool:
        if phase_name not in self.phases:
            return False
        pq = self.phases[phase_name]
        pq.used += tokens
        return pq.used <= pq.allocated

    def shift_surplus(self, from_phase: str, to_phase: str):
        if from_phase not in self.phases or to_phase not in self.phases:
            return
        src = self.phases[from_phase]
        dst = self.phases[to_phase]
        surplus = src.remaining
        if surplus > 0:
            src.allocated -= surplus
            dst.allocated += surplus

    def get_summary(self) -> Dict[str, Dict[str, int]]:
        return {
            k: {"allocated": v.allocated, "used": v.used, "remaining": v.remaining}
            for k, v in self.phases.items()
        }
