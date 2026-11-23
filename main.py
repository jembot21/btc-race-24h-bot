"""Retry buying CBBTC until held, exit on a 5% trailing stop, then stay in cash."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars


strategy = {"bought": False, "sold": False, "peak_close": None}


def on_batch(state, batch):
    position = state.positions.get("CBBTC")
    held = position is not None and position.qty > 0
    if held:
        strategy["bought"] = True
    entering = (
        not state.warming_up
        and not held
        and not strategy["bought"]
        and not strategy["sold"]
    )
    # Include the entry batch, but exclude all history before the buy is sent.
    if entering or strategy["bought"]:
        for bar in batch["bars"]:
            if bar["symbol"] == "CBBTC":
                close = int(bar["c"])
                peak = strategy["peak_close"]
                strategy["peak_close"] = close if peak is None else max(peak, close)

    if strategy["sold"] or state.warming_up:
        return []

    if entering:
        return [{
            "side": "buy",
            "symbol": "CBBTC",
            "notional_quote_units": state.cash * 995 // 1000,
            "max_slippage_bps": 100,
        }]

    close = state.close("CBBTC")
    peak = strategy["peak_close"]
    if held and close is not None and peak is not None and close * 100 <= peak * 95:
        strategy["sold"] = True
        return [{
            "side": "sell",
            "symbol": "CBBTC",
            "qty": position.qty,
            "max_slippage_bps": 100,
        }]

    return []


if __name__ == "__main__":
    makefun_bars.run(on_batch)
