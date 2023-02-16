```python
%load_ext conjure
```


    <IPython.core.display.Javascript object>


    Conjure extension is loaded.
    For usage help run: %conjure_help



```python
%%conjure

find x,y,z : int(0..9)
find xyz : int(400..800)
minimising xyz
such that
  xyz = 100 * x + 10 * y + z,
  x + y + z = 15,
  y = 2 * x
```




    {'x': 4, 'xyz': 483, 'y': 8, 'z': 3}


