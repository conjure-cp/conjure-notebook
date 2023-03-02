```python
%load_ext conjure

```


    <IPython.core.display.Javascript object>


    Conjure extension is loaded.
    For usage help run: %conjure_help



```python
w = 7
```


```python
%%conjure --number-of-solutions all --solver minion

given w: int
find x : int(0..9)
such that
  w = x /\ (w != x)
```




    'No solution'




```python
"x" in locals()
```




    False




```python
%conjure_clear
```

    Conjure model cleared



```python
%%conjure --number-of-solutions all --solver minion

$ -O0 -S0 is to ensure solutions come out in lex order
given w: int
find x : int(0..9)
such that
  w != x
```




    {'conjure_solutions': [{'x': 0},
      {'x': 1},
      {'x': 2},
      {'x': 3},
      {'x': 4},
      {'x': 5},
      {'x': 6},
      {'x': 8},
      {'x': 9}]




```python
"x" in locals()
```




    False




```python
%conjure_clear
```

    Conjure model cleared



```python
%%conjure --number-of-solutions all --solver minion
given w: int
find x : int(0..9)
find y:  int(5..12)
such that
  x*y=w
```




    {'x': 1, 'y': 7}




```python
print("x" in locals())
```

    True

