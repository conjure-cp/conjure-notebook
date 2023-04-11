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
%%conjure

given w: int
find x : int(0..9)
such that
  w = x

```


```json
{"x": 7}
```

