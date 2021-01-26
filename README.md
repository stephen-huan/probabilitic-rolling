# Probabilistic Rolling

A probability theory model for [Mudae](https://top.gg/bot/432610292342587392)
rolling on Discord.
Optimizations include integer linear programming techniques and
dynamic programming on the expected value of a random variable.

Initial data collected by [Luke Thistlethwaite](https://github.com/lthistle)
and extended to character-level data by [Avik Rao](https://github.com/AvikRao).

See Luke's repository [here](https://github.com/lthistle/mudae-optimizer).

[White paper on optimization](https://github.com/stephen-huan/cs-lectures/blob/master/probability-theory/gacha-optimization/writeup.pdf)

### Installing and Running

To install dependencies, run:
```bash
pipenv install
```

Run the files in the top-level directory with:
```bash
python main.py
```

The files in the modules problib and disablelist need to be ran like this:
```bash
python -m problib.test_model
```

