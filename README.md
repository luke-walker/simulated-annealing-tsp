# Traveling Salesman Problem w/ Simulated Annealing Optimization
## Dependencies
- **Python>=3.8**

```pip install matplotlib numpy```
- **matplotlib>=3.7.5**
- **numpy>=1.24.4**

## Command-line Arguments
|Argument|Description|Required?
|-|-|-
|-h, --help|Display help message|N
|-f, --file PATH|Specify the .csv file to use|Y/N [^1]
|-n, --count #|Specify the number of random data points|Y/N [^1]
|-r, --reheat #|Specify the number of iterations before the temperature is reset|Y
|-i, --iterations #|Specify the total number of iterations|Y/N [^2]
|-s, --seed #|Specify the PRNG seed|N
|-a, --animate|Display animated plots|N

[^1]: Either ```-f``` or ```-n``` must be specified, but not both.
[^2]: Must be specified if ```-a``` is not used.

## Run
```python main.py <args> [options]```

Example:
```python main.py -n 50 -r 100 -i 1000```
