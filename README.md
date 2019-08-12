# pystockbalance
You have stock in your portfolio which changes value over time. Maybe you have
a ratio of values that you want to keep between these stocks. Depending on how
they fare, you need to know which ones you need to buy how much of to balance
the ratios again. This script does just that.


## Usage
First, create a problem file, in this case called "problem.json" in which you
list all assets:

```json
[
    {
        "name":             "Paper 1",
        "wanted_ratio":     20,
        "current_value":    12345
    },
    {
        "name":             "Paper 2",
        "wanted_ratio":     30,
        "current_value":    3345
    },
    {
        "name":             "Paper 3",
        "wanted_ratio":     50,
        "current_value":    16345
    }
]
```

You can see we have 3 stocks which we want to have in a 2 : 3 : 5 ratio. The
values are currently 12345, 3345 and 16345, respectively. Now let's balance them:

```
$ ./pystockbalance problem.json
             Paper 1: value  12345 want 20.0% is 38.5%
             Paper 2: value   3345 want 30.0% is 10.4%
             Paper 3: value  16345 want 50.0% is 51.0%
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Need to spend: 29690
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             Paper 1: value  12345 want 20.0% is 20.0%
             Paper 2: value  18517 want 30.0% is 30.0% after buying  15172
             Paper 3: value  30862 want 50.0% is 50.0% after buying  14517
```

After spending 29690, all stocks are balanced again. Let's say you don't have
as much but still want to improve the ratios. Limit the amount of money you
have by specifying the "-a" option:

```
$ ./pystockbalance -a 10000 problem.json
             Paper 1: value  12345 want 20.0% is 38.5%
             Paper 2: value   3345 want 30.0% is 10.4%
             Paper 3: value  16345 want 50.0% is 51.0%
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Need to spend: 10000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             Paper 1: value  12345 want 20.0% is 29.4%
             Paper 2: value  11109 want 30.0% is 26.4% after buying   7764
             Paper 3: value  18581 want 50.0% is 44.2% after buying   2236

```

You'll see the ratios aren't entirely fixed, but still much improved. Now say
you have $50k and want to spend it all, keeping the ratios intact:

```
$ ./pystockbalance.py -a 50000 --spend-all problem.json
             Paper 1: value  12345 want 20.0% is 38.5%
             Paper 2: value   3345 want 30.0% is 10.4%
             Paper 3: value  16345 want 50.0% is 51.0%
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Need to spend: 50000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             Paper 1: value  16407 want 20.0% is 20.0% after buying   4062
             Paper 2: value  24610 want 30.0% is 30.0% after buying  21266
             Paper 3: value  41017 want 50.0% is 50.0% after buying  24673
```

In general, the help page can be consulted:

```
usage: pystockbalance.py [-h] [-s] [-a money] [-v] json_filename

Balance multiple asset values to achieve a common divisor ratio.

positional arguments:
  json_filename         Problem statement in JSON file form.

optional arguments:
  -h, --help            show this help message and exit
  -s, --spend-all       Get rid of all available money.
  -a money, --available-money money
                        Available money to buy. Defaults to 1000000.
  -v, --verbose         Increases verbosity. Can be specified multiple times
                        to increase.
```

## License
GNU GPL-3.
