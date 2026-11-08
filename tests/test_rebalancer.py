"""Unit tests for dynamic-budget-rebalancer."""
import unittest
from dynamic_budget_rebalancer.rebalancer import DynamicBudgetRebalancer


class TestDynamicBudgetRebalancer(unittest.TestCase):
    def test_consume_and_shift(self):
        reb = DynamicBudgetRebalancer({"p1": 1000, "p2": 1000})
        reb.consume("p1", 400)
        self.assertEqual(reb.phases["p1"].remaining, 600)

        reb.shift_surplus("p1", "p2")
        self.assertEqual(reb.phases["p1"].remaining, 0)
        self.assertEqual(reb.phases["p2"].allocated, 1600)
