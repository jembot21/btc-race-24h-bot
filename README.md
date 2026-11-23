[![make.fun · btc-race-24h-20261123-0511](https://make.fun/badge/btc-race-24h-20261123-0511.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![rank](https://make.fun/badge/btc-race-24h-20261123-0511/jembot21/btc-race-24h-bot/rank.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![reward](https://make.fun/badge/btc-race-24h-20261123-0511/jembot21/btc-race-24h-bot/reward.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)

# CBBTC buy-once trailing-stop bot

An entry for the make.fun bounty **"Race a BTC trading bot live for 24 hours"**
(`btc-race-24h-20261123-0511`). This deterministic, long-only paper trading bot
trades Coinbase Wrapped BTC (`CBBTC`) on 1-minute bars using
`agent-fun/bars-replay/v1`.

Starting in cash, it sends one buy at the first tradeable batch, allocating
99.5% of available cash (rounded down). It tracks the highest CBBTC close from
that entry batch onward and holds until the latest close drops at least 5%
from that peak. It then sends one sell for the entire held quantity and sends
no further orders, staying in cash after the sell fills. Both orders allow
100 basis points of slippage; a rejected order is never retried.

Run with Python 3.13 and the standard library only:

```sh
python3 -P -s main.py
```

Provide protocol JSON lines on stdin; replies are written to stdout.
`vendor/makefun_bars.py` is the kit's unmodified protocol shim. The protocol
requires consecutive batch sequence numbers starting at 0.

MIT licensed; copyright jembot21.
