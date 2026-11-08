"""CLI for dynamic-budget-rebalancer."""
import sys
import argparse
from .rebalancer import DynamicBudgetRebalancer


def main():
    parser = argparse.ArgumentParser(description="Dynamic Budget Rebalancer CLI")
    parser.add_argument("--demo", action="store_true", help="Run budget rebalancer demo")
    args = parser.parse_args()

    if args.demo:
        rebalancer = DynamicBudgetRebalancer({
            "planning": 4000,
            "execution": 6000,
            "verification": 2000
        })
        rebalancer.consume("planning", 1500)
        print(f"[*] Planning used 1500 tokens. Rebalancing surplus to execution...")
        rebalancer.shift_surplus("planning", "execution")

        summary = rebalancer.get_summary()
        for p, s in summary.items():
            print(f"    - Phase {p}: Allocated={s['allocated']}, Used={s['used']}, Remaining={s['remaining']}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
