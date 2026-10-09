"""Standard-library math CLI expanded from Sunny's uploaded calculator exercises."""
from __future__ import annotations
import argparse
import json
import math
import operator
import statistics

BINARY = {"add": operator.add, "subtract": operator.sub, "multiply": operator.mul,
          "divide": operator.truediv, "power": operator.pow, "modulus": operator.mod,
          "floor-divide": operator.floordiv, "hypot": math.hypot, "log": math.log}
UNARY = {"square": lambda x: x*x, "cube": lambda x: x*x*x, "sqrt": math.sqrt,
         "cbrt": lambda x: math.copysign(abs(x)**(1/3), x), "ln": math.log,
         "sin": math.sin, "cos": math.cos, "tan": math.tan,
         "asin": math.asin, "acos": math.acos, "atan": math.atan,
         "absolute": abs, "ceil": math.ceil, "floor": math.floor,
         "radians": math.radians, "degrees": math.degrees}
INTEGER = {"factorial": (1, math.factorial), "gcd": (2, math.gcd), "lcm": (2, math.lcm),
           "combination": (2, math.comb), "permutation": (2, math.perm)}
UNITS = {"length": {"m":1, "cm":.01,"inch":.0254,"km":1000,"mile":1609.344},
         "mass": {"kg":1,"g":.001,"lb":.45359237},
         "volume": {"liter":1,"ml":.001,"us-gallon":3.785411784},
         "time": {"second":1,"minute":60,"hour":3600,"day":86400,"week":604800}}

def finite(value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError("Use finite real numbers.")
    return value

def calculate(operation: str, values: list[float]) -> int | float:
    for value in values: finite(value)
    if operation in INTEGER:
        arity, fn = INTEGER[operation]
        if len(values) != arity or any(not float(v).is_integer() or abs(v)>1000 for v in values):
            raise ValueError(f"{operation} needs {arity} whole number(s) between -1000 and 1000.")
        result = fn(*(int(v) for v in values))
    else:
        fn = BINARY.get(operation) or UNARY.get(operation)
        if fn is None: raise ValueError("Unknown operation.")
        arity = 2 if operation in BINARY else 1
        if len(values) != arity: raise ValueError(f"{operation} needs {arity} number(s).")
        result = fn(*values)
    if isinstance(result, complex): raise ValueError("Complex results are outside this real-number calculator.")
    # Large factorials are deliberately kept as integers, not cast to float.
    if isinstance(result, float): finite(result)
    return result

def summarize(values: list[float]) -> dict:
    if not 1 <= len(values) <= 10000: raise ValueError("Use 1–10000 values.")
    for value in values: finite(value)
    result = {"count":len(values),"mean":statistics.mean(values),"median":statistics.median(values),
              "modes":statistics.multimode(values),"population_variance":statistics.pvariance(values),
              "population_stddev":statistics.pstdev(values)}
    for key in ("mean","median","population_variance","population_stddev"): finite(result[key])
    return result

def convert(value: float, source: str, target: str) -> float:
    finite(value)
    temperatures={"celsius","fahrenheit","kelvin"}
    if source in temperatures and target in temperatures:
        celsius = value if source=="celsius" else (value-32)*5/9 if source=="fahrenheit" else value-273.15
        if celsius < -273.15: raise ValueError("Temperature is below absolute zero.")
        result = celsius if target=="celsius" else celsius*9/5+32 if target=="fahrenheit" else celsius+273.15
    else:
        group=next((g for g in UNITS.values() if source in g and target in g),None)
        if group is None: raise ValueError("Units must be recognized and belong to the same quantity.")
        if value < 0: raise ValueError("Non-temperature quantities must be nonnegative.")
        result=value*group[source]/group[target]
    return finite(result)

def number_properties(number: int) -> dict:
    if isinstance(number,bool) or not isinstance(number,int) or abs(number)>10**12:
        raise ValueError("Use an integer between -10^12 and 10^12.")
    prime = number>1 and all(number % divisor for divisor in range(2,math.isqrt(number)+1))
    digits=str(abs(number))
    return {"integer":number,"even":number%2==0,"prime":prime,
            "perfect_square":number>=0 and math.isqrt(number)**2==number,
            "armstrong":number>=0 and number==sum(int(d)**len(digits) for d in digits),
            "palindrome":str(number)==str(number)[::-1]}

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest="command",required=True)
    calc=commands.add_parser("calc",help="Arithmetic and functions; trig inputs are radians")
    calc.add_argument("operation",choices=sorted(BINARY|UNARY|INTEGER));calc.add_argument("values",nargs="+",type=float)
    stats=commands.add_parser("stats",help="Descriptive population statistics")
    stats.add_argument("values",nargs="+",type=float)
    units=commands.add_parser("convert",help="Compatible unit conversion")
    units.add_argument("value",type=float);units.add_argument("source");units.add_argument("target")
    props=commands.add_parser("number",help="Integer properties")
    props.add_argument("value",type=int)
    args=parser.parse_args(argv)
    try:
        if args.command=="calc":result=calculate(args.operation,args.values)
        elif args.command=="stats":result=summarize(args.values)
        elif args.command=="convert":result=convert(args.value,args.source,args.target)
        else:result=number_properties(args.value)
        print(json.dumps(result,allow_nan=False,indent=2))
    except (ValueError, ZeroDivisionError, OverflowError) as error:
        parser.exit(2,f"Error: {error}\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
