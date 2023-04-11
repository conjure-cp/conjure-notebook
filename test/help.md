```python


%load_ext conjure

```


    <IPython.core.display.Javascript object>


    Conjure extension is loaded.
    For usage help run: %conjure_help



```python
%conjure_help
```

    Conjure jupyter extension magic commands: 
    %%conjure - Runs the provided conjure model along with previously ran models.
    %conjure_clear - clears the previously ran conjure models.
    %conjure_print - prints the previously ran conjure models.
    %conjure_rollback - removes the last appended conjure model.
    %conjure_settings - shows conjure settings menu.
    More information about Conjure: https://conjure.readthedocs.io



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


```json
{"x": 4, "xyz": 483, "y": 8, "z": 3}
```



```python
%conjure_clear
```

    Conjure model cleared



```python
w = 6
```


```python
%%conjure
given w: int
find x: int(-10..10)
such that
x = w
```


```json
{"x": 6}
```

