# Smart Math Calculator

A standard-library Python command-line calculator expanded from Hasnain Ali Mehervi's personal `smart_calculator.py` and `small smart calculator.py` exercises. This is an educational project, not commissioned client software.

## Run

Python 3.10+; no dependencies or installation needed.

```sh
python calculator.py calc add 5 3
python calculator.py calc cbrt -27
python calculator.py calc factorial 10
python calculator.py stats 1 2 3 4
python calculator.py convert -40 celsius fahrenheit
python calculator.py number 153
python -m unittest discover -s tests -v
```

## Scope

Arithmetic, roots, logarithms, trigonometry (radians), integer combinatorics, population statistics, integer properties and compatible length/mass/volume/time/temperature conversions. Run `python calculator.py calc --help` for the exact operation list. Volume uses US gallons. Calendar months/years are deliberately excluded because they are variable lengths.

The expanded version fixes even-length medians, tied modes, negative real cube roots, zero LCM, invalid numeric domains and the original `list` built-in shadowing. It has explicit operation dispatch and does not evaluate arbitrary expressions. Integer combinatorics are limited to ±1000 and number-property inputs to ±10^12; invalid domains still return errors.

## Limits

Floating-point rounding applies. Complex arithmetic, symbolic algebra, finance and electronics calculations are not implemented here. Statistical outputs are descriptive population summaries, not research conclusions. The project is a CLI, not a web application. The original snippets were consolidated and substantially rewritten; features should be attributed to this expanded version.
